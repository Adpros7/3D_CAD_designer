import easier_openai
from search import search

def main():
    chatbot = easier_openai.Assistant(model="gpt-5.1", system_prompt="Act as a specialized software engineer for Blender's Python API. Translate natural language requests into accurate Python code for Blender. Return error-free code, exactly matching the user's request.")
    requirements = input("Enter your requirements: ")
    files = ["html_files/" +f[0] for f in search(chatbot.chat(f"write search queries for the blender docs that matches the following requirements: {requirements} RESPOND ONLY IN PYTHON LIST FORMAT LIKE THIS: ['Query1', 'Query2', 'Query3']"))]
    print(str(chatbot.chat(f"Write code for these requirements: {requirements}", file_search=files)).removeprefix("```python\n").removesuffix("\n```"))


if __name__ == "__main__":
    main()
