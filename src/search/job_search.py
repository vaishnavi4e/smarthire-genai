from pathlib import Path

import faiss
import numpy as np
import pandas as pd

from src.search.embed import create_embedding_model


INDEX_PATH = "vectorstore/jobs.index"
METADATA_PATH = "vectorstore/jobs_metadata.csv"


class JobSearch:
    """Semantic job search using FAISS."""

    def __init__(
        self,
        index_path: str = INDEX_PATH,
        metadata_path: str = METADATA_PATH,
    ):
        if not Path(index_path).exists():
            raise FileNotFoundError(
                f"FAISS index not found: {index_path}"
            )

        if not Path(metadata_path).exists():
            raise FileNotFoundError(
                f"Job metadata not found: {metadata_path}"
            )

        self.index = faiss.read_index(index_path)
        self.metadata = pd.read_csv(metadata_path)
        self.model = create_embedding_model()

    def create_candidate_text(self, profile) -> str:
        """Convert a candidate profile into searchable text."""

        return "\n".join([
            f"name: {profile.name}",
            f"skills: {', '.join(profile.skills)}",
            f"experience: {', '.join(profile.experience)}",
            f"education: {', '.join(profile.education)}",
            f"target_role: {profile.target_role}",
        ])

    def search(self, profile, top_k: int = 5) -> list[dict]:
        """Return the top matching jobs."""

        candidate_text = self.create_candidate_text(profile)

        candidate_embedding = self.model.encode(
            [candidate_text],
            normalize_embeddings=True,
        )

        candidate_embedding = np.asarray(
            candidate_embedding,
            dtype="float32"
        )

        scores, indices = self.index.search(
            candidate_embedding,
            top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            job = self.metadata.iloc[int(index)].to_dict()
            job["similarity_score"] = float(score)
            results.append(job)

        return results