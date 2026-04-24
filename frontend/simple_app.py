import streamlit as st
import pandas as pd
import sqlite3
import hashlib
from datetime import datetime
import requests
import time

# Page config
st.set_page_config(
    page_title="Job Copilot SaaS",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CUSTOM CSS WITH DARK MODE SUPPORT =============
def apply_css(dark_mode=False):
    if dark_mode:
        bg_gradient = "linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)"
        card_bg = "#1e2746"
        text_color = "#ffffff"
        metric_bg = "#0f3460"
    else:
        bg_gradient = "linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)"
        card_bg = "white"
        text_color = "#2c3e50"
        metric_bg = "white"
    
    st.markdown(f"""
    <style>
        /* Main app background */
        .stApp {{
            background: {bg_gradient};
        }}
        
        /* Modern card design */
        .job-card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 1.5rem;
            color: white;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .job-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 40px rgba(0,0,0,0.3);
        }}
        
        /* Modern metric cards */
        .metric-card {{
            background: {metric_bg};
            padding: 1.5rem;
            border-radius: 1rem;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.3s;
            border: none;
            color: {text_color};
        }}
        
        .metric-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        }}
        
        .metric-card h3 {{
            font-size: 2rem;
            margin: 0;
            color: #667eea;
        }}
        
        /* Job listing card */
        .job-listing-card {{
            background: {card_bg};
            border-radius: 0.75rem;
            padding: 1.25rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            transition: all 0.3s;
            color: {text_color};
            border-left: 4px solid #667eea;
        }}
        
        .job-listing-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }}
        
        /* Modern buttons */
        .stButton > button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 0.5rem;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            transition: all 0.3s;
            width: 100%;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }}
        
        /* Modern expanders */
        .streamlit-expanderHeader {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 0.5rem;
            font-weight: bold;
        }}
        
        /* Modern inputs */
        .stTextInput > div > div > input {{
            border-radius: 0.5rem;
            border: 2px solid #e0e0e0;
            padding: 0.5rem;
            transition: all 0.3s;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: #667eea;
            box-shadow: 0 0 0 2px rgba(102,126,234,0.2);
        }}
        
        /* Sidebar styling */
                .css-1d391kg {{
            background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
        }}
        
        /* Typography */
        h1, h2, h3 {{
            color: {text_color} !important;
            font-weight: 700 !important;
        }}
        
        /* Gradient text for titles */
        .gradient-text {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 2.5rem;
            font-weight: bold;
        }}
        
        /* Salary badge */
        .salary-badge {{
            background: #28a745;
            color: white;
            padding: 0.25rem 0.75rem;
            border-radius: 1rem;
            font-size: 0.875rem;
            font-weight: bold;
            display: inline-block;
        }}
        
        /* Tag styling */
        .skill-tag {{
            background: #e3f2fd;
            color: #1976d2;
            padding: 0.25rem 0.5rem;
            border-radius: 0.25rem;
            font-size: 0.75rem;
            margin: 0.25rem;
            display: inline-block;
        }}
        
        /* Animation for loading */
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .stExpander, .job-listing-card {{
            animation: fadeInUp 0.5s ease-out;
        }}
        
        /* Success/Info/Warning boxes */
        .stAlert {{
            border-radius: 0.5rem;
            border-left: 4px solid;
        }}
        
        /* Footer */
        .footer {{
            text-align: center;
            padding: 2rem;
            color: #666;
            font-size: 0.875rem;
        }}
    </style>
    """, unsafe_allow_html=True)

# ============= DATABASE SETUP =============
def init_database():
    conn = sqlite3.connect('jobcopilot.db', check_same_thread=False)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            name TEXT,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_title TEXT,
            job_url TEXT,
            job_salary TEXT,
            job_type TEXT,
            saved_at TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            job_title TEXT,
            company TEXT,
            job_url TEXT,
            applied_date TIMESTAMP,
            status TEXT DEFAULT 'applied'
        )
    ''')
    
    conn.commit()
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(conn, email, name, password):
    cursor = conn.cursor()
    password_hash = hash_password(password)
    try:
        cursor.execute('INSERT INTO users (email, name, password_hash, created_at) VALUES (?, ?, ?, ?)',
                      (email, name, password_hash, datetime.now()))
        conn.commit()
        return cursor.lastrowid
    except:
        return None

def login_user(conn, email, password):
    cursor = conn.cursor()
    cursor.execute('SELECT id, email, name, password_hash FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user and hash_password(password) == user[3]:
        return {'id': user[0], 'email': user[1], 'name': user[2]}
    return None

def save_job(conn, user_id, title, url, salary, job_type):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO saved_jobs (user_id, job_title, job_url, job_salary, job_type, saved_at) VALUES (?,?,?,?,?,?)',
                  (user_id, title, url, salary, job_type, datetime.now()))
    conn.commit()

def get_saved_jobs(conn, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT job_title, job_url, job_salary, job_type FROM saved_jobs WHERE user_id = ?', (user_id,))
    return cursor.fetchall()

# ============= ADZUNA API =============
ADZUNA_APP_ID = "cba1c51a"
ADZUNA_APP_KEY = "39f3605c39092"

def search_jobs(what, where='', results=25):
    url = "https://api.adzuna.com/v1/api/jobs/us/search/1"
    params = {
        'app_id': ADZUNA_APP_ID,
        'app_key': ADZUNA_APP_KEY,
        'results_per_page': results,
        'what': what,
        'content-type': 'application/json'
    }
    if where and where.strip() and where.lower() != 'remote':
        params['where'] = where
    
    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()
        jobs = []
        for job in data.get('results', []):
            jobs.append({
                'title': job.get('title', 'Untitled'),
                'company': job.get('company', {}).get('display_name', 'Unknown'),
                'salary': f"${job.get('salary_min', '')}-${job.get('salary_max', '')}" if job.get('salary_min') else "Not specified",
                'location': job.get('location', {}).get('display_name', 'Various'),
                'url': job.get('redirect_url', ''),
                'description': job.get('description', 'No description available')[:200],
                'created': job.get('created', 'Recently')
            })
        return jobs
    except:
        return []

# ============= SESSION STATE =============
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = init_database()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False

# Apply CSS with current dark mode setting
apply_css(st.session_state.dark_mode)

# ============= LOGIN/REGISTER UI =============
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="job-card" style="text-align: center;">
            <div style="font-size: 4rem;">🎯</div>
            <h1 style="margin: 0; color: white;">Job Copilot</h1>
            <p style="margin: 0; opacity: 0.9;">Your AI-Powered Job Search Assistant</p>
        </div>
        """, unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            with st.form("login"):
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                if st.form_submit_button("Login"):
                    user = login_user(st.session_state.db_conn, email, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.user_id = user['id']
                        st.session_state.user_name = user['name']
                        st.rerun()
                    else:
                        st.error("❌ Invalid email or password")
        
        with tab2:
            with st.form("register"):
                name = st.text_input("Full Name", placeholder="John Doe")
                email = st.text_input("Email", placeholder="your@email.com")
                password = st.text_input("Password", type="password", placeholder="••••••••")
                confirm = st.text_input("Confirm Password", type="password")
                if st.form_submit_button("Register"):
                    if password != confirm:
                        st.error("❌ Passwords don't match")
                    elif register_user(st.session_state.db_conn, email, name, password):
                        st.success("✅ Registered! Please login.")
                    else:
                        st.error("❌ Email already exists")

# ============= MAIN APP =============
else:
    # Sidebar with dark mode toggle
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 3rem;">👤</div>
            <h3 style="margin: 0;">{st.session_state.user_name}</h3>
            <p style="margin: 0; opacity: 0.8;">Job Seeker</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dark mode toggle
        dark_mode = st.toggle("🌙 Dark Mode", value=st.session_state.dark_mode)
        if dark_mode != st.session_state.dark_mode:
            st.session_state.dark_mode = dark_mode
            st.rerun()
        
        st.markdown("---")
        
        page = st.radio("📋 Menu", [
            "🏠 Dashboard", 
            "🔍 Job Matches", 
            "💾 Saved Jobs", 
            "📋 Applications",
            "👤 Profile"
        ])
        
        st.markdown("---")
        
        # Stats in sidebar
        saved_count = len(get_saved_jobs(st.session_state.db_conn, st.session_state.user_id))
        col1, col2 = st.columns(2)
        with col1:
            st.metric("💾 Saved", saved_count)
        with col2:
            st.metric("📊 Applied", 0)
        
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    
    # Main content area
    if page == "🏠 Dashboard":
        # Welcome banner
        st.markdown(f"""
        <div class="job-card">
            <h2>👋 Welcome back, {st.session_state.user_name}!</h2>
            <p>Your AI job search assistant is ready to help you land your dream job.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{saved_count}</h3>
                <p>💾 Saved Jobs</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>0</h3>
                <p>📋 Applications</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>65%</h3>
                <p>📊 Profile Complete</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick search
        st.markdown("---")
        st.markdown("### 🔍 Quick Job Search")
        quick_search = st.text_input("", placeholder="e.g., software engineer, nurse, teacher", label_visibility="collapsed")
        if quick_search:
            st.session_state.quick_search = quick_search
            st.session_state.page = "🔍 Job Matches"
            st.rerun()
        
        # Tips
        with st.expander("💡 Pro Tips for Job Search"):
            st.markdown("""
            - **Use specific keywords** like 'Python developer' instead of just 'developer'
            - **Leave location blank** for nationwide results
            - **Save jobs** you're interested in to apply later
            - **Track applications** to stay organized
            - **Complete your profile** for better job matches
            """)
    
    elif page == "🔍 Job Matches":
        st.markdown('<h1 style="text-align: center;">🔍 Find Your Dream Job</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        # Search filters
        col1, col2 = st.columns([2, 1])
        with col1:
            keyword = st.text_input("Job Title / Keyword", "software engineer", placeholder="e.g., data scientist, project manager")
        with col2:
            location = st.text_input("Location (optional)", "", placeholder="e.g., New York or leave blank")
        
        if st.button("🔍 Search Jobs", type="primary", use_container_width=True):
            with st.spinner("🔍 AI is searching for your dream job..."):
                time.sleep(0.5)
                jobs = search_jobs(keyword, location, 25)
                
                if jobs:
                    st.success(f"✨ Found {len(jobs)} jobs matching your criteria!")
                    
                    for idx, job in enumerate(jobs):
                        # Determine salary display
                        salary_display = job['salary'] if job['salary'] != "Not specified" else "💰 Salary not specified"
                        
                        st.markdown(f"""
                        <div class="job-listing-card">
                            <div style="display: flex; justify-content: space-between; align-items: start; flex-wrap: wrap;">
                                <div style="flex: 1;">
                                    <h3 style="margin: 0 0 0.5rem 0;">📌 {job['title']}</h3>
                                    <p style="margin: 0; color: #667eea; font-weight: bold;">🏢 {job['company']}</p>
                                </div>
                                <div>
                                    <span class="salary-badge">{salary_display}</span>
                                </div>
                            </div>
                            <div style="margin-top: 0.75rem;">
                                <span style="background: #e3f2fd; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem;">
                                    📍 {job['location']}
                                </span>
                                <span style="background: #f3e5f5; padding: 0.25rem 0.5rem; border-radius: 0.25rem; font-size: 0.875rem; margin-left: 0.5rem;">
                                    📅 {job['created'][:10] if job['created'] != 'Recently' else 'Recently'}
                                </span>
                            </div>
                            <p style="margin-top: 0.75rem; color: #666;">{job['description'][:150]}...</p>
                            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
                                <a href="{job['url']}" target="_blank" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-decoration: none; font-weight: bold;">
                                    🔗 Apply Now
                                </a>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        col1, col2 = st.columns([1, 5])
                        with col1:
                            if st.button(f"💾 Save", key=f"save_{idx}"):
                                save_job(st.session_state.db_conn, st.session_state.user_id,
                                        job['title'], job['url'], job['salary'], "Full Time")
                                st.toast("✅ Job saved to your list!", icon="🎉")
                else:
                    st.warning("😕 No jobs found. Try different keywords or location!")
    
    elif page == "💾 Saved Jobs":
        st.markdown('<h1 style="text-align: center;">💾 Your Saved Jobs</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        saved = get_saved_jobs(st.session_state.db_conn, st.session_state.user_id)
        if saved:
            for idx, job in enumerate(saved):
                st.markdown(f"""
                <div class="job-listing-card">
                    <h3>📌 {job[0]}</h3>
                    <p>💰 {job[2]}</p>
                    <p>⏰ {job[3]}</p>
                    <a href="{job[1]}" target="_blank" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 0.5rem 1rem; border-radius: 0.5rem; text-decoration: none; display: inline-block; margin-top: 0.5rem;">
                        🔗 Apply Now
                    </a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("📭 No saved jobs yet. Search for jobs and click 'Save' to build your list!")
    
    elif page == "📋 Applications":
        st.markdown('<h1 style="text-align: center;">📋 Track Your Applications</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("track_application"):
            st.markdown("### 📝 Add New Application")
            col1, col2 = st.columns(2)
            with col1:
                job_title = st.text_input("Job Title", placeholder="e.g., Senior Software Engineer")
                company = st.text_input("Company", placeholder="e.g., Google")
            with col2:
                status = st.selectbox("Status", ["📝 Applied", "📞 Interview", "🎉 Offer", "❌ Rejected"])
                date = st.date_input("Application Date", datetime.now())
            
            if st.form_submit_button("📌 Track Application", use_container_width=True):
                st.success(f"✅ Application tracked successfully! Status: {status}")
        
        st.markdown("---")
        st.info("💡 Your tracked applications will appear here. Start by adding your first application above!")
    
    elif page == "👤 Profile":
        st.markdown('<h1 style="text-align: center;">👤 Your Profile</h1>', unsafe_allow_html=True)
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 📋 Personal Information")
            name = st.text_input("Full Name", st.session_state.user_name)
            email = st.text_input("Email", "", disabled=True)
            location = st.text_input("Location", "Remote / Anywhere")
            experience = st.slider("Years of Experience", 0, 30, 5)
        
        with col2:
            st.markdown("### 💪 Skills & Expertise")
            skills = st.text_area("Skills (comma separated)", "Python, Project Management, Communication, Leadership")
            st.markdown("### 🎯 Job Preferences")
            preferred_role = st.text_input("Target Role", "Software Engineer")
            preferred_salary = st.number_input("Minimum Salary ($/hr)", 0, 200, 25)
        
        if st.button("💾 Save Profile", type="primary", use_container_width=True):
            st.success("✅ Profile saved successfully!")
            st.balloons()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p>🎯 Job Copilot SaaS | Powered by Adzuna API | Your AI Job Search Assistant</p>
        <p style="font-size: 0.75rem;">© 2026 Job Copilot. All rights reserved.</p>
    </div>
    """, unsafe_allow_html=True)