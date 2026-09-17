"""Translation strings (i18n) for the MarkItDown Converter CLI.

Each language maps the same set of keys to translated text. When adding a new
string to the CLI, add its key to every language table in ``TRANSLATIONS``.
"""

from __future__ import annotations

#: Language used when an unknown or unsupported code is requested.
DEFAULT_LANGUAGE = "en"

#: Maps the number typed at the language menu to a language code.
LANGUAGE_CHOICES: dict[str, str] = {
    "1": "id",
    "2": "en",
}

#: Bilingual strings for the language-selection menu itself.
LANGUAGE_MENU: dict[str, str] = {
    "title": "Pilih bahasa / Choose language:",
    "option_id": "    1) Bahasa Indonesia",
    "option_en": "    2) English",
    "prompt": "  Pilihan / Choice (1/2): ",
    "invalid": "  [!] Pilihan tidak valid. Masukkan 1 atau 2."
    " / Invalid choice. Enter 1 or 2.",
}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "id": {
        "formats": (
            "PDF, PowerPoint (pptx), Word (docx), Excel (xlsx/xls), CSV, HTML, "
            "XML, JSON, TXT, Markdown, RTF, ODT, ODP, ODS, EPUB, Outlook (msg), "
            "gambar, audio (wav/mp3), dan lainnya"
        ),
        "banner_supported": "  Format yang didukung: {formats}",
        "banner_quit": "  Ketik 'q' kapan saja untuk keluar.",
        "prompt_file_path": "Path file yang ingin diubah: ",
        "file_not_found": "  [!] File tidak ditemukan: {path}",
        "not_a_file": "  [!] Bukan sebuah file: {path}",
        "output_naming_title": "\n  Pilih penamaan file hasil:",
        "output_option_same": "    1) Sama seperti file asli (hanya ekstensi menjadi .md)",
        "output_option_custom": "    2) Nama / path kustom",
        "prompt_choice": "  Pilihan (1/2): ",
        "prompt_custom_name": "  Nama file (boleh sertakan path lengkap): ",
        "invalid_choice_1_2": "  [!] Pilihan tidak valid. Masukkan 1 atau 2.",
        "converting": "\n  Mengonversi '{name}' ...",
        "convert_failed": "  [x] Gagal mengonversi: {error}",
        "empty_result": "  [x] Hasil konversi kosong.",
        "convert_success": "  [✓] Konversi berhasil ({count} karakter).",
        "overwrite_prompt": "  File '{path}' sudah ada. Timpa? (y/n): ",
        "cancelled": "  Dibatalkan.",
        "saved": "  [✓] Tersimpan di: {path}",
        "goodbye": "  Sampai jumpa!",
        "interrupted": "\n\n  Dihentikan. Sampai jumpa!",
    },
    "en": {
        "formats": (
            "PDF, PowerPoint (pptx), Word (docx), Excel (xlsx/xls), CSV, HTML, "
            "XML, JSON, TXT, Markdown, RTF, ODT, ODP, ODS, EPUB, Outlook (msg), "
            "images, audio (wav/mp3), and more"
        ),
        "banner_supported": "  Supported formats: {formats}",
        "banner_quit": "  Type 'q' at any time to exit.",
        "prompt_file_path": "Path of the file to convert: ",
        "file_not_found": "  [!] File not found: {path}",
        "not_a_file": "  [!] Not a file: {path}",
        "output_naming_title": "\n  Choose how to name the output file:",
        "output_option_same": "    1) Same as the source file (only the extension changes to .md)",
        "output_option_custom": "    2) Custom name / path",
        "prompt_choice": "  Choice (1/2): ",
        "prompt_custom_name": "  File name (may include a full path): ",
        "invalid_choice_1_2": "  [!] Invalid choice. Enter 1 or 2.",
        "converting": "\n  Converting '{name}' ...",
        "convert_failed": "  [x] Conversion failed: {error}",
        "empty_result": "  [x] The conversion result is empty.",
        "convert_success": "  [✓] Conversion succeeded ({count} characters).",
        "overwrite_prompt": "  File '{path}' already exists. Overwrite? (y/n): ",
        "cancelled": "  Cancelled.",
        "saved": "  [✓] Saved to: {path}",
        "goodbye": "  Goodbye!",
        "interrupted": "\n\n  Interrupted. Goodbye!",
    },
}


def get_translations(language: str) -> dict[str, str]:
    """Return the string table for ``language``, falling back to the default."""
    return TRANSLATIONS.get(language, TRANSLATIONS[DEFAULT_LANGUAGE])
