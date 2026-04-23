# frontend/pages/2_Cover_Letter.py
import streamlit as st
from datetime import datetime

def show():
    st.markdown("## 📝 AI Cover Letter Generator")
    st.markdown("Generate personalized cover letters in seconds")
    
    # Check subscription
    plan = st.session_state.get('subscription_plan', 'free')
    
    if plan == 'free':
        st.warning("""
        ⚠️ **Free Plan**: Cover letters are not available on Free plan.
        
        **Upgrade to Basic ($9.99/mo)** to get:
        - ✅ 5 cover letters per month
        - ✅ AI-powered personalization
        - ✅ Multiple tone options
        - ✅ Download & save
        """)
        
        if st.button("💎 Upgrade Now", use_container_width=True):
            st.session_state.current_page = "💎 Upgrade"
            st.rerun()
        return
    
    elif plan == 'basic':
        remaining = st.session_state.get('remaining_cover_letters', 5)
        if remaining <= 0:
            st.error("You've used all your cover letters this month. Upgrade to Premium for unlimited!")
            if st.button("Upgrade to Premium"):
                st.session_state.current_page = "💎 Upgrade"
                st.rerun()
            return
        
        st.info(f"📊 You have {remaining} cover letters remaining this month")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Job Details")
        
        # Pre-filled from selected job if available
        selected_job = st.session_state.get('selected_job', {})
        
        job_title = st.text_input("Job Title*", value=selected_job.get('title', ''))
        company_name = st.text_input("Company Name*", value=selected_job.get('employer_name', ''))
        job_description = st.text_area("Job Description*", height=200, 
                                      value=selected_job.get('description_preview', ''))
        
        tone = st.selectbox("Tone", ["Professional", "Enthusiastic", "Confident", "Concise", "Creative"])
        
        with st.expander("📎 Additional Information (Optional)"):
            achievements = st.text_area("Key Achievements", height=100,
                                       placeholder="• Led team of 10\n• Increased sales by 30%\n• Saved $50k annually")
            referral = st.text_input("Referral Name (if any)")
            portfolio = st.text_input("Portfolio/Website URL (optional)")
    
    with col2:
        st.markdown("### 📄 Cover Letter Preview")
        st.markdown("---")
        
        if st.button("✨ Generate Cover Letter", type="primary", use_container_width=True):
            if job_title and company_name and job_description:
                with st.spinner("AI writing your cover letter..."):
                    # AI generation logic
                    cover_letter = generate_cover_letter(
                        job_title, company_name, job_description, tone,
                        st.session_state.get('user_name', 'Candidate'),
                        achievements
                    )
                    st.session_state.generated_letter = cover_letter
                    st.success("Cover letter generated successfully!")
                    
                    # Decrement counter for basic plan
                    if plan == 'basic':
                        st.session_state.remaining_cover_letters = remaining - 1
            else:
                st.error("Please fill in all required fields (*)")
        
        if 'generated_letter' in st.session_state:
            st.text_area("Your Cover Letter", st.session_state.generated_letter, height=400)
            
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                if st.button("📋 Copy", use_container_width=True):
                    st.toast("Copied to clipboard!")
            with col_b:
                if st.button("💾 Save", use_container_width=True):
                    filename = f"cover_letter_{job_title}_{datetime.now().strftime('%Y%m%d')}.txt"
                    st.download_button(
                        label="📥 Download",
                        data=st.session_state.generated_letter,
                        file_name=filename,
                        mime="text/plain"
                    )
            with col_c:
                if st.button("🔄 Regenerate", use_container_width=True):
                    del st.session_state.generated_letter
                    st.rerun()

def generate_cover_letter(title, company, description, tone, name, achievements):
    """Generate cover letter using AI (simulated for now)"""
    
    tone_adjectives = {
        "Professional": "professional and polished",
        "Enthusiastic": "energetic and passionate",
        "Confident": "confident and assertive",
        "Concise": "brief and impactful",
        "Creative": "creative and memorable"
    }
    
    # Simulated AI generation
    letter = f"""
Dear Hiring Manager,

I am excited to apply for the {title} position at {company}. With my background and skills, I am confident I can contribute significantly to your team's success.

{achievements if achievements else "Throughout my career, I have developed strong skills in project management, communication, and problem-solving. I take pride in delivering results and exceeding expectations."}

The opportunity at {company} particularly appeals to me because it aligns with my professional goals and values. I am eager to bring my expertise to your organization.

Thank you for considering my application. I look forward to discussing how I can contribute to {company}'s continued success.

Best regards,
{name}
"""
    return letter