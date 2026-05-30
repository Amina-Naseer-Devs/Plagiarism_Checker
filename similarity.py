from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocessing import preprocess_text, is_valid_text
import os

def load_documents(data_folder="data"):
    documents = {}
    for filename in os.listdir(data_folder):
        if filename.endswith(".txt"):
            filepath = os.path.join(data_folder, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                raw_text = f.read()
                cleaned = preprocess_text(raw_text)
                if cleaned.strip():
                    documents[filename] = cleaned
    return documents

def check_similarity(input_text):

    # Edge Case 1 — Empty input
    if not input_text or not input_text.strip():
        return "empty", []

    # Edge Case 2 — Numbers or symbols only
    if not is_valid_text(input_text):
        return "invalid_content", []

    # Edge Case 3 — Too short
    if len(input_text.strip().split()) < 3:
        return "too_short", []

    # Edge Case 4 — No documents in /data
    documents = load_documents()
    if not documents:
        return "no_documents", []

    input_clean = preprocess_text(input_text)

    # Edge Case 5 — Empty after cleaning
    if not input_clean.strip():
        return "invalid_content", []

    doc_names = list(documents.keys())
    doc_texts = list(documents.values())

    all_texts = [input_clean] + doc_texts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    for name, score in zip(doc_names, scores):
        results.append((name, round(score * 100, 2)))

    results.sort(key=lambda x: x[1], reverse=True)

    return "success", results


def get_warning(score):
    if score >= 70:
        return "⚠️  HIGH SIMILARITY — Potential copyright concern. Attribution required."
    elif score >= 40:
        return "🔔  MODERATE SIMILARITY — Content review recommended."
    else:
        return "✅  LOW SIMILARITY — Content appears original."


def get_top_match(results):
    if results:
        top_doc, top_score = results[0]
        return top_doc, top_score
    return None, 0