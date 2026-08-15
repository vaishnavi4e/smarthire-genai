from src.parsing.resume_parser import CandidateProfile
from src.search.job_search import JobSearch


def main():
    profile = CandidateProfile(
        name="Test Candidate",
        skills=[
            "Python",
            "SQL",
            "Machine Learning",
            "Data Analysis"
        ],
        experience=[
            "Data Analyst Intern"
        ],
        education=[
            "B.Tech Computer Science"
        ],
        target_role="Data Analyst"
    )

    search_engine = JobSearch()

    results = search_engine.search(
        profile,
        top_k=5
    )

    print("\nTOP 5 MATCHING JOBS")
    print("=" * 70)

    for i, job in enumerate(results, start=1):
        print(f"\n{i}. {job['jobtitle']}")
        print(f"Company: {job['company']}")
        print(f"Location: {job['joblocation_address']}")
        print(f"Skills: {job['skills']}")
        print(f"Similarity: {job['similarity_score']:.4f}")


if __name__ == "__main__":
    main()
    