# SimaNNDS — Persian Language Dataset

SimaNNDS is a compact Persian-language dataset repository for experiments with the SimaNN language model and related text-processing work.

## Repository layout

- `corpus/`: UTF-8 plain-text files for next-token / next-byte language-modeling experiments. Blank lines separate text blocks; each titled section begins with `عنوان:`.
- `conversations/`: UTF-8 JSON Lines (JSONL) instruction/response examples. These are kept separate from raw language-model text.
- `manifest.json`: dataset provenance, intended uses, limitations, normalization policy, and measured statistics.
- `docs/DATASET_CARD.fa.md`: Persian-language data card describing scope, provenance, formats, risks, and licensing status.
- `docs/REVIEW_GUIDE.fa.md`: Persian checklist for human review, source tracking, split discipline, and quality control.
- `tools/validate_dataset.py`: standard-library-only structural validator and statistics report.
- `.github/workflows/validate-dataset.yml`: runs the validator on relevant pushes and pull requests.

## Data card

See [کارت دادهٔ فارسی](docs/DATASET_CARD.fa.md) and the [راهنمای بازبینی انسانی](docs/REVIEW_GUIDE.fa.md).

## Current snapshot

Snapshot measured on 2026-11-21:

| Dataset | Files | Sections / examples | Size |
|---|---:|---:|---:|
| Plain-text corpus | 19 | 262 titled sections; 589 blank-line-separated text blocks | 253,594 bytes |
| Conversation examples | 8 | 242 JSONL records | 139,455 bytes |
| **Total** | **27** | **262 sections + 242 conversations** | **393,049 bytes (about 383.8 KiB)** |

The text corpus contains 25,301 whitespace-separated words. This is a structural count, not a tokenizer-specific token count. The current text blocks and conversation pairs have no exact normalized duplicates according to the repository validator. Semantic near-duplicates are not automatically detected.

Conversation split counts: **train 226**, **validation 8**, **test 8**. These are small synthetic partitions, not an independently reviewed benchmark.

Current text files:

- `fa_general_0001.txt`: educational and general explanatory prose.
- `fa_everyday_0001.txt`: everyday scenes, short narratives, and informal dialogue.
- `fa_science_0001.txt`: measurement, probability, materials, acoustics, astronomy, food science, soil, maps, prototyping, and charts.
- `fa_culture_0001.txt`: oral history, photography, theatre, craft, museums, translation, language variation, typography, and responsible visiting.
- `fa_practical_0001.txt`: moving, shared household work, events, bicycle care, cooking, plant observation, appointments, budgeting, and pet responsibility.
- `fa_digital_0001.txt`: software security, backup, networks, logging, version control, accessibility, metadata, and compression.
- `fa_reasoning_0001.txt`: problem formulation, estimation, units, charts, sampling, probability, algorithms, state machines, and numerical reasoning.
- `fa_observation_0001.txt`: field notes, public spaces, access, household resources, repair, waste, sound, lighting, plants, and product design.
- `fa_infrastructure_0001.txt`: geology, weather observation, urban water and energy systems, rail scheduling, archives, supply chains, quality control, map projections, robotics, and operating systems.
- `fa_urban_0001.txt`: urban mobility, wayfinding, public spaces, building energy, rainwater, oral history, and neighborhood data.
- `fa_food_0001.txt`: food storage, meal planning, labels, soil and irrigation, pollinators, packaging, cooking, and local food narratives.
- `fa_materials_0001.txt`: craft materials, restoration, ceramics, textiles, repairability, life-cycle thinking, and workshop safety.
- `fa_ecology_0001.txt`: wetlands, water sampling, birds, coastal change, biodiversity, waste, light pollution, and climate data.
- `fa_mathematics_0001.txt`: mathematical definitions, proof, functions, probability, geometry, measurement, and modeling.
- `fa_history_methods_0001.txt`: historical sources, chronology, archaeology, oral history, archives, migration, and heritage.
- `fa_economics_civics_0001.txt`: household budgets, inflation, markets, public goods, civic participation, and policy evaluation.
- `fa_linguistics_0001.txt`: phonology, morphology, semantics, translation, Persian orthography, corpus design, and conversation.
- `fa_biology_0001.txt`: cells, enzymes, genetics, evolution, ecology, microbiomes, and experimental design.
- `fa_physics_0001.txt`: mechanics, energy, fluids, heat, electricity, magnetism, waves, optics, and measurement.

Conversation files:

- `fa_dialogue_0001.jsonl`: initial question-and-answer examples.
- `fa_dialogue_0002.jsonl`: examples covering writing, data reasoning, software development, accessibility, privacy, and practical communication.
- `fa_dialogue_0003.jsonl`: additional software, reasoning, accessibility, privacy, writing, debugging, and low-resource computing examples; includes held-out split labels.
- `fa_dialogue_0004.jsonl`: additional original examples on networking, operating systems, databases, compilers, Unicode, robotics, and measurement.
- `fa_dialogue_0005.jsonl` and `fa_dialogue_0006.jsonl`: urban studies, food systems, learning methods, work practices, and data literacy.
- `fa_dialogue_0007.jsonl`: craft, materials, repair, ecology, waste management, and field observation.
- `fa_dialogue_0008.jsonl`: 30 additional train examples covering mathematics, history, economics, linguistics, biology, physics, and scientific reasoning.

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

The allowed split values are `train`, `validation`, and `test`. Keep held-out records out of training. The conversation records are auxiliary instruction data. The current SimaNN byte-level RNN trainer consumes plain text; it does **not** directly train on this JSONL format. A future adapter or a training objective designed for instruction-response pairs is required. Do not concatenate JSONL into the raw corpus as if it were ordinary prose.

## Provenance and limitations

All material currently in this repository is original synthetic Persian text authored specifically for SimaNNDS. No external websites, books, articles, or third-party datasets were imported for these batches. The synthetic examples are not quotations or verified human conversations, and no independent human review is claimed.

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

The validator checks UTF-8 decoding, NFC, Persian yeh/kaf code points, final newlines, trailing whitespace, duplicate text blocks, JSONL syntax and required fields, provenance labels, language/split values, repeated conversation prompts, manifest inventory, and measured statistics. It is a structural check only: it does not verify factual claims, safety, copyright status, semantic similarity, or expert-level linguistic quality.

## Training guidance

Use only the files under `corpus/` for the current plain-text SimaNN training path. Keep the conversation JSONL files separate. Never train on the validation or test records when using them for evaluation. Because the corpus is small and synthetic, start with pipeline smoke tests and inspect generated samples; do not interpret a falling training loss as evidence that the model has learned reliable facts or conversational ability.

The repository is deliberately text-only and small. It avoids model weights, archives, and other large binary assets so it remains practical to clone and inspect on low-storage, CPU-only computers.

## Contribution rules

1. Add original material or material whose source and license have been verified.
2. Record provenance, generation or collection date, intended use, transformations, and limitations in `manifest.json`.
3. Never invent source attribution, factual certainty, or license terms.
4. Keep raw language-model text separate from instruction/conversation records.
5. Normalize and deduplicate before committing; run the validator after each meaningful batch.
6. Prefer small, reviewable UTF-8 files and meaningful commit messages.
