# frontend/components/sidebar.py
import streamlit as st
from datetime import datetime

def render_sidebar():
    """Render the navigation sidebar with user info"""
    
    with st.sidebar:
        # Logo and user section
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="margin: 0;">🎯 Job Copilot</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # User profile section
        st.markdown(f"""
        <div style="text-align: center; margin: 1rem 0;">
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        width: 60px; height: 60px; border-radius: 50%; 
                        display: flex; align-items: center; justify-content: center;
                        margin: 0 auto; color: white; font-size: 24px;">
                {st.session_state.get('user_name', 'U')[0].upper()}
            </div>
            <h4 style="margin: 0.5rem 0 0 0;">{st.session_state.get('user_name', 'User')}</h4>
            <p style="color: #666; font-size: 12px; margin: 0;">{st.session_state.get('user_email', '')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Subscription badge
        plan = st.session_state.get('subscription_plan', 'free')
        plan_colors = {
            'free': ('#f0f0f0', '#333', '📋 FREE'),
            'basic': ('#667eea', 'white', '💎 BASIC'),
            'premium': ('linear-gradient(135deg, #FFD700, #FFA500)', 'white', '⭐ PREMIUM')
        }
        bg, color, text = plan_colors.get(plan, plan_colors['free'])
        
        st.markdown(f"""
        <div style="background: {bg}; padding: 0.5rem; border-radius: 0.5rem; 
                    text-align: center; margin: 0.5rem 0; color: {color};">
            <b>{text}</b>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation menu
        st.markdown("### 📍 Navigation")
        
        menu_items = {
            "🏠 Dashboard": "dashboard",
            "🎯 Job Matches": "job_matches",
            "📝 Cover Letter": "cover_letter",
            "🎤 Interview Prep": "interview_prep",
            "🔍 Company Check": "company_check",
            "👤 My Profile": "profile",
            "💎 Upgrade": "upgrade"
        }
        
        # Store current page in session state
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "🏠 Dashboard"
        
        for label, page_key in menu_items.items():
            if st.button(label, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = label
                st.rerun()
        
        st.markdown("---")
        
        # Statistics section
        st.markdown("### 📊 Your Activity")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Jobs Viewed", "47", "+12")
        with col2:
            st.metric("Applications", "12", "+3")
        
        # Daily limit info (for free tier)
        if plan == 'free':
            st.info("💡 Upgrade to Basic for unlimited matches")
        
        # Profile completion
        st.markdown("### 📈 Profile")
        st.progress(0.65, text="65% Complete")
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            from components.auth import AuthComponent
            auth = AuthComponent()
            auth.logout()
    
    return st.session_state.current_page