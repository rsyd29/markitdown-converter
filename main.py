#!/usr/bin/env python3
"""MarkItDown CLI Converter.

Convert various file types (PDF, PPTX, DOCX, XLSX, CSV, HTML, etc.)
into Markdown using Microsoft's `markitdown` library.

The interface language (Indonesian or English) is chosen at startup.

Usage:
    python main.py
"""

from __future__ import annotations

import sys
from pathlib import Path

from markitdown import MarkItDown

from i18n import LANGUAGE_CHOICES, LANGUAGE_MENU, get_translations


def clean_input(raw: str) -> str:
    """Clean input: strip whitespace and surrounding quotes from the path."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        raw = raw[1:-1].strip()
    return raw


def choose_language() -> dict[str, str]:
    """Ask the user to pick a language and return its string table."""
    print("=" * 60)
    print("        MarkItDown Converter — File to Markdown")
    print("=" * 60)
    print(LANGUAGE_MENU["title"])
    print(LANGUAGE_MENU["option_id"])
    print(LANGUAGE_MENU["option_en"])

    while True:
        choice = clean_input(input(LANGUAGE_MENU["prompt"]))
        if choice in LANGUAGE_CHOICES:
            return get_translations(LANGUAGE_CHOICES[choice])
        print(LANGUAGE_MENU["invalid"])


def print_banner(t: dict[str, str]) -> None:
    print("-" * 60)
    print(t["banner_supported"].format(formats=t["formats"]))
    print(t["banner_quit"])
    print("-" * 60)


def pick_source_file(t: dict[str, str]) -> Path:
    """Prompt for the source file path until the user enters a valid file."""
    while True:
        raw = clean_input(input(t["prompt_file_path"]))
        if raw.lower() in {"q", "quit", "exit"}:
            print(t["goodbye"])
            sys.exit(0)
        if not raw:
            continue

        path = Path(raw).expanduser()
        if not path.exists():
            print(t["file_not_found"].format(path=path))
            continue
        if not path.is_file():
            print(t["not_a_file"].format(path=path))
            continue
        return path.resolve()


def ensure_md_extension(path: Path) -> Path:
    """Ensure the path ends with .md (replace/add the extension if needed)."""
    if path.suffix.lower() == ".md":
        return path
    if path.suffix:
        return path.with_suffix(".md")
    return Path(f"{path}.md")


def choose_output_path(source: Path, t: dict[str, str]) -> Path:
    """Determine where to save the converted Markdown file."""
    print(t["output_naming_title"])
    print(t["output_option_same"])
    print(t["output_option_custom"])

    while True:
        choice = clean_input(input(t["prompt_choice"]))
        if choice == "1":
            return source.with_suffix(".md")

        if choice == "2":
            raw = clean_input(input(t["prompt_custom_name"]))
            if not raw:
                continue
            path = Path(raw).expanduser()
            # If it's just a name without a directory, save it next to the source.
            if path.parent == Path("."):
                path = source.parent / path.name
            return ensure_md_extension(path).resolve()

        print(t["invalid_choice_1_2"])


def convert_file(source: Path, md: MarkItDown, t: dict[str, str]) -> str | None:
    """Convert the file; return the Markdown content or None on failure."""
    print(t["converting"].format(name=source.name))
    try:
        result = md.convert(str(source))
    except Exception as exc:  # noqa: BLE001 — show all errors in a friendly way
        print(t["convert_failed"].format(error=exc))
        return None

    content = (getattr(result, "markdown", None) or result.text_content or "").strip()
    if not content:
        print(t["empty_result"])
        return None

    print(t["convert_success"].format(count=len(content)))
    return content


def save_file(destination: Path, content: str, t: dict[str, str]) -> None:
    """Save the Markdown content to the destination, confirming if it exists."""
    if destination.exists():
        answer = clean_input(t["overwrite_prompt"].format(path=destination)).lower()
        if answer not in {"y", "yes"}:
            print(t["cancelled"])
            return

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")
    print(t["saved"].format(path=destination))


def main() -> None:
    t = choose_language()
    print_banner(t)
    md = MarkItDown()

    try:
        while True:
            print()
            source = pick_source_file(t)

            content = convert_file(source, md, t)
            if content is None:
                continue

            destination = choose_output_path(source, t)
            save_file(destination, content, t)
    except KeyboardInterrupt:
        print(t["interrupted"])
        sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Raised while choosing the language, before a string table exists.
        print("\n\n  Dihentikan. Sampai jumpa! / Interrupted. Goodbye!")
        sys.exit(0)
