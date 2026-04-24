import streamlit as st
import pandas as pd
import glob
import os
import sqlite3
import hashlib
from datetime import datetime
from adzuna_client import adzuna
# ============= DATABASE SETUP =============
def init_database():
    conn = sqlite3.connect('jobcopilot.db', check_same_thread=False)
    cursor = conn.cursor()
    
    # Users table (without last_login to avoid errors)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP
        )
    ''')
    
    # User profiles table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            location TEXT,
            years_experience INTEGER,
            current_role TEXT,
            skills TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Saved jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_title TEXT,
            job_url TEXT,
            job_salary TEXT,
            job_type TEXT,
            saved_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # Applications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_title TEXT,
            company TEXT,
            job_url TEXT,
            applied_date TIMESTAMP,
            status TEXT DEFAULT 'applied',
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, hash_value):
    return hash_password(password) == hash_value

def register_user(conn, email, name, password):
    cursor = conn.cursor()
    password_hash = hash_password(password)
    try:
        cursor.execute('''
            INSERT INTO users (email, name, password_hash, created_at, subscription_plan)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, name, password_hash, datetime.now(), 'free'))
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError:
        return None

def login_user(conn, email, password):
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    
    if user and verify_password(password, user[3]):
        # No last_login update to avoid errors
        return {'id': user[0], 'email': user[1], 'name': user[2]}
    return None

def save_profile(conn, user_id, location, years_exp, current_role, skills):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO user_profiles (user_id, location, years_experience, current_role, skills)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, location, years_exp, current_role, skills))
    conn.commit()

def get_profile(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT location, years_experience, current_role, skills FROM user_profiles WHERE user_id = ?', (user_id,))
    return cursor.fetchone()

def save_job(conn, user_id, job_title, job_url, job_salary, job_type):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO saved_jobs (user_id, job_title, job_url, job_salary, job_type, saved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, job_title, job_url, job_salary, job_type, datetime.now()))
    conn.commit()
    return cursor.lastrowid

