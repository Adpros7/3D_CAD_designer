import os
import time
import joblib
import numpy as np
from html.parser import HTMLParser
from sklearn.feature_extraction.text import TfidfVectorizer

HTML_DIR = "html_files"
CACHE_DIR = ".search_cache"
INDEX_FILE = os.path.join(CACHE_DIR, "index.joblib")

os.makedirs(CACHE_DIR, exist_ok=True)


class UltraFastStripper(HTMLParser):
    def __init__(self, limit=200_000):
        super().__init__()
        self.parts = []
        self.size = 0
        self.limit = limit
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript", "svg"):
            self.skip = False

    def handle_data(self, data):
        if self.skip:
            return
        self.parts.append(data)
        self.size += len(data)
        if self.size >= self.limit:
            raise StopIteration

    def get_text(self):
        return " ".join(self.parts)


def extract_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    stripper = UltraFastStripper()
    try:
        stripper.feed(html)
    except StopIteration:
        pass

    return stripper.get_text()


def build_index():
    print("building index...")
    t0 = time.time()

    texts = []
    files = []

    for name in os.listdir(HTML_DIR):
        if name.endswith(".html"):
            files.append(name)
            texts.append(extract_text(os.path.join(HTML_DIR, name)))

    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=12000,
        min_df=2,
        max_df=0.9,
        ngram_range=(1, 1),
        dtype=np.float32
    )

    matrix = vectorizer.fit_transform(texts)

    joblib.dump(
        (vectorizer, matrix, files),
        INDEX_FILE,
        compress=3
    )

    print(f"done in {time.time() - t0:.2f}s")


def load_index():
    if not os.path.exists(INDEX_FILE):
        build_index()
    return joblib.load(INDEX_FILE)


vectorizer, matrix, files = load_index()


def search(query, top_k=3):
    q = vectorizer.transform([query])
    scores = (matrix @ q.T).toarray().ravel()

    idx = np.argpartition(scores, -top_k)[-top_k:]
    idx = idx[np.argsort(scores[idx])[::-1]]

    return [(files[i], float(scores[i])) for i in idx]


if __name__ == "__main__":
    results = search("camera focal length")
    for f, s in results:
        print(f, round(s, 4))
