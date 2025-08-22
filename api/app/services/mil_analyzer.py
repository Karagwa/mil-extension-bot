from typing import Dict, List
from app.core.config import settings

LABELS = ["credible", "unknown", "misleading"]

class Analyzer:
    def __init__(self):
        self.model_name = "mock" if settings.mock_mode else "ynie/roberta-large-snli_mnli_fever_anli_R1_R2_R3-nli"
        if not settings.mock_mode:
            from transformers import pipeline
            # zero-shot gives us probabilities across our labels
            self.clf = pipeline(
                    "zero-shot-classification",
                model="D:/huggingface_models/roberta-nli"
                )


    def analyze(self, text: str) -> Dict:
        """
        Returns: {label, score(0..100), tips[], model_name}
        """
        if settings.mock_mode:
            # Deterministic, fast heuristic for tests
            lower = text.lower()
            if "cure" in lower or "miracle" in lower or "shocking" in lower:
                label, score = "misleading", 25.0
            elif "opinion" in lower or "blog" in lower:
                label, score = "unknown", 55.0
            else:
                label, score = "credible", 80.0
        else:
            # Real model: map zero-shot probabilities to our three labels
            candidate_labels = ["credible news", "uncertain", "misleading / fake"]
            res = self.clf(text, candidate_labels=candidate_labels)
            # Take top
            top = res["labels"][0]
            if "credible" in top: label = "credible"
            elif "uncertain" in top: label = "unknown"
            else: label = "misleading"
            score = float(res["scores"][0] * 100)

        tips: List[str] = {
            "credible": [
                "Still cross-check key claims with a second reputable source.",
                "Skim for primary data or named experts.",
            ],
            "unknown": [
                "Check date, author, and outlet; uncertain signals present.",
                "Search if reputable outlets report the same claim.",
            ],
            "misleading": [
                "Beware sensational language; verify with fact-checkers.",
                "Look for missing sourcing or cherry-picked data.",
            ],
        }[label]

        return {"label": label, "score": score, "tips": tips, "model_name": self.model_name}