def get_saved_jobs(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT job_title, job_url, job_salary, job_type, saved_at 
        FROM saved_jobs WHERE user_id = ? ORDER BY saved_at DESC
    ''', (user_id,))
    return cursor.fetchall()

def track_application(conn, user_id, job_title, company, job_url):
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (user_id, job_title, company, job_url, applied_date, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, job_title, company, job_url, datetime.now(), 'applied'))
    conn.commit()

def get_applications(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('''
        SELECT job_title, company, applied_date, status 
        FROM applications WHERE user_id = ? ORDER BY applied_date DESC
    ''', (user_id,))
    return cursor.fetchall()

# ============= PAGE CONFIG =============
st.set_page_config(page_title="Job Copilot SaaS", page_icon="🎯", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
    @media only screen and (max-width: 768px) {
        .stButton button { width: 100% !important; }
        button { min-height: 44px !important; }
    }
    .job-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ============= INITIALIZE =============
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = init_database()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'sidebar_open' not in st.session_state:
    st.session_state.sidebar_open = False

# ============= JOB LOADING FUNCTION =============
def load_and_display_jobs():
    """Load and display LIVE jobs from Adzuna API"""
    
    st.markdown("### 🔍 Search Live Jobs")
    
    # Search filters
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        search_query = st.text_input("Job Title / Keyword", "developer", key="job_search_input")
    with col2:
        location = st.text_input("Location (optional - leave blank for nationwide)", "", key="job_location_input")
    st.caption("💡 Examples: 'new york', 'chicago', 'remote' (may show fewer results)")
    with col3:
        results_count = st.selectbox("Results", [10, 25, 50], index=1, key="job_results_count")
    
    if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
        with st.spinner(f"Searching for '{search_query}' jobs..."):
            try:
                jobs = adzuna.search_jobs(search_query, location, results_count)
                
                if jobs:
                    st.success(f"📊 Found {len(jobs)} jobs!")
                    
                    for idx, job in enumerate(jobs):
                        with st.expander(f"📌 {job['title'][:60]}", expanded=False):
                            col1, col2 = st.columns([2, 1])
                            with col1:
                                st.write(f"**🏢 Company:** {job['company']}")
                                st.write(f"**💰 Salary:** {job['salary_preview']}")
                                st.write(f"**📍 Location:** {job['location']}")
                                st.write(f"**⏰ Type:** {job['job_type']}")
                                st.write(f"**🔧 Skills:** {job['tags']}")
                                
                                # Show description preview
                                desc = job.get('description', '')
                                if len(desc) > 250:
                                    st.write(f"**📝 Description:** {desc[:250]}...")
                                else:
                                    st.write(f"**📝 Description:** {desc}")
                            
                            with col2:
                                if job['url']:
                                    st.link_button("🔗 Apply Now", job['url'], use_container_width=True)
                                
                                # Save button connects to your database
                                if st.button(f"💾 Save Job", key=f"save_live_{idx}"):
                                    save_job(
                                        st.session_state.db_conn, 
                                        st.session_state.user_id, 
                                        job['title'], 
                                        job['url'], 
                                        job['salary_preview'], 
                                        job['job_type']
                                    )
                                    st.toast("✅ Job saved to your list!")
                else:
                    st.info(f"No jobs found for '{search_query}'. Try a different keyword or location.")
                    st.caption("💡 **Popular searches:** 'developer', 'project manager', 'data analyst', 'marketing', 'sales'")
                    
            except Exception as e:
                st.error(f"Error fetching jobs: {e}")
                st.info("The job search will work once connected. You can still browse saved jobs.")
    
    # Show saved jobs count
    saved_count = len(get_saved_jobs(st.session_state.db_conn, st.session_state.user_id))
    if saved_count > 0:
        st.markdown("---")
        st.caption(f"💾 You have {saved_count} saved jobs. Go to 'Saved Jobs' tab to view them.")
# ============= LOGIN/REGISTER =============
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div class="job-card" style="text-align: center;">', unsafe_allow_html=True)
        st.markdown("### 🎯 Job Copilot SaaS")
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                if st.form_submit_button("Login", use_container_width=True):
                    user = login_user(st.session_state.db_conn, email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['id']
                        st.session_state.user_email = user['email']
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("Invalid email or password")
        
        with tab2:
            with st.form("register_form"):
                name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                confirm = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Register", use_container_width=True):
                    if password != confirm:
                        st.error("Passwords don't match")
                    elif register_user(st.session_state.db_conn, email, name, password):
                        st.success("Registration successful! Please login.")
                    else:
                        st.error("Email already exists")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ============= MAIN APP =============
else:
    # Sidebar toggle
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("☰"):
            st.session_state.sidebar_open = not st.session_state.sidebar_open
    
    if st.session_state.sidebar_open:
        with st.sidebar:
            st.markdown(f"### 👤 {st.session_state.user_name}")
            st.caption(st.session_state.user_email)
            st.markdown("---")
            
            page = st.radio("Navigation", 
                ["🏠 Dashboard", "🎯 Job Matches", "💾 Saved Jobs", "📋 Applications", "👤 Profile"])
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()
    else:
        page = "🏠 Dashboard"
    
    # Get counts for display
    saved_count = len(get_saved_jobs(st.session_state.db_conn, st.session_state.user_id))
    app_count = len(get_applications(st.session_state.db_conn, st.session_state.user_id))
    
    # Page routing
    if page == "🏠 Dashboard":
        st.markdown(f"""
        <div class="job-card">
            <h2>👋 Welcome back, {st.session_state.user_name}!</h2>
            <p>Your AI job search assistant is ready</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Saved Jobs", saved_count)
        with col2:
            st.metric("Applications", app_count)
        with col3:
            st.metric("Profile", "65%")
        
        st.markdown("---")
        st.markdown("### 📋 Recent Jobs")
        load_and_display_jobs()
    
    elif page == "🎯 Job Matches":
        st.markdown("## 🎯 Find Jobs")
        load_and_display_jobs()
    
    elif page == "💾 Saved Jobs":
        st.markdown("## 💾 Saved Jobs")
        saved = get_saved_jobs(st.session_state.db_conn, st.session_state.user_id)
        for job in saved:
            with st.expander(f"📌 {job[0]}"):
                st.write(f"💰 {job[2]} | ⏰ {job[3]}")
                if job[1]:
                    st.link_button("Apply", job[1])
    
    elif page == "📋 Applications":
        st.markdown("## 📋 Applications")
        apps = get_applications(st.session_state.db_conn, st.session_state.user_id)
        for app in apps:
            st.write(f"📌 {app[0]} at {app[1]} - {app[2]} - {app[3]}")
    
    elif page == "👤 Profile":
        st.markdown("## 👤 Profile")
        profile = get_profile(st.session_state.db_conn, st.session_state.user_id)
        with st.form("profile_form"):
            location = st.text_input("Location", profile[0] if profile else "Remote")
            years = st.number_input("Years Experience", 0, 30, profile[1] if profile else 5)
            role = st.text_input("Current Role", profile[2] if profile else "")
            skills = st.text_area("Skills", profile[3] if profile else "")
            if st.form_submit_button("Save"):
                save_profile(st.session_state.db_conn, st.session_state.user_id, location, years, role, skills)
                st.success("Saved!")