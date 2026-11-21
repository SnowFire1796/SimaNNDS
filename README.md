# SimaNNDS — Persian Language Dataset

SimaNNDS is the dataset repository for experiments with the SimaNN language model.

## Repository goals

- Build a compact, inspectable Persian corpus suitable for next-token language-model training.
- Keep raw language-model text separate from instruction/conversation examples.
- Prefer original, coherent Persian material with varied topics and registers.
- Track provenance, normalization, dataset statistics, and limitations.
- Stay practical for low-storage, CPU-only development machines.

## Current contents

- `corpus/`: UTF-8 plain-text documents, including general educational prose and everyday narrative/dialogue. Blank lines separate passages; headings are part of the text.
- `conversations/`: UTF-8 JSONL instruction/response examples. These are auxiliary data and are **not** consumed by the current SimaNN byte-level RNN trainer without a future adapter.
- `manifest.json`: provenance, intended use, and current dataset status.
- `tools/validate_dataset.py`: standard-library-only validation and statistics.

## Important: current data status

The initial material is original synthetic text authored for this repository. It is not a scrape of the Persian web, not a verified encyclopedia, and not a substitute for a professionally curated corpus. It should be treated as a starter corpus for pipeline testing and early experiments, not as sufficient training data for a capable Persian assistant.

No third-party corpus has been imported in this initial batch. The repository license is intentionally left undecided; do not redistribute the data as an openly licensed dataset until the maintainer selects and adds an appropriate license.

## Normalization policy

- Encoding: UTF-8.
- Prefer Persian `ی` (U+06CC) and `ک` (U+06A9).
- Use ZWNJ (U+200C) consistently in compounds where appropriate.
- Preserve punctuation and paragraph boundaries.
- Avoid destructive normalization that changes meaning or removes natural register differences.

## Validation

Run:

```bash
python3 tools/validate_dataset.py
```

The validator checks UTF-8 decoding, empty/duplicate passages, JSONL syntax, required fields, and reports byte/character/word counts. It does not certify factual correctness or linguistic quality.

## Training notes

The current SimaNN implementation is a small byte-level Elman RNN. It can read plain text files, but it has limited capacity and does not perform instruction tuning. For now, use the files under `corpus/` for next-byte prediction experiments. Keep conversation examples separate until a suitable training objective and data loader are implemented.

## Contribution rules

1. Add original or properly licensed material only.
2. Record source, license, collection date, and transformations for external data.
3. Never invent source attribution or license terms.
4. Deduplicate before committing.
5. Keep each batch reasonably sized and record its statistics in the manifest.
