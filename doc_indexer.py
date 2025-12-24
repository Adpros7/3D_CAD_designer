from pathlib import Path
from bs4 import BeautifulSoup
from rapidfuzz import process, fuzz
import json
import re


class BlenderDocIndex:
    def __init__(self, docs_root: str, out_dir: str):
        self.docs_root = Path(docs_root)
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.index = {}

    def build(self):
        html_files = list(self.docs_root.rglob("*.html"))
        if not html_files:
            raise RuntimeError("No HTML files found")

        for html_path in html_files:
            text = self._extract_text(html_path)
            if not text:
                continue

            rel = html_path.relative_to(self.docs_root)
            safe_name = self._safe_name(rel)

            txt_path = self.out_dir / f"{safe_name}.txt"
            txt_path.write_text(text, encoding="utf-8")

            self.index[safe_name] = {
                "path": str(txt_path),
                "title": text.split("\n", 1)[0][:200],
                "content": text,
            }

        self._save_index()

    def search(self, query: str, limit: int = 5):
        if not self.index:
            self._load_index()

        choices = {k: v["content"] for k, v in self.index.items()}
        results = process.extract(
            query,
            choices,
            scorer=fuzz.WRatio,
            limit=limit,
        )

        return [
            {
                "doc": key,
                "score": score,
                "path": self.index[key]["path"],
                "title": self.index[key]["title"],
            }
            for key, score, _ in results
        ]

    def _extract_text(self, html_path: Path) -> str:
        soup = BeautifulSoup(
            html_path.read_text(encoding="utf-8", errors="ignore"),
            "html.parser",
        )

        # Remove UI junk
        for selector in [
            "nav",
            "header",
            "footer",
            "script",
            "style",
            "aside",
            ".sidebar-drawer",
            ".toc-drawer",
            ".theme-toggle",
            ".edit-this-page",
            ".related-pages",
        ]:
            for tag in soup.select(selector):
                tag.decompose()

        article = soup.find("article", id="furo-main-content")
        if not article:
            return ""

        lines = []
        for el in article.find_all(["h1", "h2", "h3", "p", "li"]):
            t = el.get_text(" ", strip=True)
            if t:
                lines.append(t)

        if not lines:
            return ""

        text = "\n\n".join(lines)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def _safe_name(self, path: Path) -> str:
        name = str(path.with_suffix(""))
        name = name.replace("\\", "_").replace("/", "_")
        return re.sub(r"[^a-zA-Z0-9_]+", "_", name)

    def _save_index(self):
        index_path = self.out_dir / "index.json"
        index_path.write_text(
            json.dumps(self.index, indent=2),
            encoding="utf-8",
        )

    def _load_index(self):
        index_path = self.out_dir / "index.json"
        if not index_path.exists():
            raise RuntimeError("Index not built yet")
        self.index = json.loads(index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    docs = BlenderDocIndex(
        docs_root="blender_docs",
        out_dir="blender_txt",
    )
    docs.build()

    # quick test
    results = docs.search("sequencer scene rendering")
    for r in results:
        print(r["score"], r["title"], "->", r["path"])
