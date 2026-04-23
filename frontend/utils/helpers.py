# frontend/utils/helpers.py
import re
import pandas as pd
from datetime import datetime, timedelta

def extract_salary(salary_str):
    """Extract hourly rate from salary string"""
    if pd.isna(salary_str):
        return None
    
    # Hourly: $6-9/hr, $8-$15/hr, $6 an Hour
    match = re.search(r'\$?(\d+(?:\.\d+)?)\s*[-/]?\s*(?:hr|hour)', str(salary_str), re.I)
    if match:
        return float(match.group(1))
    
    # Monthly: $300/Month
    match = re.search(r'\$(\d+(?:,\d+)?)\s*/?\s*(?:mo|month)', str(salary_str), re.I)
    if match:
        monthly = float(match.group(1).replace(',', ''))
        return round(monthly / 160, 2)
    
    return None

def calculate_match_percentage(user_skills, job_skills):
    """Calculate skill match percentage"""
    if not job_skills:
        return 0
    
    user_set = set([s.lower().strip() for s in user_skills])
    job_set = set([s.lower().strip() for s in job_skills])
    
    if not job_set:
        return 0
    
    matches = len(user_set & job_set)
    return round((matches / len(job_set)) * 100, 2)

def format_date(date_string):
    """Format date for display"""
    try:
        date_obj = pd.to_datetime(date_string)
        now = datetime.now()
        
        if date_obj.date() == now.date():
            return "Today"
        elif date_obj.date() == (now - timedelta(days=1)).date():
            return "Yesterday"
        else:
            return date_obj.strftime("%b %d, %Y")
    except:
        return date_string

def truncate_text(text, max_length=100):
    """Truncate long text"""
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def generate_skill_tags(skills_list):
    """Generate HTML for skill tags"""
    html = ""
    for skill in skills_list[:5]:
        html += f'<span style="background: #e0e0e0; padding: 2px 8px; border-radius: 12px; font-size: 12px; margin: 2px;">{skill}</span> '
    return html

def parse_job_type(job_type_string):
    """Standardize job type"""
    job_type_string = str(job_type_string).lower()
    if 'full' in job_type_string:
        return "Full Time"
    elif 'part' in job_type_string:
        return "Part Time"
    elif 'contract' in job_type_string:
        return "Contract"
    else:
        return "Other"

def get_salary_color(salary_value):
    """Get color for salary display"""
    if not salary_value:
        return "gray"
    elif salary_value >= 25:
        return "green"
    elif salary_value >= 15:
        return "orange"
    else:
        return "red"

def validate_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def generate_daily_report(jobs_df):
    """Generate daily job report summary"""
    if jobs_df.empty:
        return "No jobs found today."
    
    report = f"""
    📊 Daily Job Report - {datetime.now().strftime('%Y-%m-%d')}
    
    Total Jobs: {len(jobs_df)}
    Full Time: {len(jobs_df[jobs_df['job_type'] == 'Full Time'])}
    Part Time: {len(jobs_df[jobs_df['job_type'] == 'Part Time'])}
    
    Average Salary: ${jobs_df['salary_preview'].apply(extract_salary).mean():.2f}/hr
    
    Top Skills:
    """
    
    # Extract top skills
    all_skills = []
    for tags in jobs_df['tags'].dropna():
        all_skills.extend(str(tags).split(', '))
    
    from collections import Counter
    top_skills = Counter(all_skills).most_common(5)
    
    for skill, count in top_skills:
        report += f"\n  - {skill}: {count} jobs"
    
    return report

def session_timeout_check():
    """Check if session has expired"""
    if 'last_activity' in st.session_state:
        last = st.session_state.last_activity
        if datetime.now() - last > timedelta(hours=24):
            # Session expired
            for key in ['logged_in', 'user_email', 'token']:
                if key in st.session_state:
                    del st.session_state[key]
            return True
    st.session_state.last_activity = datetime.now()
    return False