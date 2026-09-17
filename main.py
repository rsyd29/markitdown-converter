#!/usr/bin/env python3
"""MarkItDown CLI Converter.

Convert various file types (PDF, PPTX, DOCX, XLSX, CSV, HTML, etc.)
into Markdown using Microsoft's `markitdown` library.

The interface language (Indonesian or English) is chosen at startup.

Usage:
    python main.py
"""

from __future__ import annotations

import importlib.util
import io
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Any, Self

from markitdown import MarkItDown

from i18n import LANGUAGE_CHOICES, LANGUAGE_MENU, get_translations


def clean_input(raw: str) -> str:
    """Clean input: strip whitespace and surrounding quotes from the path."""
    raw = raw.strip()
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in ("'", '"'):
        raw = raw[1:-1].strip()
    return raw


class Progress:
    """Show an animated spinner and elapsed time while work is running.

    When stdout is not a terminal, it prints the message once instead of
    animating, but still records the elapsed time.
    """

    _FRAMES = ("|", "/", "-", "\\")

    def __init__(self, message: str) -> None:
        self._message = message
        self._done = threading.Event()
        self._thread: threading.Thread | None = None
        self.elapsed = 0.0

    def __enter__(self) -> Self:
        self._start = time.monotonic()
        if sys.stdout.isatty():
            self._thread = threading.Thread(target=self._animate, daemon=True)
            self._thread.start()
        else:
            print(self._message)
        return self

    def __exit__(self, *exc_info: object) -> None:
        self.elapsed = time.monotonic() - self._start
        if self._thread is not None:
            self._done.set()
            self._thread.join()
            sys.stdout.write("\r" + " " * 80 + "\r")
            sys.stdout.flush()

    def _animate(self) -> None:
        frame = 0
        while not self._done.is_set():
            elapsed = time.monotonic() - self._start
            sys.stdout.write(
                f"\r  {self._FRAMES[frame % len(self._FRAMES)]} "
                f"{self._message} ({elapsed:.1f}s)"
            )
            sys.stdout.flush()
            frame += 1
            self._done.wait(0.1)


#: Audio formats handled by markitdown's audio converter.
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".mp4"}

#: Google's free speech service drops the connection on large single requests,
#: so audio is transcribed in chunks, downmixed to 16 kHz mono to keep each
#: upload small. Transient connection errors are retried a few times.
AUDIO_CHUNK_MS = 60_000
AUDIO_SAMPLE_RATE = 16_000
AUDIO_CHANNELS = 1
AUDIO_RETRIES = 3
AUDIO_RETRY_DELAY_S = 1.5

#: Local Whisper model used when Google's service is unreachable. Smaller
#: models ("tiny", "base") run faster on CPU; larger ones ("medium", "large")
#: are more accurate but slower. "small" is a good accuracy/speed balance.
WHISPER_MODEL = "small"

#: Segments with a higher "no speech" probability are treated as silence/music
#: and skipped, which prevents Whisper from hallucinating text on non-speech.
WHISPER_NO_SPEECH_THRESHOLD = 0.6


def is_audio(path: Path) -> bool:
    """Return True if the file is an audio format handled by markitdown."""
    return path.suffix.lower() in AUDIO_EXTENSIONS


def audio_dependencies_installed() -> bool:
    """Return True if the packages needed for Google transcription are available."""
    return (
        importlib.util.find_spec("pydub") is not None
        and importlib.util.find_spec("speech_recognition") is not None
    )


def whisper_available() -> bool:
    """Return True if the local Whisper transcription backend is installed."""
    return importlib.util.find_spec("faster_whisper") is not None


#: Maps the audio language menu choice to (Google tag, Whisper code). ``None``
#: for either value means "auto-detect".
AUDIO_LANGUAGE_CHOICES: dict[str, tuple[str | None, str | None]] = {
    "1": ("id-ID", "id"),
    "2": ("en-US", "en"),
    "3": (None, None),
}


def choose_audio_language(t: dict[str, str]) -> tuple[str | None, str | None]:
    """Prompt for the audio transcription language."""
    print(t["audio_language_title"])
    print(t["audio_language_id"])
    print(t["audio_language_en"])
    print(t["audio_language_auto"])

    while True:
        choice = clean_input(input(t["audio_language_prompt"]))
        if choice in AUDIO_LANGUAGE_CHOICES:
            return AUDIO_LANGUAGE_CHOICES[choice]
        print(t["audio_language_invalid"])


def recognize_chunk(recognizer: Any, data: Any, language: str | None) -> str | None:
    """Transcribe one chunk with Google, retrying transient connection errors.

    Returns the chunk text (possibly empty for silence), or ``None`` when the
    service is unreachable.
    """
    import speech_recognition as sr

    for attempt in range(1, AUDIO_RETRIES + 1):
        try:
            if language:
                return recognizer.recognize_google(data, language=language)
            return recognizer.recognize_google(data)
        except sr.UnknownValueError:
            # Silence or unintelligible speech in this chunk is not fatal.
            return ""
        except sr.RequestError:
            if attempt < AUDIO_RETRIES:
                time.sleep(AUDIO_RETRY_DELAY_S * attempt)
    return None


