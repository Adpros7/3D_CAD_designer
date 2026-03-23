import json
import tempfile
from pathlib import Path

from easier_openai import Assistant
from search import search

with open(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\prompts.json") as f:
    prompts = json.load(f)

userInput = input("What do you want to design?\n")
path = input("Where do you want to save it?\n") or Path().home()
stlOrBlend = input("Do you want to save it as a .stl or .blend file?\n")
stlOrBlend = "stl" if "stl" in stlOrBlend.lower() else "blend"

workerAgent = Assistant(
    system_prompt=prompts["worker_system"], default_conversation=False, model="gpt-5.2"
)
orchestrationAgent = Assistant(
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

print(searchResults)
modelParts = orchestrationAgent.chat(
    prompts["parts_decomposition"].format(inp=userInput, results=searchResults),
    file_search=searchResults,
).split(",")

partResults = []
for i in modelParts:
    partResults.append(
        workerAgent.chat(
            prompts["worker_task"].format(component=i),
            custom_tools={"search documentation": search},
        )
    )

final = orchestrationAgent.chat(prompts["merge_code"].format(scripts=partResults))

with tempfile.NamedTemporaryFile(
    "w", delete=False, encoding="utf-8", suffix=".py"
) as f:
    name = f.name
    f.write(
        f"{final}\n\n\nbpy.ops.{"wm.save_as_mainfile" if stlOrBlend == "blend" else "export_mesh.stl"}\
            (filepath='{path}/{name}.{stlOrBlend}')\n"
    )

print(name)
