Add por_inference.py: selects questions based on PoR firing score (E = Q × S_q × t)

por_inference.py — 改良版 PoR微積対応アルゴリズム

import logging from typing import List, Tuple, Optional, Dict, Callable import spacy import numpy as np import torch from transformers import pipeline from models.por_model import PoRModel, DefaultPoRModel

ロギング設定

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') logger = logging.getLogger(name)

NLP & BERTモデル読み込み

try: nlp_default = spacy.load("en_core_web_sm") except OSError: logger.error("spaCy model not found. Run: python -m spacy download en_core_web_sm") raise

try: device = 0 if torch.cuda.is_available() else -1 embedder_default = pipeline("feature-extraction", model="distilbert-base-uncased", device=device) except Exception as e: logger.error(f"Embedding pipeline init failed: {e}") raise

class PoRInference: """PoR構造に基づく対応選択エンジン"""

def __init__(
    self,
    threshold: float = 0.5,
    max_question_length: int = 100,
    max_context_vocab: int = 50,
    por_model: Optional[PoRModel] = None,
    nlp_model=None,
    embed_pipeline=None
):
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
    unique_tokens = len(set(token.text.lower() for token in doc if token.is_alpha))
    return min(unique_tokens / self.max_context_vocab, 1.0)

def _calculate_temporal_relevance(self, time_score: float) -> float:
    try:
        return max(min(float(time_score), 1.0), 0.0)
    except Exception as e:
        logger.error("Invalid time_score: %s", e)
        return 0.5

def _get_embedding(self, text: str) -> Optional[np.ndarray]:
    try:
        output = self.embedder(text, return_tensors="pt")[0][0]
        if output.shape[0] == 0:
            return None
        return output.mean(dim=0).detach().cpu().numpy()
    except Exception as e:
        logger.error(f"Embedding failed: {e}")
        return None

def _compute_semantic_similarity(self, question: str, context_emb: np.ndarray) -> float:
    question_emb = self._get_embedding(question)
    if question_emb is None or context_emb is None:
        return 0.0
    cos_sim = np.dot(question_emb, context_emb) / (np.linalg.norm(question_emb) * np.linalg.norm(context_emb))
    return max(cos_sim, 0.0)

def compute_por_score(self, question: str, context: str, time_score: float) -> Dict[str, float]:
    question_score = self._calculate_question_score(question)
    context_density = self._calculate_context_density(context)
    temporal_relevance = self._calculate_temporal_relevance(time_score)
    context_emb = self._get_embedding(context)
    semantic_similarity = self._compute_semantic_similarity(question, context_emb)

    score = self.por_model.exist_score(
        question_score=question_score,
        context_density=context_density,
        temporal_relevance=temporal_relevance,
        semantic_similarity=semantic_similarity
    )

    return {
        "E": score,
        "Q": question_score,
        "S_q": context_density,
        "t": temporal_relevance,
        "sim": semantic_similarity
    }

def select_by_por(self, candidates: List[str], context: str, time_score: float = 1.0) -> List[Dict]:
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
            [{"question": c, **self.compute_por_score(c, context, time_score)} for c in candidates],
            key=lambda x: x["E"]
        )
        results.append(fallback)

    return sorted(results, key=lambda x: x["E"], reverse=True)

実行例

if name == "main": por = PoRInference( threshold=0.6, max_question_length=120, por_model=DefaultPoRModel(weights={"question": 0.4, "context": 0.3, "temporal": 0.15, "semantic": 0.15}) ) questions = [ "What is consciousness?", "What is 2 + 2?", "Can machines feel regret?", "Define entropy.", "Explain the weather tomorrow." ] context = "This is a conversation about AI and consciousness in philosophical context." results = por.select_by_por(questions, context, time_score=0.9)

print("PoR-fired questions:")
for item in results:
    print(f" - {item['question']} [E = {item['E']:.4f}] | Q={item['Q']:.2f}, S_q={item['S_q']:.2f}, t={item['t']:.2f}, sim={item['sim']:.2f}")

