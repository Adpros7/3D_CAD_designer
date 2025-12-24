import os
from bs4 import BeautifulSoup
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

HTML_DIR = "html_files"
CACHE_DIR = ".search_cache"
INDEX_FILE = os.path.join(CACHE_DIR, "index.joblib")

os.makedirs(CACHE_DIR, exist_ok=True)

def extract_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        soup = BeautifulSoup(f, "html.parser")
        for t in soup(["script", "style"]):
            t.decompose()
        return soup.get_text(" ")

def build_index():
    texts = []
    files = []

    for f in os.listdir(HTML_DIR):
        if f.endswith(".html"):
            files.append(f)
            texts.append(extract_text(os.path.join(HTML_DIR, f)))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=20000,
        ngram_range=(1, 2),
        dtype=np.float32
    )

    matrix = vectorizer.fit_transform(texts).tocsr() # type: ignore

    joblib.dump((vectorizer, matrix, files), INDEX_FILE)

def load_index():
    if not os.path.exists(INDEX_FILE):
        build_index()
    return joblib.load(INDEX_FILE)

vectorizer, matrix, files = load_index()

def search(query, top_k=3):
    q = vectorizer.transform([query])
    scores = (matrix @ q.T).toarray().ravel()

    top_idx = np.argpartition(scores, -top_k)[-top_k:]
    top_idx = top_idx[np.argsort(scores[top_idx])[::-1]]

    return [(files[i], float(scores[i])) for i in top_idx]

if __name__ == "__main__":
    for f, s in search("animation of vectors"):
        print(f, round(s, 4))
