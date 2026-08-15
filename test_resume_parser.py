from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume


RESUME_PATH = "data/resumes/Shrivatsav_resume3.pdf"


def main():
    print("Loading resume...")

    resume_text = load_resume(RESUME_PATH)

    print("Resume loaded successfully.")
    print("Characters extracted:", len(resume_text))

    print("\nSending resume to the AI parser...")

    profile = parse_resume(resume_text)

    print("\nPROFILE EXTRACTED SUCCESSFULLY")
    print("=" * 50)

    print("Name:", profile.name)
    print("Skills:", profile.skills)
    print("Experience:", profile.experience)
    print("Education:", profile.education)
    print("Target Role:", profile.target_role)


if __name__ == "__main__":
    main()