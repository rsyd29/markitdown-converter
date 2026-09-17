#!/usr/bin/env python3
"""MarkItDown CLI Converter.

Mengonversi berbagai jenis file (PDF, PPTX, DOCX, XLSX, CSV, HTML, dll.)
menjadi Markdown menggunakan pustaka `markitdown` dari Microsoft.

Cara pakai:
    python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from markitdown import MarkItDown


# Daftar ekstensi yang umum didukung markitdown. Dipakai hanya sebagai info,
# bukan untuk memblokir file — konversi tetap dicoba apa pun ekstensinya.
SUPPORTED_FORMATS = (
    "PDF, PowerPoint (pptx), Word (docx), Excel (xlsx/xls), CSV, HTML, "
    "XML, JSON, TXT, Markdown, RTF, ODT, ODP, ODS, EPUB, Outlook (msg), "
    "gambar, audio (wav/mp3), dan lainnya"
)


def clean_input(raw: str) -> str:
    """Bersihkan input: buang spasi dan tanda kutip di sekitar path."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        raw = raw[1:-1].strip()
    return raw


def print_banner() -> None:
    print("=" * 60)
    print("        MarkItDown Converter — File to Markdown")
    print("=" * 60)
    print(f"  Format yang didukung: {SUPPORTED_FORMATS}")
    print("  Ketik 'q' kapan saja untuk keluar.")
    print("-" * 60)


def pick_source_file() -> Path:
    """Minta path file sumber sampai pengguna memasukkan file yang valid."""
    while True:
        raw = clean_input(input("Path file yang ingin diubah: "))
        if raw.lower() in {"q", "quit", "exit"}:
            print("  Sampai jumpa!")
            sys.exit(0)
        if not raw:
            continue

        path = Path(raw).expanduser()
        if not path.exists():
            print(f"  [!] File tidak ditemukan: {path}")
            continue
        if not path.is_file():
            print(f"  [!] Bukan sebuah file: {path}")
            continue
        return path.resolve()


def ensure_md_extension(path: Path) -> Path:
    """Pastikan path berakhiran .md (ganti/tambah ekstensi bila perlu)."""
    if path.suffix.lower() == ".md":
        return path
    if path.suffix:
        return path.with_suffix(".md")
    return Path(f"{path}.md")


def choose_output_path(source: Path) -> Path:
    """Tentukan lokasi penyimpanan file Markdown hasil konversi."""
    print("\n  Pilih penamaan file hasil:")
    print("    1) Sama seperti file asli (hanya ekstensi menjadi .md)")
    print("    2) Nama / path kustom")

    while True:
        choice = clean_input(input("  Pilihan (1/2): "))
        if choice == "1":
            return source.with_suffix(".md")

        if choice == "2":
            raw = clean_input(input("  Nama file (boleh sertakan path lengkap): "))
            if not raw:
                continue
            path = Path(raw).expanduser()
            # Jika hanya nama tanpa folder, simpan di folder yang sama dgn sumber.
            if path.parent == Path("."):
                path = source.parent / path.name
            return ensure_md_extension(path).resolve()

        print("  [!] Pilihan tidak valid. Masukkan 1 atau 2.")


def convert_file(source: Path, md: MarkItDown) -> str | None:
    """Konversi file, kembalikan isi Markdown atau None bila gagal."""
    print(f"\n  Mengonversi '{source.name}' ...")
    try:
        result = md.convert(str(source))
    except Exception as exc:  # noqa: BLE001 — tampilkan semua error dgn ramah
        print(f"  [x] Gagal mengonversi: {exc}")
        return None

    content = (getattr(result, "markdown", None) or result.text_content or "").strip()
    if not content:
        print("  [x] Hasil konversi kosong.")
        return None

    print(f"  [✓] Konversi berhasil ({len(content)} karakter).")
    return content


def save_file(destination: Path, content: str) -> None:
    """Simpan isi Markdown ke tujuan, dengan konfirmasi bila sudah ada."""
    if destination.exists():
        answer = clean_input(
            f"  File '{destination}' sudah ada. Timpa? (y/n): "
        ).lower()
        if answer not in {"y", "yes"}:
            print("  Dibatalkan.")
            return

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    print(f"  [✓] Tersimpan di: {destination}")


def main() -> None:
    print_banner()
    md = MarkItDown()

    while True:
        print()
        source = pick_source_file()

        content = convert_file(source, md)
        if content is None:
            continue

        destination = choose_output_path(source)
        save_file(destination, content)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n  Dihentikan. Sampai jumpa!")
        sys.exit(0)
