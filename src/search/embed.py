import pandas as pd
from sentence_transformers import SentenceTransformer


JOB_TEXT_COLUMNS = [
    "jobtitle",
    "skills",
    "jobdescription",
    "experience",
    "education",
    "industry",
]


def load_job_dataset(file_path: str) -> pd.DataFrame:
    """
    Load the Naukri job dataset.
    """

    df = pd.read_csv(file_path)

    required_columns = JOB_TEXT_COLUMNS + [
        "company",
        "joblocation_address",
    ]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df


def create_job_text(row: pd.Series) -> str:
    """
    Combine important job fields into one searchable text.
    """

    parts = []

    for column in JOB_TEXT_COLUMNS:
        value = row.get(column, "")

        if pd.notna(value) and str(value).strip():
            parts.append(f"{column}: {str(value).strip()}")

    return "\n".join(parts)


def prepare_job_texts(df: pd.DataFrame) -> list[str]:
    """
    Create searchable text for every job posting.
    """

    return df.apply(create_job_text, axis=1).tolist()


def create_embedding_model():
    """
    Load the local sentence-transformer embedding model.
    """

    return SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str], model) -> list:
    """
    Convert text into numerical embeddings.
    """

    return model.encode(
        texts,
        show_progress_bar=True,
        normalize_embeddings=True
    )
