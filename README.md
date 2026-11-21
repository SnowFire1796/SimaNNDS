# SimaNNDS — Persian Language Dataset

SimaNNDS is a compact Persian-language dataset repository for experiments with the SimaNN language model and related text-processing work.

## Repository layout

- `corpus/`: UTF-8 plain-text files for next-token / next-byte language-modeling experiments. Blank lines separate text blocks; each titled section begins with `عنوان:`.
- `conversations/`: UTF-8 JSON Lines (JSONL) instruction/response examples. These are kept separate from raw language-model text.
- `manifest.json`: dataset provenance, intended uses, limitations, normalization policy, and measured statistics.
- `tools/validate_dataset.py`: standard-library-only structural validator and statistics report.

## Current snapshot

Snapshot measured on 2026-11-21:

| Dataset | Files | Sections / examples | Size |
|---|---:|---:|---:|
| Plain-text corpus | 5 | 83 titled sections; 186 blank-line-separated text blocks | 90,157 bytes |
| Conversation examples | 2 | 78 JSONL records | 45,784 bytes |
| **Total** | **7** | **83 sections + 78 conversations** | **135,941 bytes (about 133 KiB)** |

The text corpus contains about 9,021 whitespace-separated tokens. This is a structural count, not a tokenizer-specific token count. The current text blocks and conversation pairs have no exact normalized duplicates according to the repository validator.

Current text files:

- `fa_general_0001.txt`: educational and general explanatory prose.
- `fa_everyday_0001.txt`: everyday scenes, short narratives, and informal dialogue.
- `fa_science_0001.txt`: measurement, probability, materials, acoustics, astronomy, food science, soil, maps, prototyping, and charts.
- `fa_culture_0001.txt`: oral history, photography, theatre, craft, museums, translation, language variation, typography, and responsible visiting.
- `fa_practical_0001.txt`: moving, shared household work, events, bicycle care, cooking, plant observation, appointments, budgeting, and pet responsibility.

Conversation files:

- `fa_dialogue_0001.jsonl`: initial question-and-answer examples.
- `fa_dialogue_0002.jsonl`: additional examples covering writing, data reasoning, software development, accessibility, privacy, and practical communication.

## Data format

Each JSONL line is one independent JSON object. The current schema is:

```json
{
  "instruction": "متن درخواست یا پرسش به فارسی",
  "response": "پاسخ به فارسی",
  "language": "fa",
  "provenance": "assistant_authored_synthetic",
  "split": "train"
}
```

The conversation records are auxiliary instruction data. The current SimaNN byte-level RNN trainer consumes plain text; it does **not** directly train on this JSONL format. A future adapter or a training objective designed for instruction-response pairs is required. Do not concatenate JSONL into the raw corpus as if it were ordinary prose.

## Provenance and limitations

All material currently in this repository is original synthetic Persian text authored specifically for SimaNNDS. No external websites, books, articles, or third-party datasets were imported for these batches. The synthetic examples are not quotations or verified human conversations.

Synthetic text can contain simplifications, omissions, or factual mistakes. It is useful for testing data pipelines and early experiments, but it is not a substitute for a large, diverse, professionally reviewed Persian corpus. The repository does not claim that generated samples represent the frequency or distribution of natural Persian usage.

No repository-wide license has been selected. The data should be treated as **unlicensed / no permission granted for redistribution** until the maintainer chooses and adds an appropriate license. Do not infer a license from the fact that the repository is public.

## Persian text normalization

- Encoding is UTF-8.
- Prefer Persian yeh `ی` (U+06CC) and Persian kaf `ک` (U+06A9), not their Arabic lookalikes.
- Use ZWNJ (U+200C) consistently in compounds and verb prefixes where standard Persian orthography calls for it.
- Normalize Unicode text to NFC where practical.
- Keep ordinary spaces, punctuation, and paragraph boundaries readable.
- Do not apply blind replacements that alter meaning, dialect, quotations, or code snippets.

## Validation

From the repository root, run:

```bash
python3 tools/validate_dataset.py
```

The validator checks UTF-8 decoding, expected Persian yeh/kaf code points, final newlines, duplicate text blocks, JSONL syntax and fields, provenance labels, language/split values, repeated conversation prompts, and byte/character/word statistics. It is a structural check only: it does not verify factual claims, safety, copyright status, or expert-level linguistic quality.

## Training guidance

Use only the files under `corpus/` for the current plain-text SimaNN training path. Keep the conversation JSONL files separate. Because the corpus is small and synthetic, start with pipeline smoke tests and inspect generated samples; do not interpret a falling training loss as evidence that the model has learned reliable facts or conversational ability.

The repository is deliberately text-only and small. It avoids model weights, archives, and other large binary assets so it remains practical to clone and inspect on low-storage, CPU-only computers.

## Contribution rules

1. Add original material or material whose source and license have been verified.
2. Record provenance, generation or collection date, intended use, transformations, and limitations in `manifest.json`.
3. Never invent source attribution, factual certainty, or license terms.
4. Keep raw language-model text separate from instruction/conversation records.
5. Normalize and deduplicate before committing; run the validator after each meaningful batch.
6. Prefer small, reviewable UTF-8 files and meaningful commit messages.
