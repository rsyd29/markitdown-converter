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
        "progress_chunk": "  Mengonversi potongan {current}/{total} ...",
        "progress_whisper": "Mengonversi dengan Whisper lokal ...",
        "convert_failed": "  [x] Gagal mengonversi: {error}",
        "empty_result": "  [x] Hasil konversi kosong.",
        "audio_missing_deps": (
            "      Petunjuk: transkripsi audio butuh backend. Pasang salah satu:\n"
            '      - Google (online):  pip install "markitdown[audio-transcription]"\n'
            "      - Whisper (offline): pip install faster-whisper"
        ),
        "audio_missing_ffmpeg": (
            "      Petunjuk: ffmpeg belum terpasang (dibutuhkan untuk mp3).\n"
            "      Pasang dengan: brew install ffmpeg"
        ),
        "audio_no_speech": "  [x] Tidak ada ucapan yang terdeteksi pada audio ini.",
        "audio_network_error": (
            "  [x] Transkripsi gagal: layanan Google tidak terjangkau (broken pipe/timeout).\n"
            "      Cek koneksi internet, VPN/proxy, atau firewall — atau pasang Whisper\n"
            "      lokal untuk transkripsi offline: pip install faster-whisper"
        ),
        "audio_language_title": "\n  Pilih bahasa audio:",
        "audio_language_id": "    1) Bahasa Indonesia",
        "audio_language_en": "    2) English",
        "audio_language_auto": "    3) Otomatis (deteksi)",
        "audio_language_prompt": "  Pilihan (1-3): ",
        "audio_language_invalid": "  [!] Pilihan tidak valid. Masukkan 1-3.",
        "convert_success": "  [✓] Konversi berhasil ({count} karakter, {seconds:.1f} detik).",
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
        "progress_chunk": "  Transcribing chunk {current}/{total} ...",
        "progress_whisper": "Transcribing with local Whisper ...",
        "convert_failed": "  [x] Conversion failed: {error}",
        "empty_result": "  [x] The conversion result is empty.",
        "audio_missing_deps": (
            "      Hint: audio transcription needs a backend. Install either:\n"
            '      - Google (online):  pip install "markitdown[audio-transcription]"\n'
            "      - Whisper (offline): pip install faster-whisper"
        ),
        "audio_missing_ffmpeg": (
            "      Hint: ffmpeg is not installed (required for mp3).\n"
            "      Install it with: brew install ffmpeg"
        ),
        "audio_no_speech": "  [x] No speech was detected in this audio file.",
        "audio_network_error": (
            "  [x] Transcription failed: Google's service is unreachable (broken pipe/timeout).\n"
            "      Check your internet connection, VPN/proxy, or firewall — or install\n"
            "      local Whisper for offline transcription: pip install faster-whisper"
        ),
        "audio_language_title": "\n  Choose the audio language:",
        "audio_language_id": "    1) Indonesian",
        "audio_language_en": "    2) English",
        "audio_language_auto": "    3) Auto-detect",
        "audio_language_prompt": "  Choice (1-3): ",
        "audio_language_invalid": "  [!] Invalid choice. Enter 1-3.",
        "convert_success": "  [✓] Conversion succeeded ({count} characters, {seconds:.1f}s).",
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
