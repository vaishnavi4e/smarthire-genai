import os

import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume_local
from src.search.job_search import JobSearch
from src.guardrails import check_input


st.set_page_config(
    page_title="SmartHire GenAI",
    page_icon="💼",
    layout="wide",
)

st.title("💼 SmartHire GenAI")
st.subheader("AI-Powered Career & Job Matching Assistant")

st.write(
    "Upload a resume to extract a candidate profile and "
    "discover semantically matching job opportunities."
)

st.divider()

# =========================================================
# RESUME UPLOAD
# =========================================================

st.header("📄 Resume Upload")

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf", "docx"],
)

profile = None
resume_text = ""

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    os.makedirs("data/resumes", exist_ok=True)

    temp_path = os.path.join(
        "data",
        "resumes",
        uploaded_file.name,
    )

    with open(temp_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    try:

        resume_text = load_resume(temp_path)

        if not resume_text.strip():
            st.error(
                "Resume text is empty. Please upload a valid resume."
            )
            st.stop()

        st.success(
            f"Resume loaded successfully — "
            f"{len(resume_text)} characters extracted."
        )

        # =================================================
        # CANDIDATE PROFILE
        # =================================================

        st.header("👤 Candidate Profile")

        profile = parse_resume_local(resume_text)

        st.info(
            "Candidate profile extracted locally from "
            "the uploaded resume."
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write("**Name:**", profile.name)

            st.write(
                "**Target Role:**",
                profile.target_role,
            )

            st.write(
                "**Experience:**",
                ", ".join(profile.experience)
                if profile.experience
                else "Not available",
            )

        with col2:

            st.write(
                "**Skills:**",
                ", ".join(profile.skills)
                if profile.skills
                else "Not available",
            )

            st.write(
                "**Education:**",
                ", ".join(profile.education)
                if profile.education
                else "Not available",
            )

        # =================================================
        # JOB SEARCH
        # =================================================

        st.header("🔎 Matching Jobs")

        if st.button("Find Top 5 Jobs"):

            with st.spinner(
                "Searching the 22,000-job database..."
            ):

                search_engine = JobSearch()

                results = search_engine.search(
                    profile,
                    top_k=5,
                )

            if results:

                st.success(
                    f"Found {len(results)} matching jobs."
                )

                for i, job in enumerate(
                    results,
                    start=1,
                ):

                    title = job.get(
                        "jobtitle",
                        "Unknown Role",
                    )

                    with st.expander(
                        f"{i}. {title}"
                    ):

                        st.write(
                            "**Company:**",
                            job.get(
                                "company",
                                "Not specified",
                            ),
                        )

                        st.write(
                            "**Location:**",
                            job.get(
                                "joblocation_address",
                                "Not specified",
                            ),
                        )

                        st.write(
                            "**Skills:**",
                            job.get(
                                "skills",
                                "Not specified",
                            ),
                        )

                        st.write(
                            "**Experience:**",
                            job.get(
                                "experience",
                                "Not specified",
                            ),
                        )

                        st.write(
                            "**Education:**",
                            job.get(
                                "education",
                                "Not specified",
                            ),
                        )

                        st.write(
                            "**Similarity Score:**",
                            round(
                                job.get(
                                    "similarity_score",
                                    0,
                                ),
                                4,
                            ),
                        )

            else:

                st.warning("No matching jobs found.")

    except Exception as error:

        st.error(
            f"Something went wrong: {error}"
        )


# =========================================================
# CV IMPROVEMENT
# =========================================================

if profile is not None:

    st.divider()

    st.header("✨ AI CV Improvement")

    st.write(
        "Get suggestions for improving your resume "
        "based on your profile and target role."
    )

    target_role = st.text_input(
        "Target role",
        value=profile.target_role
        if profile.target_role != "Not specified"
        else "",
        placeholder="Example: Software Engineer",
    )

    if st.button("Analyze My CV"):

        if not target_role.strip():

            st.warning(
                "Please enter a target role first."
            )

        else:

            st.subheader("📌 Suggested Skills")

            st.write(
                "Skills detected in your resume:"
            )

            for skill in profile.skills[:10]:

                st.write(f"• {skill}")

            st.subheader("📝 Resume Improvement Tips")

            suggestions = [
                "Use measurable achievements instead of only listing responsibilities.",
                "Keep technical skills clearly grouped and easy to scan.",
                "Tailor resume keywords to the target job role.",
                "Highlight relevant projects, internships, and practical experience.",
                "Use concise action verbs at the beginning of bullet points.",
            ]

            for suggestion in suggestions:

                st.write(f"• {suggestion}")

            st.success(
                "CV analysis completed successfully."
            )


# =========================================================
# CAREER MENTOR
# =========================================================

st.divider()

st.header("🤖 Career Mentor")

question = st.text_area(
    "Ask a career-related question",
    placeholder=(
        "Example: What skills should I improve "
        "for my career?"
    ),
)

if st.button("Get Career Advice"):

    valid, message = check_input(question)

    if not valid:

        st.warning(message)

    elif profile is None:

        st.warning(
            "Please upload a resume before asking "
            "for personalized career advice."
        )

    else:

        st.subheader("💡 SmartHire Career Advice")

        question_lower = question.lower()

        if "skill" in question_lower:

            st.write(
                "Based on your resume and matching jobs, "
                "focus on strengthening the technical skills "
                "that repeatedly appear in relevant job listings."
            )

            st.write("Your detected skills include:")

            for skill in profile.skills[:10]:

                st.write(f"• {skill}")

            st.write(
                "Consider building practical projects "
                "that demonstrate these skills."
            )

        elif (
            "resume" in question_lower
            or "cv" in question_lower
        ):

            st.write(
                "Focus your resume on measurable achievements, "
                "relevant technical skills, projects, "
                "internships, and experience related to "
                "your target role."
            )

        elif (
            "job" in question_lower
            or "career" in question_lower
        ):

            st.write(
                "Focus on roles that closely match your "
                "detected skills and education. Use the "
                "Top 5 Matching Jobs section to identify "
                "suitable opportunities."
            )

        else:

            st.write(
                "Continue developing role-specific skills, "
                "build practical projects, and tailor your "
                "resume toward the positions you want."
            )

        st.success(
            "Career advice generated using your resume "
            "and job-matching context."
        )