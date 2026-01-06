import os
from typing import Any
from unittest import result
from whoosh.qparser import QueryParser
from whoosh.index import create_in, open_dir
from whoosh.fields import * # type: ignore

def indexer():
    schema = Schema(title=TEXT(stored=True),
                    path=ID(stored=True), content=TEXT)
    ix = create_in("./.search_cache", schema)
    writer = ix.writer()
    files = os.listdir(r"C:\Users\prani\Coding\AI\3D_CAD_designer\blender_docs")
    for file in files:
        with open(f"blender_docs/{file}", "r", encoding="utf-8") as f:
            writer.add_document(title=f"{file.removesuffix('.md')}", path=f"blender_docs/{file}",
                                content=f"{f.read()}")

    writer.commit()

def search(query):
    ix = open_dir("./.search_cache")
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query)
        results = searcher.search(query)
        parsed_results = [result["path"] for result in results]
        return [parsed_results[0] if len(parsed_results) > 0 else None, parsed_results[1] if len(parsed_results) > 1 else None, parsed_results[2] if len(parsed_results) > 2 else None]

def main():
    indexer()

if __name__ == "__main__":
    main()
