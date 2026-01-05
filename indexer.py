from bs4 import BeautifulSoup
import pyperclip


def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find(id="furo-main-content")

with open("test.txt", "w") as f:
    with open("html_files/aud.html", "r", encoding="utf-8") as f:
        fu = f.read()
        print(extract_text_from_html(fu).text)
        pyperclip.copy(extract_text_from_html(fu).text)
        f.write(extract_text_from_html(fu).text)
