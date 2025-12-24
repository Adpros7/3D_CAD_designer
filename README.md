# 3D CAD / Blender Designer

A desktop helper that turns natural-language prompts into Blender Python scripts. The app pairs an OpenAI-powered assistant with a lightweight local search index of Blender documentation so you can generate, review, and copy ready-to-run code directly from a Tkinter UI.

## Features
- Tkinter desktop window for quick prompting and code retrieval.
- OpenAI assistant tuned for Blender's Python API to translate requirements into runnable scripts.
- Local TF-IDF index over downloaded Blender HTML docs for fast context retrieval.
- Automatic clipboard copy of generated code and optional download format hinting (`stl`, `blend`, or no download).

## Prerequisites
- **Python:** 3.13.9 (use `pyenv install 3.13.9` if needed).
- **OpenAI credentials:** set `OPENAI_API_KEY` (or the key expected by `easier-openai`) before running the app.
- **Blender documentation:** place HTML files under `html_files/` (see below for downloading tips).
- Optional: `virtualenv` or `python -m venv` for isolated dependencies.

## Installation
1. **Clone the repo**
   ```bash
   git clone <repo-url>
   cd 3D_CAD_designer
   ```

2. **Select Python 3.13.9** (recommended)
   ```bash
   pyenv install 3.13.9  # if not already available
   pyenv local 3.13.9
   ```

3. **Create and activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Preparing Blender HTML docs
The search helper expects Blender documentation pages stored locally:
1. Download the Blender manual as HTML ("Offline Manual") from the Blender docs site. [Download ZIP] (https://docs.blender.org/api/current/blender_python_reference_5_0.zip)
2. Extract the archive and copy the HTML files into `html_files/` at the project root (keep filenames intact).
3. The search cache is written to `.search_cache/index.joblib`; it is built automatically on first run.

## Building the search index (optional pre-warm)
You can force the TF-IDF index to build before launching the UI:
```bash
python -m search
```
This reads `html_files/` and stores the cache under `.search_cache/`. Subsequent runs reuse the cache unless HTML files change.

## Running the app
1. Ensure your API key environment variable is exported.
2. Start the Tkinter UI:
   ```bash
   python main.py
   ```
3. In the window:
   - Enter a natural-language requirement (e.g., "generate a torus knot mesh with adjustable twists").
   - Choose a download hint from the dropdown (`stl`, `blend`, or `no download`).
   - Click **Generate Code**.
4. The assistant searches relevant docs, generates Blender Python code, prints it to the console, and automatically copies it to your clipboard. A "Code Copied to Clipboard" label appears when generation finishes.

## Troubleshooting
- **Clipboard not updating:** ensure a desktop environment is available; `pyperclip` may require additional system packages on some platforms.
- **Index build is slow:** remove `.search_cache/` and rerun `python -m search` after trimming `html_files/` to only the docs you need.
- **API errors:** verify `OPENAI_API_KEY` is set and your network allows outbound requests.
- **Python version mismatch:** align with `3.13.9` for best compatibility or adjust `pyproject.toml`/`.python-version` if pinning a different interpreter.

## License
[MIT](https://choosealicense.com/licenses/mit/)


## Notes

README create by codex AI.
