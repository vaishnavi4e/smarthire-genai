from pydantic import BaseModel, Field
import re


class CandidateProfile(BaseModel):
    """Structured candidate profile."""

    name: str = "Candidate"

    skills: list[str] = Field(
        default_factory=list
    )

    experience: list[str] = Field(
        default_factory=list
    )

    education: list[str] = Field(
        default_factory=list
    )

    target_role: str = "Not specified"


def validate_candidate_profile(
    profile: CandidateProfile,
) -> CandidateProfile:
    """Validate and clean a candidate profile."""

    if not profile.name.strip():
        profile.name = "Candidate"

    profile.skills = list(
        dict.fromkeys(
            skill.strip()
            for skill in profile.skills
            if skill and skill.strip()
        )
    )

    profile.experience = list(
        dict.fromkeys(
            item.strip()
            for item in profile.experience
            if item and item.strip()
        )
    )

    profile.education = list(
        dict.fromkeys(
            item.strip()
            for item in profile.education
            if item and item.strip()
        )
    )

    return profile


COMMON_SKILLS = [
    "Python",
    "Java",
    "C++",
    "C",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "Machine Learning",
    "Deep Learning",
    "Artificial Intelligence",
    "Data Analysis",
    "Data Science",
    "Excel",
    "Power BI",
    "Tableau",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Git",
    "GitHub",
    "Docker",
    "AWS",
    "Azure",
    "TensorFlow",
    "PyTorch",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "NLP",
    "Natural Language Processing",
    "Communication",
    "Leadership",
]


def parse_resume_local(resume_text: str) -> CandidateProfile:
    """
    Extract a basic candidate profile locally
    without using an external LLM API.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text is empty. Please upload a valid resume."
        )

    text = resume_text.strip()
    lower_text = text.lower()

    # -----------------------------------------
    # NAME
    # -----------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    name = "Candidate"

    for line in lines[:10]:

        cleaned = re.sub(
            r"[^A-Za-z .'-]",
            "",
            line
        ).strip()

        if (
            2 <= len(cleaned.split()) <= 5
            and "resume" not in cleaned.lower()
            and "curriculum" not in cleaned.lower()
        ):
            name = cleaned
            break

    # -----------------------------------------
    # SKILLS
    # -----------------------------------------

    detected_skills = []

    for skill in COMMON_SKILLS:

        if skill.lower() in lower_text:
            detected_skills.append(skill)

    detected_skills = list(
        dict.fromkeys(detected_skills)
    )

    # -----------------------------------------
    # EXPERIENCE
    # -----------------------------------------

    experience = []

    experience_keywords = [
        "intern",
        "developer",
        "engineer",
        "analyst",
        "manager",
        "consultant",
    ]

    for keyword in experience_keywords:

        if keyword in lower_text:
            experience.append(
                f"Relevant experience related to {keyword}"
            )

    experience = list(
        dict.fromkeys(experience)
    )[:5]

    # -----------------------------------------
    # EDUCATION
    # -----------------------------------------

    education = []

    education_patterns = [
        r"\bB\.?\s*Tech\b",
        r"\bB\.?\s*E\b",
        r"\bB\.?\s*Sc\b",
        r"\bM\.?\s*Tech\b",
        r"\bM\.?\s*E\b",
        r"\bM\.?\s*Sc\b",
        r"\bMBA\b",
        r"\bBCA\b",
        r"\bMCA\b",
        r"\bBachelor\b",
        r"\bMaster\b",
    ]

    for pattern in education_patterns:

        matches = re.findall(
            pattern,
            text,
            flags=re.IGNORECASE
        )

        for match in matches:
            education.append(match)

    education = list(
        dict.fromkeys(education)
    )

    # -----------------------------------------
    # TARGET ROLE
    # -----------------------------------------

    role_keywords = [
        "Data Scientist",
        "Data Analyst",
        "Machine Learning Engineer",
        "AI Engineer",
        "Software Engineer",
        "Software Developer",
        "Web Developer",
        "Python Developer",
        "Full Stack Developer",
        "Backend Developer",
        "Frontend Developer",
        "Business Analyst",
        "Product Manager",
    ]

    target_role = "Not specified"

    for role in role_keywords:

        if role.lower() in lower_text:
            target_role = role
            break

    # -----------------------------------------
    # CREATE PROFILE
    # -----------------------------------------

    profile = CandidateProfile(
        name=name,
        skills=detected_skills,
        experience=experience,
        education=education,
        target_role=target_role,
    )

    return validate_candidate_profile(profile)