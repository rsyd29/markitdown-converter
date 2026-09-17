#!/usr/bin/env bash
# Menjalankan MarkItDown Converter: buat virtual environment (bila belum ada),
# pasang dependency, lalu jalankan aplikasi.

set -e

# Pindah ke direktori tempat skrip ini berada (agar bisa dijalankan dari mana saja).
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Buat virtual environment bila belum ada.
if [ ! -d ".venv" ]; then
    echo "Membuat virtual environment (.venv) ..."
    python3 -m venv .venv
fi

# Aktifkan virtual environment.
source .venv/bin/activate

# Pasang dependency.
echo "Memasang dependency ..."
pip install -r requirements.txt

# Jalankan aplikasi.
python main.py
