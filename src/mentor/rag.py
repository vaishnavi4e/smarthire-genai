from src.search.job_search import JobSearch


class CareerMentor:
    """
    Retrieval component for the SmartHire Career Mentor.
    """

    def __init__(self):
        self.job_search = JobSearch()

    def retrieve_context(self, query: str, top_k: int = 5) -> str:
        """
        Retrieve relevant job information for a career question.
        """

        # Create a lightweight profile from the user's query.
        class QueryProfile:
            name = "Career Query"
            skills = [query]
            experience = []
            education = []
            target_role = query

        results = self.job_search.search(
            QueryProfile(),
            top_k=top_k
        )

        context = []

        for job in results:
            context.append(
                f"""
Job Title: {job.get('jobtitle', '')}
Company: {job.get('company', '')}
Skills: {job.get('skills', '')}
Experience: {job.get('experience', '')}
Education: {job.get('education', '')}
Industry: {job.get('industry', '')}
Location: {job.get('joblocation_address', '')}
Description: {job.get('jobdescription', '')}
"""
            )

        return "\n---\n".join(context)


def create_mentor_prompt(question: str, context: str) -> str:
    """
    Create a grounded career mentor prompt.
    """

    return f"""
You are SmartHire, an AI career mentor.

Answer the user's career question using ONLY the retrieved job information below.

USER QUESTION:
{question}

RETRIEVED JOB INFORMATION:
{context}

Rules:
- Ground your answer in the retrieved information.
- Do not invent job requirements.
- If the retrieved information is insufficient, clearly say so.
- Give practical and concise career advice.
"""