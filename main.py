from concurrent.futures import thread
import easier_openai
from search import search
import pyperclip
import tkinter as tk

def main():
    chatbot = easier_openai.Assistant(model="gpt-5.1", system_prompt="Act as a specialized software engineer for Blender's Python API. Translate natural language requests into accurate Python code for Blender. Return error-free code, exactly matching the user's request.")
    root = tk.Tk()
    root.geometry("400x400")
    root.title("Blender Python Code Generator")
    entry = tk.Entry(root, bg="black", fg="white")
    entry.place(relx=0.5, rely=0.1, relwidth=0.8, relheight=0.1, anchor="center")
    requirements = ""
    def worker():
        global requirements
        global final
        files = ["html_files/" +f[0] for f in search(chatbot.chat(f"write search queries for the blender docs that matches the following requirements: {requirements} RESPOND ONLY IN PYTHON LIST FORMAT LIKE THIS: ['Query1', 'Query2', 'Query3']"))]
        final = str(chatbot.chat(f"Write code for these requirements: {requirements}", file_search=files)).removeprefix("```python\n").removesuffix("\n```")
        pyperclip.copy(final)
        
    def get_text():
        global requirements
        requirements = entry.get()
        thread.ThreadPoolExecutor().submit(worker)


    genButton = tk.Button(root, text="Generate Code", command=get_text , bg="black", fg="white")
    genButton.place(relx=0.5, rely=0.2, relwidth=0.2, relheight=0.1, anchor="center")
    print(final)
    # copied_message = tk.Label(root, text="Code Copied to Clipboard", bg="black", fg="white")
    # copied_message.place(relx=0.5, rely=0.3, relwidth=0.8, relheight=0.1, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    main()
