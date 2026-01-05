import os
from bs4 import BeautifulSoup
import pyperclip


def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id="furo-main-content")

os.mkdir("blender_docs") if not os.path.exists("blender_docs") else None
for file in os.listdir("html_files"):
    with open(f"C:\Users\prani\Coding\AI\3D_CAD_designer\html_files{file}", "r", encoding="utf-8") as fl:
        fu = fl.read()
    with open(f"blender_docs/{file.removesuffix('.html')}.md", "w") as f:
        f.write(extract_text_from_html(fu).text)
