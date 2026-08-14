# SmartHire GenAI – Resume Matching & AI Career Mentor

SmartHire GenAI is an AI-powered career portal that helps students analyze their resumes, discover relevant job opportunities, improve their CVs, and get career guidance through an AI Career Mentor.

## Features

- Resume parsing using LLM structured output
- Extract candidate profile including skills, education, experience, and target role
- Semantic job matching using embeddings
- FAISS vector database for job search
- AI-generated CV improvement suggestions
- RAG-based AI Career Mentor
- LangChain workflow
- Guardrails for safe and relevant responses
- Streamlit web interface

## Technologies Used

- Python
- Generative AI / LLM API
- LangChain
- Embeddings
- FAISS
- RAG
- Streamlit
- Pandas
- PyPDF
- Git & GitHub

## Project Structure

```text
smarthire-genai/
├── data/
│   ├── jobs/
│   ├── resumes/
│   └── career_notes/
├── vectorstore/
├── notebooks/
├── src/
│   ├── parsing/
│   ├── search/
│   ├── generate/
│   ├── mentor/
│   └── safety/
├── app/
├── reports/
├── README.md
├── requirements.txt
├── .env.example
└── .gitignore