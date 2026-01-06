import ast
from concurrent.futures.thread import ThreadPoolExecutor
import easier_openai
from index_and_search import search
import pyperclip
import tkinter as tk
from tkinter import ttk


def main():
    chatbot = easier_openai.Assistant(
        model="gpt-5.1", system_prompt="Act as a specialized software engineer for Blender's Python API. Translate natural language requests into accurate Python code for Blender. Return error-free code, exactly matching the user's request.", reasoning_effort="high")
    entry = input("Enter Your requirements: ")
    download_as = input("Download as (stl, blend, no download): ")

    def worker():
        global requirements
        print("Generating code...")
        requirements = entry + \
            f" At the end of the code, make it download like this to the downloads folder of whatever operating system they are on: {download_as}. Add this as a comment to the start of the code: \"requirements\": {entry} DO NOT USE ANY DEPRECATED FUNCTIONS"
        files = []
        queries = ast.literal_eval(str(chatbot.chat(
            f"Create search queries tailored for the Blender documentation that satisfy the provided requirements: {requirements}. \
                Your response must be in the following Python list format: ['Query1', 'Query2', 'Query3']. \
                Since the queries are intended for the Python API documentation, do not include the terms 'blender', 'python', or 'api' in your queries. \
                Aim to keep each query to a maximum of two words; four words is the absolute maximum allowed. Note: identifiers such as 'bpy.ops.export_mesh.stl' should be considered as a single word. \
                Output Verbosity: Return how many ever queries you need to satisfy the requirements, each query being formatted in the required list format. Each query should be a succinct phrase (≤4 words, ≤1 line each). Do not add any explanations or extra content. Prioritize complete, actionable queries within this length cap. \"Armature\" is a valid and good query.", file_search=files)))
        for query in queries:
            print(query)
            print(search(query))
            files.extend(search(query)[:2])
        final = str(chatbot.chat(f"Write code for these requirements: {requirements}", file_search=files)).removeprefix(
            "```python\n").removesuffix("\n```")
        pyperclip.copy(final)
        print(final)
        if not "no" in download_as:
            pass
        return final

    worker()

if __name__ == "__main__":
    main()
