# frontend/pages/5_Profile.py
import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    st.markdown("## 👤 My Profile")
    st.markdown("Manage your profile and preferences")
    
    tab1, tab2, tab3 = st.tabs(["📋 Personal Info", "💪 Skills & Experience", "⚙️ Job Preferences"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name", st.session_state.get('user_name', ''))
            email = st.text_input("Email", st.session_state.get('user_email', ''))
            phone = st.text_input("Phone", "+1 234 567 8900")
            location = st.text_input("Location", "Remote / Philippines")
            linkedin = st.text_input("LinkedIn URL", "https://linkedin.com/in/username")
        
        with col2:
            st.markdown("#### 📄 Resume/CV")
            uploaded_file = st.file_uploader("Upload Resume (PDF/DOCX)", type=['pdf', 'docx'])
            
            if uploaded_file:
                st.success(f"✅ {uploaded_file.name} uploaded successfully!")
                
                # Show AI analysis option for premium users
                if st.session_state.get('subscription_plan') == 'premium':
                    if st.button("🔍 Analyze Resume with AI", use_container_width=True):
                        with st.spinner("AI analyzing your resume..."):
                            st.success("Analysis complete! Check your skill gap report.")
                else:
                    st.info("💡 Upgrade to Premium for AI resume analysis")
            
            st.markdown("#### 🎯 Profile Summary")
            bio = st.text_area("Short Bio", height=100, 
                              placeholder="Brief description of yourself, career goals, and what you're looking for...")
        
        if st.button("💾 Save Personal Info", use_container_width=True):
            st.success("Profile updated successfully!")
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            years_exp = st.slider("Years of Experience", 0, 30, 5)
            current_role = st.text_input("Current/Most Recent Role", "Project Manager")
            education = st.selectbox("Highest Education", 
                                     ["High School", "Bachelor's", "Master's", "PhD", "Other"])
        
        with col2:
            st.markdown("#### Top Skills")
            skills = st.text_area("Skills (comma separated)", 
                                 "Project Management, Communication, Leadership, Problem Solving, Data Analysis")
            
            st.markdown("#### Certifications")
            certifications = st.text_area("Certifications", "PMP, Scrum Master, AWS Cloud Practitioner")
        
        st.markdown("#### 💼 Work Experience")
        
        # Dynamic work experience entries
        if 'work_experience_count' not in st.session_state:
            st.session_state.work_experience_count = 1
        
        for i in range(st.session_state.work_experience_count):
            with st.expander(f"Experience {i+1}", expanded=(i==0)):
                col_a, col_b = st.columns(2)
                with col_a:
                    job_title = st.text_input(f"Job Title", key=f"job_title_{i}")
                    company = st.text_input(f"Company", key=f"company_{i}")
                with col_b:
                    start_date = st.date_input(f"Start Date", key=f"start_{i}")
                    end_date = st.date_input(f"End Date", key=f"end_{i}")
                
                responsibilities = st.text_area(f"Key Responsibilities & Achievements", 
                                               key=f"resp_{i}", height=100)
        
        if st.button("➕ Add Another Experience"):
            st.session_state.work_experience_count += 1
            st.rerun()
        
        if st.button("💾 Save Skills & Experience", use_container_width=True):
            st.success("Skills and experience saved!")
    
    with tab3:
        st.markdown("### 🎯 Job Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            min_salary = st.number_input("Minimum Desired Salary ($/hr)", min_value=0, value=25, step=5)
            max_salary = st.number_input("Maximum Desired Salary ($/hr)", min_value=0, value=50, step=5)
            
            job_types = st.multiselect("Preferred Job Types", 
                                       ["Full Time", "Part Time", "Contract", "Freelance", "Internship"],
                                       default=["Full Time"])
            
            work_location = st.radio("Work Location", ["Remote Only", "Hybrid", "On-site", "Any"], index=0)
        
        with col2:
            industries = st.multiselect("Preferred Industries",
                                       ["Technology", "Healthcare", "Finance", "Marketing/Advertising", 
                                        "Education", "E-commerce", "Manufacturing", "Non-profit"],
                                       default=["Technology"])
            
            company_size = st.select_slider("Preferred Company Size",
                                           options=["Startup (1-50)", "Small (51-200)", "Medium (201-1000)", 
                                                    "Large (1001-10000)", "Enterprise (10000+)"],
                                           value="Medium (201-1000)")
            
            travel_pref = st.selectbox("Travel Preference", ["No travel", "Occasional (<25%)", "Some (25-50%)", "Willing to travel"])
        
        st.markdown("### 📍 Location Preferences (if hybrid/on-site)")
        
        cities = st.multiselect("Preferred Cities", 
                               ["New York", "San Francisco", "Los Angeles", "Chicago", "Austin", 
                                "Seattle", "Boston", "Denver", "Remote/Anywhere"],
                               default=["Remote/Anywhere"])
        
        st.markdown("### 🔍 Additional Preferences")
        
        col1, col2 = st.columns(2)
        with col1:
            immediate_start = st.checkbox("Available to start immediately")
            visa_sponsorship = st.checkbox("Require visa sponsorship")
        with col2:
            equity_pref = st.selectbox("Equity preference", ["Not important", "Nice to have", "Important", "Required"])
        
        if st.button("💾 Save Job Preferences", use_container_width=True):
            st.success("Job preferences saved! Your job matches will improve.")
    
    # Profile completion
    st.markdown("---")
    st.markdown("### 📊 Profile Completion")
    completion = 65  # Calculate based on filled fields
    st.progress(completion/100, text=f"{completion}% Complete")
    
    if completion < 100:
        st.info("Complete your profile to get better job matches!")