# frontend/utils/api_client.py
import requests
import streamlit as st
import os

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

class APIClient:
    """Handle all backend API calls"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_headers(self):
        """Get authorization headers"""
        headers = {'Content-Type': 'application/json'}
        if 'token' in st.session_state:
            headers['Authorization'] = f"Bearer {st.session_state.token}"
        return headers
    
    # ============= AUTH ENDPOINTS =============
    def login(self, email, password):
        response = self.session.post(
            f"{API_BASE_URL}/auth/login",
            json={"email": email, "password": password}
        )
        return response.json()
    
    def register(self, name, email, password):
        response = self.session.post(
            f"{API_BASE_URL}/auth/register",
            json={"name": name, "email": email, "password": password}
        )
        return response.json()
    
    # ============= USER ENDPOINTS =============
    def get_profile(self):
        response = self.session.get(
            f"{API_BASE_URL}/user/profile",
            headers=self.get_headers()
        )
        return response.json()
    
    def update_profile(self, profile_data):
        response = self.session.post(
            f"{API_BASE_URL}/user/profile",
            json=profile_data,
            headers=self.get_headers()
        )
        return response.json()
    
    def upload_resume(self, file):
        files = {'resume': file}
        response = self.session.post(
            f"{API_BASE_URL}/user/resume",
            files=files,
            headers={'Authorization': f"Bearer {st.session_state.token}"}
        )
        return response.json()
    
    # ============= JOBS ENDPOINTS =============
    def get_job_matches(self, limit=20, offset=0):
        response = self.session.get(
            f"{API_BASE_URL}/jobs/matches",
            params={"limit": limit, "offset": offset},
            headers=self.get_headers()
        )
        return response.json()
    
    def get_job_details(self, job_id):
        response = self.session.get(
            f"{API_BASE_URL}/jobs/{job_id}",
            headers=self.get_headers()
        )
        return response.json()
    
    def save_job(self, job_id):
        response = self.session.post(
            f"{API_BASE_URL}/jobs/{job_id}/save",
            headers=self.get_headers()
        )
        return response.json()
    
    # ============= COVER LETTER ENDPOINTS =============
    def generate_cover_letter(self, job_id, tone="professional"):
        response = self.session.post(
            f"{API_BASE_URL}/cover-letter/generate",
            json={"job_id": job_id, "tone": tone},
            headers=self.get_headers()
        )
        return response.json()
    
    # ============= INTERVIEW PREP ENDPOINTS =============
    def get_interview_questions(self, job_id):
        response = self.session.post(
            f"{API_BASE_URL}/interview/questions",
            json={"job_id": job_id},
            headers=self.get_headers()
        )
        return response.json()
    
    def evaluate_answer(self, question, answer):
        response = self.session.post(
            f"{API_BASE_URL}/interview/evaluate",
            json={"question": question, "answer": answer},
            headers=self.get_headers()
        )
        return response.json()
    
    # ============= COMPANY CHECK ENDPOINTS =============
    def check_company(self, company_name):
        response = self.session.get(
            f"{API_BASE_URL}/company/check/{company_name}",
            headers=self.get_headers()
        )
        return response.json()
    
    # ============= SUBSCRIPTION ENDPOINTS =============
    def get_subscription_info(self):
        response = self.session.get(
            f"{API_BASE_URL}/subscription/info",
            headers=self.get_headers()
        )
        return response.json()
    
    def create_checkout_session(self, plan):
        response = self.session.post(
            f"{API_BASE_URL}/subscription/checkout",
            json={"plan": plan},
            headers=self.get_headers()
        )
        return response.json()