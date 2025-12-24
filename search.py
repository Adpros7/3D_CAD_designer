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


class BlenderDocStripper(HTMLParser):
    def __init__(self, limit=300_000):
        super().__init__()
        self.parts = []
        self.size = 0
        self.limit = limit
        self.skip = False
        self.in_title = False
        self.in_header = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "noscript"):
            self.skip = True
        elif tag == "title":
            self.in_title = True
        elif tag in ("h1", "h2", "h3"):
            self.in_header = True

    def handle_endtag(self, tag):
        if tag in ("script", "style", "noscript"):
            self.skip = False
        elif tag == "title":
            self.in_title = False
        elif tag in ("h1", "h2", "h3"):
            self.in_header = False

    def handle_data(self, data):
        if self.skip:
            return

        if self.in_title or self.in_header:
            data = (data + " ") * 5

        self.parts.append(data)
        self.size += len(data)

        if self.size >= self.limit:
            raise StopIteration

    def get_text(self):
        return " ".join(self.parts)


def extract_text(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        html = f.read()

    stripper = BlenderDocStripper()
    try:
        stripper.feed(html)
    except StopIteration:
        pass

    return stripper.get_text().lower()


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
        analyzer="char_wb",
        ngram_range=(3, 6),
        min_df=1,
        max_features=50000,
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


def search(query, top_k=5):
    q = vectorizer.transform([query.lower()])
    scores = (matrix @ q.T).toarray().ravel()

    idx = np.argpartition(scores, -top_k)[-top_k:]
    idx = idx[np.argsort(scores[idx])[::-1]]

    return [(files[i], float(scores[i])) for i in idx]


if __name__ == "__main__":
    for f, s in search("rigging bones animation"):
        print(f, round(s, 4))
