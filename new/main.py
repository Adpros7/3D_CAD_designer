import json
from easier_openai import Assistant
from search import search

with open(r"C:\Users\prani\Coding\AI\3D_CAD_designer\new\prompts.json") as f:
    prompts = json.load(f)

userInput = input("What do you want to design?\n")

workerAgent = Assistant(system_prompt=prompts["worker_system"], default_conversation=False, model="gpt-5.2")
orchestrationAgent = Assistant(system_prompt=prompts["orchestration_system"], default_conversation=True, model="gpt-5.2")

searchTerms: str = str(workerAgent.chat(prompts["search_terms"].format(inp=userInput)))
print(searchTerms + "\n\n\n\n\n\n")

searchResults = [search(i.strip(), 1)[0] if len(search(i.strip(), 1)) > 0 else None for i in searchTerms.split(",")]

print(searchResults)
modelParts = orchestrationAgent.chat(prompts["parts_decomposition"].format(inp=userInput, results=searchResults)).split(",")

partResults = []
for i in modelParts:
    partResults.append(workerAgent.chat(f"Your part in the project"))


