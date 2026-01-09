import ast
from pathlib import Path
import subprocess
import easier_openai
from index_and_search import search
import pyperclip


def main():
    chatbot = easier_openai.Assistant(
        model="gpt-5.1", system_prompt="Act as a specialized software engineer for Blender's Python API. Translate natural language requests into accurate Python code for Blender. Return error-free code, exactly matching the user's request.", reasoning_effort="high")
    entry = input("Enter Your requirements: ")
    download_as = input("Download as (stl, blend, no download): ")

    global requirements
    print("Generating code...")
    requirements = entry + \
        f" At the end of the code, make it download like this to the downloads folder of whatever operating system they are on: {download_as}. Add this as a comment to the start of the code: requirements: {entry}. DO NOT USE ANY DEPRECATED FUNCTIONS"
    files = []
    queries = ast.literal_eval(str(chatbot.chat(
        f"Create search queries tailored for the Blender 5.0 documentation that satisfy the provided requirements: {requirements}. \
            Your response must be in the following Python list format: ['Query1', 'Query2', 'Query3']. \
            Since the queries are intended for the Python API documentation, do not include the terms 'blender', 'python', or 'api' in your queries. \
            Aim to keep each query to a maximum of two words; four words is the absolute maximum allowed. Note: identifiers such as 'bpy.ops.export_mesh.stl' should be considered as a single word. \
            Output Verbosity: Return how many ever queries you need to satisfy the requirements, each query being formatted in the required list format. Each query should be a succinct phrase (≤4 words, ≤1 line each). Do not add any explanations or extra content. Prioritize complete, actionable queries within this length cap. \"Armature\" is a valid and good query. Try not to search for actual functions, but rather what the functions that you want actually do. For example bpy.ops.export_mesh.stl does not actually download anything, as it is invaliud syntx. Try searching for download stl instead.", file_search=files)))
    for query in queries:
        print(query)
        print(search(query))
        files.extend(search(query)[:2])
    print("Generating final code.. This may take a while... \n")
    final_stream = chatbot.chat(
        f"Write code for these requirements. Read documentation, found in the file search tool, and generate accurate code based on them. make sure it works at all costs, exactly matching the user's requirements: {requirements} Use the web search tool to if the user asks for a real life object and does not give further info to seek out dimensions and exact properties. ALWAYs ADD COLOR AND MAKE REALISTIC UNLESS OTHERWISE SPECIFIED BY THE REQUIREMENTS", file_search=files, text_stream=True, web_search=True)
    final = ""
    for chunk in final_stream:
        if chunk == "done":
            break
        final += str(chunk)
        print(chunk, end="")
    final = final.removeprefix("```python\n").removesuffix(
        "\n```").replace("```python", "", 1)
    final = final[final.find("#"):]
    pyperclip.copy(final)
    print(final)
    BLENDER_EXE = "C:/Program Files/Blender Foundation/Blender 5.0/blender.exe"
    if not "no" in download_as:
        d_path = Path.home() / "Downloads"
        with open(f"{d_path}/{download_as}.py", "w", encoding="utf-8") as f:
            f.write(final)
        subprocess.run(executable=BLENDER_EXE, args=[
            "--background", "--factory-startup", f"{download_as}.py"], cwd=d_path)


if __name__ == "__main__":
    main()
