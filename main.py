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
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Blender Python Code Generator")
    entry = input("Enter Your requirements:")
    download_as = ttk.Combobox(
        root, values=["stl", "blend", "no download"], name="download as")
    download_as.current(0)
    download_as.place(rely=0.7, relwidth=0.4, relx=0.5, anchor="center")

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
        if download_as.get() != "no download":
            pass
        return final

    def start_work():
        global requirements
        global thread
        requirements = entry.get() + \
            f" At the end of the code, make it download like this to the downloads folder of whatever operating system they are on: {download_as.get()}. Add this as a comment to the start of the code: {entry.get()} DO NOT USE ANY DEPRECATED FUNCTIONS"
        executor = ThreadPoolExecutor(max_workers=1)
        thread = executor.submit(worker)
        print("sent")
        thread.add_done_callback(lambda future: copied_message.place(
            relx=0.5, rely=0.3, relwidth=1, relheight=0.1, anchor="center"))

    genButton = tk.Button(root, text="Generate Code",
                          command=start_work, bg="black", fg="white")
    genButton.place(relx=0.5, rely=0.2, relwidth=0.5,
                    relheight=0.1, anchor="center")
    copied_message = tk.Label(
        root, text="Code Copied to Clipboard", bg="black", fg="white")
    root.mainloop()


if __name__ == "__main__":
    main()
