from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from nltk.translate.meteor_score import meteor_score
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from rouge_score import rouge_scorer
from difflib import SequenceMatcher
import ast
from typing import Dict, Union
from nltk.tokenize import word_tokenize
import nltk
from pydantic import BaseModel

nltk.download('wordnet') ## run only once, data needed for tokenizer
nltk.download('omw-1.4') ## run only once, data needed for tokenizer
nltk.download('punkt') ## run only once, data needed for tokenizer

class MetricsResult(BaseModel):
    METEOR: float
    ROUGE: Dict[str, float]
    BLEU: float
    Cosine_Similarity: float
    AST_Comparison: int
    Levenshtein_Distance: int

# Helper function to clean code by removing comments, extra spaces, and empty lines
def clean_code(code: str) -> str:
    lines = code.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.split("#")[0].strip()  # Remove comments and strip whitespace
        if line:  # Ignore empty lines
            cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# METEOR calculation
def calculate_meteor(reference: str, candidate: str) -> float:
    reference_tokens = word_tokenize(reference)  # Tokenize reference
    candidate_tokens = word_tokenize(candidate)  # Tokenize candidate
    return meteor_score([reference_tokens], candidate_tokens)

# ROUGE calculation
def calculate_rouge(reference: str, candidate: str) -> Dict[str, float]:
    scorer = rouge_scorer.RougeScorer(["rouge1", "rouge2", "rougeL"], use_stemmer=True)
    scores = scorer.score(reference, candidate)
    return {
        "ROUGE-1": scores["rouge1"].fmeasure,
        "ROUGE-2": scores["rouge2"].fmeasure,
        "ROUGE-L": scores["rougeL"].fmeasure,
    }

# BLEU calculation
def calculate_bleu(reference: str, candidate: str) -> float:
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()
    smoothing = SmoothingFunction().method1
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoothing)
    return bleu_score

# Cosine similarity calculation
def calculate_cosine_similarity(reference: str, candidate: str) -> float:
    vectorizer = CountVectorizer().fit_transform([reference, candidate])
    vectors = vectorizer.toarray()
    return cosine_similarity(vectors)[0, 1]

# AST comparison
def compare_ast(reference: str, candidate: str) -> int:
    try:
        reference_ast = ast.parse(reference)
        candidate_ast = ast.parse(candidate)
        return 1 if ast.dump(reference_ast) == ast.dump(candidate_ast) else 0
    except SyntaxError:
        return 0

# Levenshtein distance calculation
def calculate_levenshtein_distance(reference: str, candidate: str) -> int:
    matcher = SequenceMatcher(None, reference, candidate)
    return int(sum(1 for _ in matcher.get_opcodes() if _))  # Return edit distance approximation

# Main function to evaluate metrics
def evaluate_metrics(reference_code: str, candidate_code: str) -> MetricsResult:
    reference_code_cleaned = clean_code(reference_code)
    candidate_code_cleaned = clean_code(candidate_code)

    metrics = {
        "METEOR": calculate_meteor(reference_code_cleaned, candidate_code_cleaned),
        "ROUGE": calculate_rouge(reference_code_cleaned, candidate_code_cleaned),
        "BLEU": calculate_bleu(reference_code_cleaned, candidate_code_cleaned),
        "Cosine Similarity": calculate_cosine_similarity(reference_code_cleaned, candidate_code_cleaned),
        "AST Comparison": compare_ast(reference_code_cleaned, candidate_code_cleaned),
        "Levenshtein Distance": calculate_levenshtein_distance(reference_code_cleaned, candidate_code_cleaned),
    }
    
    return MetricsResult(**metrics)

# Example usage
if __name__ == "__main__":
    reference_code = """
    def add(a, b):
        return a + b
    """

    candidate_code = """
    def add(x, y):
        return x + y
    """

    metrics = evaluate_metrics(reference_code, candidate_code)
    for metric, value in metrics.items():
        print(f"{metric}: {value}")
