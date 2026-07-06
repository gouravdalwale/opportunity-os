import streamlit as st
from utils.security import contains_prompt_injection

from orchestrator import OpportunityOS

# --------------------------------------------
# PAGE CONFIG
# --------------------------------------------

st.set_page_config(
    page_title="Opportunity OS",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------
# CUSTOM CSS
# --------------------------------------------

st.markdown("""
<style>

.main{
    padding-top:1rem;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.card{
    background:#f8f9fa;
    border-radius:15px;
    padding:18px;
    margin-bottom:15px;
    border-left:6px solid #4CAF50;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
}

.summary-card{
    background:#eef6ff;
    border-radius:15px;
    padding:20px;
    text-align:center;
    box-shadow:0 3px 8px rgba(0,0,0,0.08);
}

.footer{
    text-align:center;
    color:gray;
    padding:30px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------
# SIDEBAR
# --------------------------------------------

with st.sidebar:

    st.title("🚀 Opportunity OS")

    st.success("Version 2.0")

    st.divider()

    st.subheader("🤖 AI Agents")

    st.markdown("""
- 👤 Profile Agent
- 🎯 Opportunity Agent
- 🗺 Roadmap Agent
""")

    st.divider()

    st.subheader("🌍 Supports")

    st.markdown("""
✅ Engineering

✅ Medical

✅ Business

✅ Design

✅ Law

✅ Research

✅ Entrepreneurship

✅ Arts
""")

    st.divider()

    st.info(
        "💡 Fill your profile accurately for highly personalized recommendations."
    )

# --------------------------------------------
# HEADER
# --------------------------------------------

st.title("🚀 Opportunity OS")

st.markdown(
"""
### AI-Powered Career Intelligence Platform

Opportunity OS uses a **multi-agent AI system**
to understand your profile,
recommend opportunities,
and generate a personalized career roadmap.

Built for students,
professionals,
researchers,
entrepreneurs,
designers,
and innovators.
"""
)

st.divider()

# --------------------------------------------
# DASHBOARD METRICS
# --------------------------------------------

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("🤖 AI Agents", "3")

with m2:
    st.metric("🎯 Opportunity Types", "15+")

with m3:
    st.metric("🌍 Domains", "Any")

with m4:
    st.metric("🗓 Roadmap", "30 Days")

st.divider()

# --------------------------------------------
# FEATURES
# --------------------------------------------

st.subheader("✨ What Opportunity OS Can Discover")

c1, c2, c3 = st.columns(3)

with c1:

    st.success("💼 Internships")

    st.success("🏆 Competitions")

    st.success("🎓 Fellowships")

with c2:

    st.success("🌍 Open Source")

    st.success("🔬 Research")

    st.success("📜 Certifications")

with c3:

    st.success("🚀 Startup Programs")

    st.success("💰 Grants")

    st.success("🤝 Communities")

st.divider()

# --------------------------------------------
# USER PROFILE
# --------------------------------------------

st.header("👤 Build Your Profile")

col1, col2 = st.columns(2)

with col1:

    education = st.text_input(
        "🎓 Education / Profession",
        placeholder="B.Tech Mechanical Engineering"
    )

    skills = st.text_area(
        "🛠 Skills",
        placeholder="Python, CAD, SolidWorks..."
    )

    interests = st.text_area(
        "❤️ Interests",
        placeholder="Robotics, AI, Manufacturing..."
    )

with col2:

    goal = st.text_input(
        "🎯 Career Goal",
        placeholder="Core Internship"
    )

    experience = st.selectbox(
        "🚀 Experience Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )

    domain = st.selectbox(
        "🌍 Preferred Domain",
        [
            "Technology",
            "Mechanical",
            "Civil",
            "Medical",
            "Business",
            "Design",
            "Research",
            "Law",
            "Entrepreneurship",
            "Other"
        ]
    )

# Combine profile

user_profile = f"""
Education:
{education}

Experience:
{experience}

Preferred Domain:
{domain}

Skills:
{skills}

Interests:
{interests}

Career Goal:
{goal}
"""

st.divider()

# --------------------------------------------
# AI PIPELINE
# --------------------------------------------

st.header("🤖 Multi-Agent Pipeline")

p1, p2, p3 = st.columns(3)

with p1:
    st.success("👤 Profile Agent")

with p2:
    st.success("🎯 Opportunity Agent")

with p3:
    st.success("🗺 Roadmap Agent")

st.caption(
    "The agents work together to analyze your profile, recommend opportunities, and generate a personalized roadmap."
)

st.divider()

# --------------------------------------------
# BUTTON
# --------------------------------------------

analyze = st.button(
    "🚀 Analyze My Career",
    use_container_width=True
)
# --------------------------------------------
# AI EXECUTION
# --------------------------------------------

if analyze:

    required_fields = [
    education,
    experience,
    domain,
    skills,
    interests,
    goal,
    ]   

    if any(not field.strip() for field in required_fields):
        st.warning("⚠ Please complete your profile before continuing.")
        st.stop()


    if len(user_profile) > 5000:
        st.error("⚠ Profile is too long. Please reduce the content.")
        st.stop()
    # ----------------------------------------
# Security: Prompt Injection Protection
# ----------------------------------------

    if contains_prompt_injection(user_profile):
        st.error("⚠ Potential prompt injection detected. Please remove malicious instructions.")
        st.stop()

    progress = st.progress(0)

    status = st.empty()

    # ----------------------------------------

    status.info("🤖 Opportunity OS Orchestrator is coordinating AI agents...")

    progress.progress(20)

    orchestrator = OpportunityOS()

    results = orchestrator.run(user_profile)

    profile = results["profile_analysis"]

    progress.progress(60)

    opportunities = results["opportunities"]

    progress.progress(85)

    roadmap = results["roadmap"]

    progress.progress(100)

    status.success("✅ Analysis Completed Successfully!")

    st.balloons()

    st.divider()

    # --------------------------------------------
    # EXECUTIVE DASHBOARD
    # --------------------------------------------

    st.header("📊 Executive Dashboard")

    d1, d2, d3, d4 = st.columns(4)

    with d1:
        st.metric(
            "Career Readiness",
            "AI Generated"
        )

    with d2:
        st.metric(
            "Profile Status",
            "Complete"
        )

    with d3:
        st.metric(
            "AI Agents Used",
            "3"
        )

    with d4:
        st.metric(
            "Roadmap",
            "30 Days"
        )

    st.divider()

    # --------------------------------------------
    # TABS
    # --------------------------------------------

    # --------------------------------------------
    # TABS
    # --------------------------------------------

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "📋 Dashboard",
            "👤 Profile",
            "🎯 Opportunities",
            "🗺 Roadmap",
        ]
    )

    # ============================================

    with tab1:

        st.subheader("🚀 Career Summary")

        st.success(
            "Your profile has been analyzed successfully by all three AI agents."
        )

        c1, c2 = st.columns(2)

        with c1:

            st.info(
                """
### 🤖 AI Workflow

✅ Profile Analysis

✅ Opportunity Discovery

✅ Roadmap Generation
"""
            )

        with c2:

            st.info(
                """
### 📌 Report Generated

✔ Personalized

✔ AI Powered

✔ Career Focused
"""
            )

        st.divider()

        st.markdown(
            """
### 🎯 What's Next?

Explore the tabs above to:

- Understand your profile

- Discover opportunities

- Follow your personalized roadmap
"""
        )

    # ============================================

    with tab2:

        st.subheader("👤 Profile Analysis")

        st.markdown(profile)
    # ============================================

    with tab3:

        st.subheader("🎯 Opportunity Recommendations")

        st.markdown(opportunities)

# ============================================

    with tab4:

        st.subheader("🗺️ 30-Day Career Roadmap")

        st.markdown(roadmap)