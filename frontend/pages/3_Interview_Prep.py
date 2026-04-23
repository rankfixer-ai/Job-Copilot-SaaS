# frontend/pages/3_Interview_Prep.py
import streamlit as st
import random

def show():
    st.markdown("## 🎤 AI Interview Preparation")
    st.markdown("Practice with AI-generated questions tailored to your job")
    
    # Check subscription
    plan = st.session_state.get('subscription_plan', 'free')
    
    if plan != 'premium':
        st.warning("""
        ⭐ **Premium Feature**: Interview preparation is available on Premium plan.
        
        **Upgrade to Premium ($29.99/mo)** to get:
        - ✅ AI-generated questions based on job description
        - ✅ Mock interview simulator
        - ✅ Real-time answer feedback
        - ✅ Personalized improvement suggestions
        - ✅ Sample answers from industry experts
        """)
        
        if st.button("👑 Upgrade to Premium", use_container_width=True):
            st.session_state.current_page = "💎 Upgrade"
            st.rerun()
        
        # Show demo
        with st.expander("🔍 See what Premium includes (Preview)"):
            st.markdown("""
            **Sample Interview Questions for Project Manager:**
            
            1. How do you handle scope creep in a project?
            2. Describe a time you had to manage a difficult stakeholder.
            3. What project management methodologies are you familiar with?
            4. How do you prioritize tasks when everything is urgent?
            5. Tell me about a project that failed and what you learned.
            """)
        return
    
    # Premium content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Job Information")
        job_role = st.text_input("Job Role*", placeholder="e.g., Project Manager, Software Engineer")
        company = st.text_input("Company (Optional)")
        experience_level = st.selectbox("Experience Level", ["Entry", "Mid-Level", "Senior", "Lead"])
        
        interview_type = st.radio("Interview Type", ["Technical", "Behavioral", "Mixed"], horizontal=True)
        
        if st.button("🎯 Generate Questions", type="primary", use_container_width=True):
            if job_role:
                with st.spinner("AI generating interview questions..."):
                    questions = generate_interview_questions(job_role, interview_type, experience_level)
                    st.session_state.questions = questions
                    st.success(f"Generated {len(questions)} questions!")
            else:
                st.error("Please enter a job role")
    
    with col2:
        if 'questions' in st.session_state:
            st.markdown("### 📝 Generated Questions")
            
            for i, q in enumerate(st.session_state.questions, 1):
                with st.expander(f"Question {i}"):
                    st.write(q)
                    if st.button(f"Practice This Question", key=f"practice_{i}"):
                        st.session_state.current_question = q
                        st.session_state.practice_mode = True
    
    # Practice area
    if st.session_state.get('practice_mode', False):
        st.markdown("---")
        st.markdown("### 🎙️ Practice Your Answer")
        
        st.info(f"**Current Question:** {st.session_state.current_question}")
        
        user_answer = st.text_area("Your Answer", height=150, 
                                   placeholder="Type your answer here...")
        
        if st.button("Get AI Feedback", type="primary"):
            if user_answer:
                with st.spinner("Analyzing your answer..."):
                    feedback = get_answer_feedback(st.session_state.current_question, user_answer)
                    
                    st.markdown("### 🤖 AI Feedback")
                    
                    col_f1, col_f2, col_f3 = st.columns(3)
                    with col_f1:
                        st.metric("Clarity", feedback['clarity'], "85%")
                    with col_f2:
                        st.metric("Relevance", feedback['relevance'], "78%")
                    with col_f3:
                        st.metric("Structure", feedback['structure'], "82%")
                    
                    st.markdown(f"**Strengths:** {feedback['strengths']}")
                    st.markdown(f"**Improvements:** {feedback['improvements']}")
                    
                    with st.expander("💡 Sample Answer"):
                        st.write(feedback['sample_answer'])
            else:
                st.error("Please write your answer first")
        
        if st.button("Next Question"):
            st.session_state.practice_mode = False
            st.rerun()

def generate_interview_questions(role, interview_type, level):
    """Generate interview questions based on role"""
    
    # Sample questions database
    questions_db = {
        "Project Manager": {
            "technical": [
                "How do you handle scope creep in a project?",
                "Describe your experience with Agile vs Waterfall methodologies.",
                "What tools do you use for project tracking and why?",
                "How do you manage risk in a project?",
                "How do you calculate project ROI?"
            ],
            "behavioral": [
                "Tell me about a time you had to manage a difficult stakeholder.",
                "How do you prioritize when everything is urgent?",
                "Describe a project that failed and what you learned.",
                "How do you motivate underperforming team members?",
                "Tell me about a time you had to make a tough decision."
            ]
        },
        "Software Engineer": {
            "technical": [
                "Explain the difference between REST and GraphQL.",
                "How do you handle database optimization?",
                "Describe your experience with CI/CD pipelines.",
                "What's your approach to debugging complex issues?",
                "How do you ensure code quality?"
            ],
            "behavioral": [
                "Tell me about a challenging bug you solved.",
                "How do you handle technical debt?",
                "Describe a time you disagreed with a technical decision.",
                "How do you stay updated with new technologies?",
                "Tell me about a project you're proud of."
            ]
        }
    }
    
    # Get questions for role or use generic
    role_questions = questions_db.get(role, questions_db["Project Manager"])
    
    if interview_type == "technical":
        return role_questions["technical"][:5]
    elif interview_type == "behavioral":
        return role_questions["behavioral"][:5]
    else:  # mixed
        mixed = []
        for i in range(3):
            mixed.append(role_questions["technical"][i])
            mixed.append(role_questions["behavioral"][i])
        return mixed[:6]

def get_answer_feedback(question, answer):
    """Provide feedback on user's answer"""
    
    # Simple feedback generation (will be replaced with AI)
    feedback = {
        "clarity": random.randint(70, 95),
        "relevance": random.randint(65, 90),
        "structure": random.randint(75, 92),
        "strengths": "Good use of examples and clear communication.",
        "improvements": "Could add more specific metrics and results.",
        "sample_answer": "Here's a stronger answer: I would start by... [sample answer]"
    }
    
    return feedback