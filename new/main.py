import json
from easier_openai import Assistant
from search import search

with open("prompts.json") as f:
    prompts = json.load(f)

inp = input("What do you want to design?\n")

worker = Assistant(system_prompt=prompts["worker_system"], default_conversation=False, model="gpt-5.2")
orchestration = Assistant(system_prompt=prompts["orchestration_system"], default_conversation=True, model="gpt-5.2")

search_terms: str = str(worker.chat(prompts["search_terms"].format(inp=inp)))
print(search_terms + "\n\n\n\n\n\n")

results = [search(i, 1)[0] for i in search_terms.split(",")]

# print(results)
parts = orchestration.chat(prompts["parts_decomposition"].format(inp=inp, results=results)).split(",")

print(parts)
