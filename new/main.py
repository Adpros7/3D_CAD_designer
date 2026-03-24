import json
import os
import subprocess
import tempfile
from pathlib import Path

from easier_openai import Assistant
from search import search

with open(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\prompts.json") as f:
    prompts = json.load(f)

userInput: str = input("What do you want to design?\n")
path: str | Path = input("Where do you want to save it?\n") or Path().home()
nameOfFile: str = input("What do you want to call it?\n") or "output"
stlOrBlend = input("Do you want to save it as a .stl or .blend file?\n")
stlOrBlend = "stl" if "s" in stlOrBlend.lower() else "blend"

workerAgent: Assistant = Assistant(
    system_prompt=prompts["worker_system"], default_conversation=False, model="gpt-5.2"
)
orchestrationAgent: Assistant = Assistant(
    system_prompt=prompts["orchestration_system"],
    default_conversation=True,
    model="gpt-5.2",
)

searchTerms: str = str(workerAgent.chat(prompts["search_terms"].format(inp=userInput)))
print(searchTerms + "\n\n\n\n\n\n")

searchResults = [
    search(i.strip(), 1)[0] if len(search(i.strip(), 1)) > 0 else None
    for i in searchTerms.split(",")
]

searchResults = [i[0] for i in searchResults if i is not None]
print(searchResults)
print("\n\n\n\n\n\n")
modelParts: list[str] = orchestrationAgent.chat(
    prompts["parts_decomposition"].format(inp=userInput, results=searchResults),
    file_search=searchResults,
    text_stream=False,
    return_full_response=False,
    stream=False
).split(",")

print(modelParts)
partResults = []
for i in modelParts:
    partResults.append(
        workerAgent.chat(
            prompts["worker_task"].format(component=i),
            file_search=searchResults,
        )
    )

final = orchestrationAgent.chat(prompts["merge_code"].format(scripts=partResults))

with tempfile.NamedTemporaryFile(
    "w", delete=False, encoding="utf-8", suffix=".py"
) as f:
    name: str = f.name
    f.write(
        f"{final}\n\n\nbpy.ops.{"wm.save_as_mainfile" if stlOrBlend == "blend" else "export_mesh.stl"}\
            (filepath='{os.path.join(path, nameOfFile).replace("\\", "/")}.{stlOrBlend}')\n"
    )

    print(name, f"{final}\n\n\nbpy.ops.{"wm.save_as_mainfile" if stlOrBlend == "blend" else "export_mesh.stl"}\
            (filepath='{path}/{nameOfFile}.{stlOrBlend}')\n")


subprocess.run(
    ["blender", "-b", "-P", name,]
)

os.remove(name)
