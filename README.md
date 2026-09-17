# MarkItDown Converter

**English** | [Bahasa Indonesia](README.id.md)

A simple CLI app to convert **PDF, PowerPoint, Word, Excel**, and many other
formats into **Markdown**, powered by Microsoft's
[`markitdown`](https://github.com/microsoft/markitdown) library.

## Features

- Converts many formats: PDF, PPTX, DOCX, XLSX/XLS, CSV, HTML, XML, JSON, TXT,
  RTF, ODT, ODP, ODS, EPUB, Outlook (msg), images, audio, and more.
- Interactive CLI UI — just enter the file path.
- Choose the interface language (Indonesian or English) at startup.
- Output Markdown can use a custom name, or automatically reuse the source
  file's name with the extension changed to `.md`.
- Handles missing files, failed conversions, and overwrite confirmation when
  the output file already exists.

## Requirements

- Python 3.10 or newer
- `pip`

## Installation

```bash
cd markitdown-converter

# Create a virtual environment (if you don't have one yet)
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

> A virtual environment (`.venv`) is already included in this project. If it
> exists, just activate it with `source .venv/bin/activate`.

> The dependencies above cover the main document formats (PDF, Word,
> PowerPoint, Excel, and Outlook). Other basic formats (CSV, HTML, XML, JSON,
> TXT, EPUB, etc.) are supported without extra dependencies.
>
> If you need advanced features, you can add more extras, for example:
> - `audio-transcription` — audio transcription (wav/mp3, requires `ffmpeg`)
> - `youtube-transcription` — YouTube video transcription
> - `az-doc-intel` / `az-content-understanding` — Azure services (requires credentials)
> - or `markitdown[all]` to install everything at once

## Usage

Make sure the dependencies are installed (see [Installation](#installation)).

### macOS / Linux

```bash
# Activate the virtual environment, then run
source .venv/bin/activate
python main.py
```

Or run directly without activating the venv:

```bash
.venv/bin/python main.py
```

Since `main.py` is executable and has a shebang, this also works:

```bash
source .venv/bin/activate
./main.py
```

### Windows

```bash
# Activate the virtual environment (Command Prompt / PowerShell)
.venv\Scripts\activate
python main.py
```

Or run directly without activating the venv:

```bash
.venv\Scripts\python.exe main.py
```

Then follow the steps:

1. Choose the interface language: `1` for Bahasa Indonesia, `2` for English.
2. Enter the path of the file to convert, for example:
   - `report.pdf`
   - `presentation.pptx`
   - `/Users/name/Documents/document.docx`
3. The program converts the file and shows the resulting character count.
4. Choose how to name the output file:
   - `1` → same name as the source (only the extension changes to `.md`)
   - `2` → custom name/path (if just a name, it is saved in the source folder)
5. The Markdown file is saved. The program then asks for the next file.

Type `q` at any time to exit.

## Project structure

```
markitdown-converter/
├── main.py           # Main program (CLI)
├── i18n.py           # Translation strings (Indonesian/English)
├── requirements.txt  # Dependencies
├── README.md         # Documentation (English)
├── README.id.md      # Documentation (Indonesian)
└── LICENSE           # MIT License
```

## Troubleshooting

- **Editor shows "Import markitdown could not be resolved"** — the `markitdown`
  package is already installed in the environment. Reload the Python language
  server (in Zed: `Cmd+Shift+P` → *language server: restart*, or *Reload
  Window*) so its index is refreshed.
- **A file fails to convert for a specific format** — make sure the relevant
  extras are installed (see the Installation section).

## License

Released under the [MIT License](LICENSE).
