import logging
from typing import List, Optional, Dict

import spacy
import numpy as np
import torch
from transformers import pipeline

from models.por_model import PoRModel, DefaultPoRModel
from por_diagnostics.cli import main

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

try:
    nlp_default = spacy.load("en_core_web_sm")
except OSError:
    logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm")
    raise

try:
    device = 0 if torch.cuda.is_available() else -1
    embedder_default = pipeline(
        "feature-extraction",
        model="distilbert-base-uncased",
        device=device,
    )
except Exception as e:  # pragma: no cover - hardware dependent
    logger.error(f"Embedding pipeline init failed: {e}")
    raise


class PoRInference:
    """Select questions based on PoR firing score."""

    def __init__(
        self,
        threshold: float = 0.5,
        max_question_length: int = 100,
        max_context_vocab: int = 50,
        por_model: Optional[PoRModel] = None,
        nlp_model=None,
        embed_pipeline=None,
    ) -> None:
        self.threshold = threshold
        self.max_question_length = max_question_length
        self.max_context_vocab = max_context_vocab
        self.por_model = por_model if por_model else DefaultPoRModel()
        self.nlp = nlp_model if nlp_model else nlp_default
        self.embedder = embed_pipeline if embed_pipeline else embedder_default

    def _calculate_question_score(self, question: str) -> float:
        if not question:
            logger.warning("Empty question")
            return 0.0
        doc = self.nlp(question)
        length_score = min(len(question) / self.max_question_length, 1.0)
        entity_score = len(doc.ents) / max(len(doc), 1)
        return 0.7 * length_score + 0.3 * entity_score

    def _calculate_context_density(self, context: str) -> float:
        if not context:
            logger.warning("Empty context")
            return 0.0
        doc = self.nlp(context)
        unique_tokens = len({t.text.lower() for t in doc if t.is_alpha})
        return min(unique_tokens / self.max_context_vocab, 1.0)

    @staticmethod
    def _calculate_temporal_relevance(time_score: float) -> float:
        try:
            return max(min(float(time_score), 1.0), 0.0)
        except Exception as e:  # pragma: no cover - input error
            logger.error("Invalid time_score: %s", e)
            return 0.5

    def _get_embedding(self, text: str) -> Optional[np.ndarray]:
        try:
            output = self.embedder(text, return_tensors="pt")[0][0]
            if output.shape[0] == 0:
                return None
            return output.mean(dim=0).detach().cpu().numpy()
        except Exception as e:  # pragma: no cover - external model
            logger.error("Embedding failed: %s", e)
            return None

    def _compute_semantic_similarity(
        self, question: str, context_emb: Optional[np.ndarray]
    ) -> float:
        question_emb = self._get_embedding(question)
        if question_emb is None or context_emb is None:
            return 0.0
        cos_sim = np.dot(question_emb, context_emb) / (
            np.linalg.norm(question_emb) * np.linalg.norm(context_emb)
        )
        return max(cos_sim, 0.0)

    def compute_por_score(
        self, question: str, context: str, time_score: float
    ) -> Dict[str, float]:
        question_score = self._calculate_question_score(question)
        context_density = self._calculate_context_density(context)
        temporal_relevance = self._calculate_temporal_relevance(time_score)
        context_emb = self._get_embedding(context)
        semantic_similarity = self._compute_semantic_similarity(question, context_emb)

        score = self.por_model.exist_score(
            question_score=question_score,
            context_density=context_density,
            temporal_relevance=temporal_relevance,
            semantic_similarity=semantic_similarity,
        )

        return {
            "E": score,
            "Q": question_score,
            "S_q": context_density,
            "t": temporal_relevance,
            "sim": semantic_similarity,
        }

    def select_by_por(
        self, candidates: List[str], context: str, time_score: float = 1.0
    ) -> List[Dict[str, float]]:
        if not candidates:
            logger.warning("No candidates provided")
            return []

        results = []
        for candidate in candidates:
            structure = self.compute_por_score(candidate, context, time_score)
            if structure["E"] >= self.threshold:
                results.append({"question": candidate, **structure})

        if not results:
            logger.info("No candidates met threshold %.2f", self.threshold)
            fallback = max(
                [
                    {"question": c, **self.compute_por_score(c, context, time_score)}
                    for c in candidates
                ],
                key=lambda x: x["E"],
            )
            results.append(fallback)

        return sorted(results, key=lambda x: x["E"], reverse=True)


if __name__ == "__main__":
    main()
