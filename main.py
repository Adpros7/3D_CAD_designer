from concurrent.futures.thread import ThreadPoolExecutor
import easier_openai
from search import search
import pyperclip
import tkinter as tk
from syntaxmod import general, wait_until
from tkinter import ttk


def main():
    chatbot = easier_openai.Assistant(
        model="gpt-5.1", system_prompt="Act as a specialized software engineer for Blender's Python API. Translate natural language requests into accurate Python code for Blender. Return error-free code, exactly matching the user's request.", reasoning_effort="high")
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Blender Python Code Generator")
    entry = tk.Entry(root, bg="black", fg="white")
    entry.place(relx=0.5, rely=0.1, relwidth=0.8,
                relheight=0.1, anchor="center")
    tk.Label(root, text="Download as:", justify="center").place(relx=0.4, rely=0.6)
    download_as = ttk.Combobox(root, values=["stl", "blend", "no download"])
    download_as.place(rely=0.7, relwidth=0.4, relx=0.5, anchor="center")

    def worker():
        global requirements
        global final
        files = ["html_files/" + f[0] for f in search(chatbot.chat(
            f"write search queries for the blender docs that matches the following requirements: {requirements} RESPOND ONLY IN PYTHON LIST FORMAT LIKE THIS: ['Query1', 'Query2', 'Query3']"))]
        final = str(chatbot.chat(f"Write code for these requirements: {requirements}", file_search=files, web_search=True)).removeprefix(
            "```python\n").removesuffix("\n```")
        pyperclip.copy(final)
        print(final)
        return final

    def start_work():
        global requirements
        global thread
        requirements = entry.get() + " "
        thread = ThreadPoolExecutor().submit(worker)
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
