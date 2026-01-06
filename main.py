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
    entry = input("Enter Your requirements:")
    download_as = input("Download as (stl, blend, no download): ")

    def worker():
        global requirements
        global final
        files = []
        queries = ast.literal_eval(str(chatbot.chat(
            f"write search queries for the blender docs that matches the following requirements: {requirements} RESPOND ONLY IN PYTHON LIST FORMAT LIKE THIS: ['Query1', 'Query2', 'Query3']")))
        for query in queries:
            files.extend(search(query)[:2])
        final = str(chatbot.chat(f"Write code for these requirements: {requirements}", file_search=files)).removeprefix(
            "```python\n").removesuffix("\n```")
        pyperclip.copy(final)
        print(final)
        if not "no" in download_as:
            pass
        return final

    def start_work():
        global requirements
        global thread
        requirements = entry + \
            f" At the end of the code, make it download like this to the downloads folder of whatever operating system they are on: {download_as}. Add this as a comment to the start of the code: \"requirements\": {entry} DO NOT USE ANY DEPRECATED FUNCTIONS"
        executor = ThreadPoolExecutor(max_workers=1)
        thread = executor.submit(worker)
        print("sent")

    start_work()

if __name__ == "__main__":
    main()
