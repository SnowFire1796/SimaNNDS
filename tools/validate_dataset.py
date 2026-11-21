#!/usr/bin/env python3
"""Structural checks and compact statistics for the SimaNNDS datasets.

Uses only the Python standard library. This is not a factuality or expert
linguistic-quality evaluator.
"""
from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / "corpus"
CHAT_DIR = ROOT / "conversations"
ARABIC_FORMS = {"\u064a": "\u06cc", "\u0649": "\u06cc", "\u0643": "\u06a9"}


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def comparison_key(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.translate(str.maketrans(ARABIC_FORMS))
    return " ".join(value.split()).casefold()


def inspect_persian_text(value: str, label: str, errors: list[str]) -> None:
    for char, description in (
        ("\u064a", "Arabic yeh U+064A"),
        ("\u0649", "alef maksura U+0649"),
        ("\u0643", "Arabic kaf U+0643"),
    ):
        if char in value:
            errors.append(f"{label}: contains {description}; use Persian ی/ک consistently")
    if "\ufeff" in value:
        errors.append(f"{label}: contains a UTF-8 BOM inside the content")
    if "\x00" in value:
        errors.append(f"{label}: contains a NUL character")


def main() -> int:
    errors: list[str] = []
    text_files = sorted(TEXT_DIR.glob("*.txt"))
    jsonl_files = sorted(CHAT_DIR.glob("*.jsonl"))
    if not text_files:
        errors.append("no corpus/*.txt files found")
    if not jsonl_files:
        errors.append("no conversations/*.jsonl files found")

    all_blocks: list[str] = []
    total_text_bytes = total_text_chars = total_text_words = 0
    total_text_sections = 0
    total_all_bytes = 0

    for path in text_files:
        raw = read_utf8(path)
        size = path.stat().st_size
        total_text_bytes += size
        total_all_bytes += size
        total_text_chars += len(raw)
        total_text_words += len(raw.split())
        blocks = [part.strip() for part in re.split(r"\n\s*\n", raw) if part.strip()]
        sections = len(re.findall(r"^عنوان:", raw, flags=re.MULTILINE))
        total_text_sections += sections
        all_blocks.extend(blocks)
        inspect_persian_text(raw, str(path.relative_to(ROOT)), errors)
        if raw and not raw.endswith("\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
        print(
            f"TEXT {path.relative_to(ROOT)}: {sections} titled sections, "
            f"{len(blocks)} text blocks, {size} bytes"
        )

    block_keys = [comparison_key(block) for block in all_blocks]
    duplicate_blocks = len(block_keys) - len(set(block_keys))
    if duplicate_blocks:
        errors.append(f"{duplicate_blocks} duplicate text blocks found")

    conversation_count = 0
    total_conversation_bytes = 0
    conversation_keys: set[str] = set()
    instruction_keys: set[str] = set()
    duplicate_pairs = 0
    duplicate_instructions = 0

    for path in jsonl_files:
        raw = read_utf8(path)
        size = path.stat().st_size
        total_conversation_bytes += size
        total_all_bytes += size
        local_count = 0
        for line_number, line in enumerate(raw.splitlines(), 1):
            if not line.strip():
                errors.append(f"{path.name}:{line_number}: blank JSONL line")
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                errors.append(f"{path.name}:{line_number}: invalid JSON: {exc}")
                continue
            if not isinstance(item, dict):
                errors.append(f"{path.name}:{line_number}: each JSONL row must be an object")
                continue

            valid = True
            for key in ("instruction", "response"):
                if not isinstance(item.get(key), str) or not item[key].strip():
                    errors.append(f"{path.name}:{line_number}: missing/non-string {key}")
                    valid = False
            if item.get("language") != "fa":
                errors.append(f"{path.name}:{line_number}: language must be 'fa'")
                valid = False
            if item.get("provenance") != "assistant_authored_synthetic":
                errors.append(f"{path.name}:{line_number}: provenance must be explicit")
                valid = False
            if item.get("split") not in {"train", "validation", "test"}:
                errors.append(f"{path.name}:{line_number}: split must be train, validation, or test")
                valid = False
            for key in ("instruction", "response"):
                value = item.get(key)
                if isinstance(value, str):
                    inspect_persian_text(value, f"{path.name}:{line_number}:{key}", errors)
            if not valid:
                continue

            instruction_key = comparison_key(item["instruction"])
            pair_key = instruction_key + "\u241f" + comparison_key(item["response"])
            if pair_key in conversation_keys:
                duplicate_pairs += 1
            conversation_keys.add(pair_key)
            if instruction_key in instruction_keys:
                duplicate_instructions += 1
            instruction_keys.add(instruction_key)
            local_count += 1
            conversation_count += 1

        if raw and not raw.endswith("\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
        print(f"JSONL {path.relative_to(ROOT)}: {local_count} valid examples, {size} bytes")

    if duplicate_pairs:
        errors.append(f"{duplicate_pairs} duplicate conversation pairs found")
    if duplicate_instructions:
        errors.append(f"{duplicate_instructions} repeated conversation instructions found")

    print("\nTOTALS")
    print(f"Text sections: {total_text_sections}")
    print(f"Text blocks: {len(all_blocks)}")
    print(f"Conversation examples: {conversation_count}")
    print(f"Text bytes: {total_text_bytes}")
    print(f"Conversation bytes: {total_conversation_bytes}")
    print(f"Total dataset bytes: {total_all_bytes}")
    print(f"Text characters: {total_text_chars}")
    print(f"Text whitespace-separated words: {total_text_words}")
    print(f"Duplicate text blocks: {duplicate_blocks}")
    print(f"Duplicate conversation pairs: {duplicate_pairs}")
    print(f"Repeated conversation instructions: {duplicate_instructions}")

    if errors:
        print("\nERRORS")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nStructural validation passed. This does not certify factual correctness or linguistic quality.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
