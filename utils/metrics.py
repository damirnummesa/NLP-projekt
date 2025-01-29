from pydantic import BaseModel

class MetricsResult(BaseModel):
    MODEL_ID: str
    METEOR: float
    ROUGE_1: float
    ROUGE_2: float
    ROUGE_L: float
    BLEU: float
    CosineSimilarity: float
    ASTComparison: int
    LevenshteinDistance: int
