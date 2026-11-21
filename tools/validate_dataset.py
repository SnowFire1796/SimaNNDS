#!/usr/bin/env python3
"""Validate the SimaNNDS starter corpus using only the Python standard library."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / "corpus"
CHAT_DIR = ROOT / "conversations"


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    text_files = sorted(TEXT_DIR.glob("*.txt"))
    jsonl_files = sorted(CHAT_DIR.glob("*.jsonl"))
    all_passages: list[str] = []
    total_text_bytes = 0
    total_chars = 0
    total_words = 0

    for path in text_files:
        raw = read_utf8(path)
        total_text_bytes += path.stat().st_size
        total_chars += len(raw)
        total_words += len(raw.split())
        passages = [part.strip() for part in raw.split("\n\n") if part.strip()]
        all_passages.extend(passages)
        print(f"TEXT {path.relative_to(ROOT)}: {len(passages)} passages, "
              f"{path.stat().st_size} bytes, {len(raw)} chars")

    normalized = [p.casefold() for p in all_passages]
    duplicates = len(normalized) - len(set(normalized))
    if duplicates:
        errors.append(f"{duplicates} duplicate text passages found")

    conversation_count = 0
    for path in jsonl_files:
        for line_number, line in enumerate(read_utf8(path).splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(item, dict):
                errors.append(f"{path.name}:{line_number}: each JSONL row must be an object")
                continue
            for key in ("instruction", "response"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"{path.name}:{line_number}: missing/non-string {key}")
            conversation_count += 1
        print(f"JSONL {path.relative_to(ROOT)}: {conversation_count} rows checked")

    print("\nTOTALS")
    print(f"Text passages: {len(all_passages)}")
    print(f"Conversation rows: {conversation_count}")
    print(f"Text bytes: {total_text_bytes}")
    print(f"Text characters: {total_chars}")
    print(f"Text whitespace-separated words: {total_words}")
    print(f"Duplicate passages: {duplicates}")

    if errors:
        print("\nERRORS")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nValidation passed (structural checks only; not a factuality or quality audit).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
