from pydantic import BaseModel, Field


class CVSuggestions(BaseModel):
    """Structured CV improvement suggestions."""

    missing_skills: list[str] = Field(
        default_factory=list,
        description="Skills the candidate should consider developing."
    )

    improved_bullets: list[str] = Field(
        default_factory=list,
        description="Improved versions of weak resume bullet points."
    )

    general_suggestions: list[str] = Field(
        default_factory=list,
        description="General suggestions for improving the resume."
    )


def create_cv_prompt(
    resume_text: str,
    target_role: str,
    matched_jobs: list[dict],
) -> str:
    """Create a prompt for CV improvement."""

    job_context = "\n".join(
        [
            f"- {job.get('jobtitle', '')}: "
            f"{job.get('skills', '')}"
            for job in matched_jobs
        ]
    )

    return f"""
You are an expert career and resume improvement assistant.

Analyze the candidate's resume for the target role.

TARGET ROLE:
{target_role}

RESUME:
{resume_text}

TOP MATCHING JOBS:
{job_context}

Provide:

1. Missing or useful skills the candidate should consider developing.
2. Improved versions of weak resume bullet points.
3. General resume improvement suggestions.

Rules:
- Do not invent experience or qualifications.
- Do not claim the candidate has a skill they do not have.
- Keep suggestions specific and actionable.
- Base recommendations on the resume and matching jobs.
- Return structured information only.
"""
import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


def generate_cv_suggestions(
    resume_text: str,
    target_role: str,
    matched_jobs: list[dict],
) -> CVSuggestions:
    """
    Generate structured CV improvement suggestions using an LLM.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found. Add it to the .env file."
        )

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=api_key,
    )

    structured_llm = llm.with_structured_output(CVSuggestions)

    prompt = create_cv_prompt(
        resume_text=resume_text,
        target_role=target_role,
        matched_jobs=matched_jobs,
    )

    result = structured_llm.invoke(prompt)

    return result