def transcribe_google(source: Path, t: dict[str, str], language: str | None) -> str | None:
    """Transcribe an audio file with Google, chunk by chunk.

    Returns the transcript, or ``None`` if the service is unreachable.
    """
    import pydub
    import speech_recognition as sr

    segment = pydub.AudioSegment.from_file(str(source))
    recognizer = sr.Recognizer()
    parts: list[str] = []
    total = (len(segment) + AUDIO_CHUNK_MS - 1) // AUDIO_CHUNK_MS

    for index, start in enumerate(range(0, len(segment), AUDIO_CHUNK_MS), start=1):
        print(t["progress_chunk"].format(current=index, total=total))
        chunk = segment[start : start + AUDIO_CHUNK_MS]
        chunk = chunk.set_frame_rate(AUDIO_SAMPLE_RATE).set_channels(AUDIO_CHANNELS)

        buffer = io.BytesIO()
        chunk.export(buffer, format="wav")
        buffer.seek(0)

        with sr.AudioFile(buffer) as audio_file:
            data = recognizer.record(audio_file)

        text = recognize_chunk(recognizer, data, language)
        if text is None:
            return None
        if text:
            parts.append(text)

    return " ".join(parts)


def transcribe_whisper(source: Path, language: str | None) -> str:
    """Transcribe an audio file locally with faster-whisper (works offline)."""
    from faster_whisper import WhisperModel

    model = WhisperModel(WHISPER_MODEL, device="auto", compute_type="int8")
    segments, _info = model.transcribe(
        str(source),
        language=language,
        vad_filter=True,
        condition_on_previous_text=False,
    )
    return " ".join(
        segment.text.strip()
        for segment in segments
        if segment.text.strip()
        and segment.no_speech_prob < WHISPER_NO_SPEECH_THRESHOLD
    )


def transcribe_audio(
    source: Path,
    t: dict[str, str],
    google_language: str | None,
    whisper_language: str | None,
) -> tuple[str, str | None]:
    """Transcribe an audio file, preferring Google and falling back to Whisper.

    Returns ``(transcript, error)``. ``error`` is ``None`` on success, and
    ``"network"`` or ``"no_speech"`` otherwise.
    """
    google_text = (
        transcribe_google(source, t, google_language)
        if audio_dependencies_installed()
        else None
    )

    # Fall back to local Whisper when Google failed to connect or found no
    # speech (Whisper is more robust at detecting speech).
    whisper_ran = False
    whisper_text = ""
    if (google_text is None or not google_text.strip()) and whisper_available():
        try:
            with Progress(t["progress_whisper"]):
                whisper_text = transcribe_whisper(source, whisper_language)
            whisper_ran = True
        except Exception:  # noqa: BLE001 — best-effort fallback, any failure means no text
            whisper_text = ""

    if whisper_text.strip():
        return whisper_text.strip(), None

    # Whisper ran successfully but found no speech (e.g. music or silence).
    if whisper_ran:
        return "", "no_speech"

    if google_text is None:
        return "", "network"
    if not google_text.strip():
        return "", "no_speech"
    return google_text.strip(), None


def convert_audio(source: Path, t: dict[str, str]) -> str | None:
    """Convert an audio file into a Markdown transcript."""
    if not audio_dependencies_installed() and not whisper_available():
        print(t["audio_missing_deps"])
        return None
    if shutil.which("ffmpeg") is None:
        print(t["audio_missing_ffmpeg"])
        return None

    google_language, whisper_language = choose_audio_language(t)

    print(t["converting"].format(name=source.name))
    started = time.monotonic()
    try:
        transcript, error = transcribe_audio(
            source, t, google_language, whisper_language
        )
    except Exception as exc:  # noqa: BLE001 — report decoding/other failures
        print(t["convert_failed"].format(error=exc))
        return None
    elapsed = time.monotonic() - started

    if error == "network":
        print(t["audio_network_error"])
        return None
    if error == "no_speech":
        print(t["audio_no_speech"])
        return None

    content = f"### Audio Transcript:\n{transcript}"
    print(t["convert_success"].format(count=len(content), seconds=elapsed))
    return content


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
    # Audio uses a dedicated chunked transcription path, see convert_audio().
    if is_audio(source):
        return convert_audio(source, t)

    message = t["converting"].format(name=source.name)
    try:
        with Progress(message) as progress:
            result = md.convert(str(source))
    except Exception as exc:  # noqa: BLE001 — show all errors in a friendly way
        print(t["convert_failed"].format(error=exc))
        return None

    content = (getattr(result, "markdown", None) or result.text_content or "").strip()
    if not content:
        print(t["empty_result"])
        return None

    print(t["convert_success"].format(count=len(content), seconds=progress.elapsed))
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
