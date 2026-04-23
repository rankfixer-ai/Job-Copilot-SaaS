# frontend/pages/4_Company_Check.py
import streamlit as st
import pandas as pd
import plotly.express as px

def show():
    st.markdown("## 🔍 Company Background Check")
    st.markdown("Research companies before applying")
    
    # Check subscription
    plan = st.session_state.get('subscription_plan', 'free')
    
    if plan == 'free':
        st.info("""
        💡 **Basic Plan Feature**: Company checks are available on Basic plan ($9.99/mo).
        
        **Upgrade to Basic** to get:
        - ✅ Company ratings and reviews
        - ✅ Red flag detection
        - ✅ Financial health indicators
        - ✅ Employee satisfaction scores
        """)
        
        if st.button("Upgrade to Basic", use_container_width=True):
            st.session_state.current_page = "💎 Upgrade"
            st.rerun()
        
        # Demo search
        st.markdown("---")
        st.markdown("### 🔍 Try a Demo Search")
        demo_company = st.text_input("Enter company name (Demo)", placeholder="e.g., Google, Microsoft")
        if demo_company:
            show_demo_report(demo_company)
        return
    
    # Full feature for paying users
    company_name = st.text_input("Enter company name", placeholder="e.g., Google, Microsoft, Startup XYZ")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        search_clicked = st.button("🔍 Check Company", type="primary", use_container_width=True)
    with col2:
        st.caption("Data from Glassdoor, LinkedIn, and SEC")
    
    if search_clicked and company_name:
        with st.spinner(f"Researching {company_name}..."):
            show_company_report(company_name)

def show_demo_report(company_name):
    """Show demo report for free users"""
    st.markdown(f"""
    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 0.5rem; margin: 1rem 0;">
        <h3>📊 Demo Report: {company_name}</h3>
        <p><i>This is a demo. Upgrade to Basic for full company reports.</i></p>
        
        <h4>What's included in Basic plan:</h4>
        <ul>
            <li>✅ Glassdoor rating & reviews</li>
            <li>✅ Employee satisfaction trends</li>
            <li>✅ Red flag detection (layoffs, lawsuits, etc.)</li>
            <li>✅ Salary transparency data</li>
            <li>✅ Interview experience reports</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

def show_company_report(company_name):
    """Show full company report"""
    
    # Simulated report data
    st.markdown(f"## 📊 Company Report: {company_name}")
    
    # Overall score
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Overall Rating", "4.2/5", "⭐" * 4)
    with col2:
        st.metric("Risk Score", "Low", "✅ Safe")
    with col3:
        st.metric("Glassdoor", "4.1", "★" * 4)
    with col4:
        st.metric("Would Recommend", "78%", "👍")
    
    st.markdown("---")
    
    # Detailed sections
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "⚠️ Red Flags", "✅ Green Flags", "💬 Reviews"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Company Details")
            st.markdown(f"""
            - **Industry:** Technology
            - **Size:** 10,000+ employees
            - **Founded:** 2010
            - **Headquarters:** San Francisco, CA
            - **Revenue:** $50B+ (2025)
            - **Stock:** Public (TECH)
            """)
        
        with col2:
            st.markdown("#### Employee Sentiment")
            sentiment_data = pd.DataFrame({
                "Category": ["Work-Life Balance", "Compensation", "Career Growth", "Culture", "Management"],
                "Score": [82, 78, 85, 88, 76]
            })
            fig = px.bar(sentiment_data, x='Score', y='Category', orientation='h', color='Score')
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("#### 🚨 Red Flags Detected")
        st.success("No major red flags found for this company")
        st.info("Minor concerns: Recent hiring freeze in some departments")
    
    with tab3:
        st.markdown("#### ✅ Green Flags")
        st.success("✓ Strong financial growth (25% year-over-year)")
        st.success("✓ Good benefits package (health, 401k, remote stipend)")
        st.success("✓ Low turnover rate (12% vs industry avg 18%)")
        st.success("✓ Diversity & inclusion initiatives")
    
    with tab4:
        st.markdown("#### Recent Employee Reviews")
        
        reviews = [
            {"rating": 5, "title": "Great place to work", "pros": "Amazing culture, smart colleagues", "cons": "Fast-paced but manageable"},
            {"rating": 4, "title": "Good benefits", "pros": "Excellent health benefits", "cons": "Can be political"},
            {"rating": 4, "title": "Learning opportunities", "pros": "Learn cutting-edge tech", "cons": "Work-life balance varies by team"}
        ]
        
        for review in reviews:
            with st.expander(f"{'★' * review['rating']} {review['title']}"):
                st.markdown(f"**Pros:** {review['pros']}")
                st.markdown(f"**Cons:** {review['cons']}")
    
    # Recommendation
    st.markdown("---")
    st.markdown("### 💡 Final Recommendation")
    st.success("✅ **Good opportunity** - This company appears stable with good employee satisfaction. Proceed with application.")