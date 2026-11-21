#!/usr/bin/env python3
"""Structural validation and statistics for the SimaNNDS Persian datasets.

Uses only the Python standard library. It does not judge factuality, safety,
copyright status, semantic similarity, or expert linguistic quality.
"""
from __future__ import annotations

# Structural checks are necessary, but they do not replace factual or human review.

import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT_DIR = ROOT / "corpus"
CHAT_DIR = ROOT / "conversations"
MANIFEST_PATH = ROOT / "manifest.json"
ARABIC_FORMS = {"\u064a": "\u06cc", "\u0649": "\u06cc", "\u0643": "\u06a9"}
SYNTHETIC_LABEL = "assistant_authored_synthetic"


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def comparison_key(value: str) -> str:
    value = unicodedata.normalize("NFC", value)
    value = value.translate(str.maketrans(ARABIC_FORMS))
    return " ".join(value.split()).casefold()


def inspect_text(value: str, label: str, errors: list[str]) -> None:
    if unicodedata.normalize("NFC", value) != value:
        errors.append(f"{label}: text is not Unicode NFC-normalized")
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
    for line_number, line in enumerate(value.splitlines(), 1):
        if line.endswith((" ", "\t")):
            errors.append(f"{label}:{line_number}: trailing whitespace")


def main() -> int:
    errors: list[str] = []
    text_files = sorted(TEXT_DIR.glob("*.txt"))
    conversation_files = sorted(CHAT_DIR.glob("*.txt"))
    if not text_files:
        errors.append("no corpus/*.txt files found")
    if not conversation_files:
        errors.append("no conversations/*.txt dialogue files found")

    all_blocks: list[str] = []
    total_text_bytes = total_text_chars = total_text_words = 0
    total_text_sections = 0
    total_conversation_bytes = 0
    total_conversation_examples = 0
    conversation_keys: set[str] = set()
    instruction_keys: set[str] = set()
    duplicate_pairs = 0
    duplicate_instructions = 0
    split_counts = {"train": 0, "validation": 0, "test": 0}

    for path in text_files:
        raw = read_utf8(path)
        size = path.stat().st_size
        total_text_bytes += size
        total_text_chars += len(raw)
        total_text_words += len(raw.split())
        blocks = [part.strip() for part in re.split(r"\n\s*\n", raw) if part.strip()]
        sections = len(re.findall(r"^عنوان:", raw, flags=re.MULTILINE))
        total_text_sections += sections
        all_blocks.extend(blocks)
        inspect_text(raw, str(path.relative_to(ROOT)), errors)
        if not raw:
            errors.append(f"{path.relative_to(ROOT)}: empty text file")
        if raw and not raw.endswith("\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
        print(
            f"TEXT {path.relative_to(ROOT)}: {sections} titled sections, "
            f"{len(blocks)} text blocks, {size} bytes"
        )

    block_keys = [comparison_key(block) for block in all_blocks]
    duplicate_blocks = len(block_keys) - len(set(block_keys))
    if duplicate_blocks:
        errors.append(f"{duplicate_blocks} duplicate normalized text blocks found")

    for path in conversation_files:
        raw = read_utf8(path)
        size = path.stat().st_size
        total_conversation_bytes += size
        inspect_text(raw, str(path.relative_to(ROOT)), errors)
        split = path.stem.split("_")[2] if len(path.stem.split("_")) >= 4 else ""
        if split not in split_counts:
            errors.append(f"{path.name}: filename must identify train, validation, or test split")
            continue
        local_count = 0
        blocks = [part.strip() for part in re.split(r"\\n\\s*\\n", raw) if part.strip()]
        for index, block in enumerate(blocks, 1):
            lines = block.splitlines()
            if len(lines) < 3 or not lines[0].startswith("نمونه ") or not lines[1].startswith("پرسش: ") or not lines[2].startswith("پاسخ: "):
                errors.append(f"{path.name}: block {index} must contain a numbered sample, پرسش, and پاسخ")
                continue
            instruction = lines[1][len("پرسش: "):]
            response = "\\n".join(lines[2:])[len("پاسخ: "):]
            if not instruction.strip() or not response.strip():
                errors.append(f"{path.name}: block {index} has an empty instruction or response")
                continue
            if instruction != instruction.strip() or response != response.strip():
                errors.append(f"{path.name}: block {index} has outer whitespace")
                continue
            inspect_text(instruction, f"{path.name}:{index}:instruction", errors)
            inspect_text(response, f"{path.name}:{index}:response", errors)
            instruction_key = comparison_key(instruction)
            pair_key = instruction_key + "\\u241f" + comparison_key(response)
            if pair_key in conversation_keys:
                duplicate_pairs += 1
            conversation_keys.add(pair_key)
            if instruction_key in instruction_keys:
                duplicate_instructions += 1
            instruction_keys.add(instruction_key)
            split_counts[split] += 1
            local_count += 1
            total_conversation_examples += 1
        if raw and not raw.endswith("\\n"):
            errors.append(f"{path.relative_to(ROOT)}: missing final newline")
        print(f"DIALOGUE {path.relative_to(ROOT)}: {local_count} valid examples, {size} bytes")

    if duplicate_pairs:
        errors.append(f"{duplicate_pairs} duplicate conversation pairs found")
    if duplicate_instructions:
        errors.append(f"{duplicate_instructions} repeated conversation instructions found")

    total_data_bytes = total_text_bytes + total_conversation_bytes
    actual_stats = {
        "text_files": len(text_files),
        "conversation_files": len(conversation_files),
        "text_sections": total_text_sections,
        "text_blocks": len(all_blocks),
        "conversation_examples": total_conversation_examples,
        "text_bytes": total_text_bytes,
        "conversation_bytes": total_conversation_bytes,
        "total_data_bytes": total_data_bytes,
        "text_characters_including_whitespace": total_text_chars,
        "text_whitespace_separated_words": total_text_words,
        "exact_normalized_duplicate_text_blocks": duplicate_blocks,
        "exact_duplicate_conversation_pairs": duplicate_pairs,
        "repeated_conversation_instructions": duplicate_instructions,
        "conversation_split_counts": split_counts,
    }

    try:
        manifest = json.loads(read_utf8(MANIFEST_PATH))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        errors.append(f"manifest.json: cannot read valid UTF-8 JSON: {exc}")
        manifest = {}

    if not isinstance(manifest, dict):
        errors.append("manifest.json: top-level value must be an object")
        manifest = {}

    manifest_files = manifest.get("files", [])
    if not isinstance(manifest_files, list):
        errors.append("manifest.json: files must be a list")
        manifest_files = []
    listed_paths = [
        entry.get("path")
        for entry in manifest_files
        if isinstance(entry, dict) and isinstance(entry.get("path"), str)
    ]
    manifest_paths = set(listed_paths)
    if len(listed_paths) != len(manifest_paths):
        errors.append("manifest.json: duplicate file entries found")
    actual_paths = {
        str(path.relative_to(ROOT)) for path in text_files + conversation_files
    }
    if manifest_paths != actual_paths:
        missing = sorted(actual_paths - manifest_paths)
        stale = sorted(manifest_paths - actual_paths)
        errors.append(f"manifest file inventory mismatch; unregistered={missing}, missing_on_disk={stale}")

    for entry in manifest_files:
        if not isinstance(entry, dict):
            errors.append("manifest files entries must be objects")
            continue
        path = entry.get("path", "<unknown>")
        if entry.get("provenance") != SYNTHETIC_LABEL:
            errors.append(f"manifest {path}: provenance must be {SYNTHETIC_LABEL}")
        if not entry.get("generation_date"):
            errors.append(f"manifest {path}: generation_date is required")
        if not entry.get("intended_use"):
            errors.append(f"manifest {path}: intended_use is required")
        if not entry.get("license"):
            errors.append(f"manifest {path}: license status must be stated")
        if entry.get("third_party_material") is not False:
            errors.append(f"manifest {path}: third_party_material must be false or explicitly reviewed")

    provenance_policy = manifest.get("provenance_policy", {})
    if not isinstance(provenance_policy, dict):
        errors.append("manifest provenance_policy must be an object")
        provenance_policy = {}
    if provenance_policy.get("synthetic_label") != SYNTHETIC_LABEL:
        errors.append("manifest provenance_policy has an unexpected synthetic label")
    if provenance_policy.get("external_sources") != []:
        errors.append("manifest external_sources must list every verified external source (currently expected empty)")

    recorded_stats = manifest.get("statistics", {})
    for key, value in actual_stats.items():
        if recorded_stats.get(key) != value:
            errors.append(f"manifest statistics mismatch for {key}: recorded={recorded_stats.get(key)!r}, actual={value!r}")

    print("\nTOTALS")
    for key, value in actual_stats.items():
        print(f"{key}: {value}")

    if errors:
        print("\nERRORS")
        for error in errors:
            print(f"- {error}")
        return 1
    print("\nStructural validation passed. This does not certify factual correctness, safety, licensing, or linguistic quality.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
