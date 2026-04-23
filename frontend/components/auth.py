# frontend/components/auth.py
import streamlit as st
import requests
from datetime import datetime, timedelta
import json
import os

# API configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api")

class AuthComponent:
    """Handles user authentication and session management"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def login_page(self):
        """Display login form"""
        st.markdown('<div class="main-title">🎯 Job Copilot</div>', unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #666;'>Your AI-Powered Job Search Assistant</p>", unsafe_allow_html=True)
        
        st.markdown("---")
        
        tab1, tab2 = st.tabs(["🔐 Login", "📝 Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email", key="login_email")
                password = st.text_input("Password", type="password", key="login_password")
                remember_me = st.checkbox("Remember me")
                
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    if email and password:
                        success, result = self.authenticate(email, password)
                        if success:
                            st.session_state.logged_in = True
                            st.session_state.user_email = email
                            st.session_state.user_name = result.get('name', email.split('@')[0])
                            st.session_state.token = result.get('token')
                            st.session_state.subscription_plan = result.get('plan', 'free')
                            st.session_state.remaining_cover_letters = result.get('remaining_cover_letters', 0)
                            st.rerun()
                        else:
                            st.error(result)
                    else:
                        st.error("Please enter email and password")
        
        with tab2:
            with st.form("register_form"):
                name = st.text_input("Full Name", key="reg_name")
                email = st.text_input("Email", key="reg_email")
                password = st.text_input("Password", type="password", key="reg_password")
                confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
                
                submitted = st.form_submit_button("Register", use_container_width=True)
                
                if submitted:
                    if password != confirm:
                        st.error("Passwords don't match")
                    elif email and password:
                        success, result = self.register(name, email, password)
                        if success:
                            st.success("Registration successful! Please login.")
                        else:
                            st.error(result)
                    else:
                        st.error("Please fill all fields")
        
        # Demo mode note
        st.markdown("---")
        st.info("💡 **Demo Mode**: Click Login with any email/password to try the app")
    
    def authenticate(self, email, password):
        """Authenticate user with backend"""
        try:
            # For demo mode - accept any credentials
            # Replace with real API call when backend is ready
            if "@" in email and password:
                return True, {
                    'name': email.split('@')[0],
                    'token': 'demo_token_' + email,
                    'plan': 'free',
                    'remaining_cover_letters': 0
                }
            
            # Real API call (commented for now)
            # response = self.session.post(f"{API_BASE_URL}/auth/login", json={
            #     "email": email,
            #     "password": password
            # })
            # if response.status_code == 200:
            #     data = response.json()
            #     return True, data
            # return False, response.json().get('error', 'Login failed')
            
            return False, "Invalid credentials"
        except Exception as e:
            return False, str(e)
    
    def register(self, name, email, password):
        """Register new user"""
        try:
            # For demo mode - always succeed
            return True, "Registration successful"
            
            # Real API call
            # response = self.session.post(f"{API_BASE_URL}/auth/register", json={
            #     "name": name,
            #     "email": email,
            #     "password": password
            # })
            # if response.status_code == 201:
            #     return True, "Registration successful"
            # return False, response.json().get('error', 'Registration failed')
        except Exception as e:
            return False, str(e)
    
    def logout(self):
        """Clear session and logout"""
        for key in ['logged_in', 'user_email', 'user_name', 'token', 'subscription_plan', 'remaining_cover_letters']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
    
    def check_feature_access(self, feature_name):
        """Check if user can access a premium feature"""
        plan = st.session_state.get('subscription_plan', 'free')
        
        features = {
            'cover_letter': {'free': False, 'basic': True, 'premium': True},
            'interview_prep': {'free': False, 'basic': False, 'premium': True},
            'company_check': {'free': False, 'basic': True, 'premium': True},
            'resume_analysis': {'free': False, 'basic': True, 'premium': True}
        }
        
        return features.get(feature_name, {}).get(plan, False)