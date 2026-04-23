# adzuna_client.py
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class AdzunaClient:
    def __init__(self):
        self.app_id = os.getenv('ADZUNA_APP_ID')
        self.app_key = os.getenv('ADZUNA_APP_KEY')
        self.country = os.getenv('ADZUNA_COUNTRY', 'us')
        self.base_url = f"https://api.adzuna.com/v1/api/jobs/{self.country}/search/1"
    
    def search_jobs(self, what, where='', results_per_page=25):
        """Search for jobs using Adzuna API"""
        
        params = {
            'app_id': self.app_id,
            'app_key': self.app_key,
            'results_per_page': results_per_page,
            'what': what,
            'where': where,
            'content-type': 'application/json',
            'sort_by': 'date'
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data:
                return self.format_jobs(data['results'])
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return []
    
    def format_jobs(self, raw_jobs):
        """Format Adzuna jobs to match your app's expected structure"""
        formatted = []
        
        for job in raw_jobs:
            formatted.append({
                'title': job.get('title', 'Untitled'),
                'salary_preview': self.format_salary(job),
                'job_type': self.get_job_type(job),
                'tags': self.extract_skills(job),
                'url': job.get('redirect_url', ''),
                'date_posted': job.get('created', datetime.now().isoformat()),
                'company': job.get('company', {}).get('display_name', 'Unknown'),
                'location': job.get('location', {}).get('display_name', 'Remote'),
                'description': job.get('description', 'No description available'),
                'adzuna_id': job.get('id', '')
            })
        
        return formatted
    
    def format_salary(self, job):
        """Format salary information"""
        salary_min = job.get('salary_min')
        salary_max = job.get('salary_max')
        
        if salary_min and salary_max:
            return f"${int(salary_min):,}-${int(salary_max):,}"
        elif salary_min:
            return f"From ${int(salary_min):,}"
        else:
            return "Not specified"
    
    def get_job_type(self, job):
        """Extract job type"""
        contract = job.get('contract_type', '')
        if contract:
            return contract
        description = job.get('description', '').lower()
        if 'part time' in description or 'part-time' in description:
            return 'Part Time'
        elif 'contract' in description:
            return 'Contract'
        else:
            return 'Full Time'
    
    def extract_skills(self, job):
        """Extract key skills from job"""
        title = job.get('title', '').lower()
        description = job.get('description', '').lower()
        
        common_skills = [
            'python', 'javascript', 'sql', 'java', 'react', 'angular',
            'project management', 'agile', 'scrum', 'leadership', 'communication',
            'excel', 'data analysis', 'machine learning', 'aws', 'docker'
        ]
        
        found_skills = []
        for skill in common_skills:
            if skill in title or skill in description:
                found_skills.append(skill.title())
        
        return ', '.join(found_skills[:5]) if found_skills else 'Various Skills'

# Create a global instance
adzuna = AdzunaClient()