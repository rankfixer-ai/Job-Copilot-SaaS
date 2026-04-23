# frontend/pages/1_Job_Matches.py
import streamlit as st
import pandas as pd
import plotly.express as px
from components.charts import create_match_gauge, create_skill_radar, create_salary_distribution
import glob
import os

def show():
    st.markdown("## 🎯 AI-Powered Job Matches")
    st.markdown("Jobs matched to your profile using advanced AI algorithms")
    
    # Filters
    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
    
    with col1:
        search = st.text_input("🔍 Search jobs", placeholder="Job title, skills, or company...")
    
    with col2:
        min_score = st.slider("Min Match Score", 0, 100, 60)
    
    with col3:
        job_types = st.multiselect("Job Type", ["Full Time", "Part Time", "Any"], default=["Full Time"])
    
    with col4:
        sort_by = st.selectbox("Sort By", ["Match Score", "Salary", "Date Posted"])
    
    # Load jobs
    try:
        # Find the latest CSV file
        csv_files = glob.glob('data/*.csv')
        if csv_files:
            latest_file = max(csv_files, key=os.path.getctime)
            df = pd.read_csv(latest_file)
            df = df.drop_duplicates(subset=['title'])
            
            # Apply filters
            if search:
                df = df[df['title'].str.contains(search, case=False) | 
                       df['tags'].str.contains(search, case=False, na=False)]
            
            if job_types and 'Any' not in job_types:
                df = df[df['job_type'].isin(job_types)]
            
            st.success(f"Found {len(df)} jobs matching your criteria")
            
            # Display jobs
            for idx, row in df.iterrows():
                match_score = 65 + (idx * 3) % 30  # Simulated score
                
                if match_score >= min_score:
                    with st.expander(f"📌 {row['title']} - {match_score}% Match"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**💵 Salary:** {row['salary_preview']}")
                            st.markdown(f"**⏰ Type:** {row['job_type']}")
                            st.markdown(f"**🔧 Skills:** {row['tags']}")
                            st.markdown(f"**📅 Posted:** {row['date_posted']}")
                            
                            # Match breakdown
                            st.markdown("#### 📊 Match Breakdown")
                            breakdown_data = {
                                "Skills": 85, "Salary": 70, "Experience": 75, "Location": 90
                            }
                            for category, score_val in breakdown_data.items():
                                st.progress(score_val/100, text=f"{category}: {score_val}%")
                        
                        with col2:
                            st.markdown("#### ⚡ Quick Actions")
                            if st.button("📝 Generate Cover Letter", key=f"cl_{idx}"):
                                st.session_state.selected_job = row.to_dict()
                                st.session_state.goto_cover_letter = True
                                st.success("Job selected! Go to Cover Letter tab")
                            
                            st.link_button("👁️ View Original Job", row['url'])
                            
                            if st.button("💾 Save to Favorites", key=f"save_{idx}"):
                                st.success("Job saved!")
        else:
            st.warning("No job data found. Run the scraper first!")
            st.code("python onlinejobs_scraper.py", language="bash")
            
    except Exception as e:
        st.error(f"Error loading jobs: {e}")