# SimaNNDS — Persian Language Dataset

SimaNNDS is a compact Persian-language dataset repository for experiments with the SimaNN language model and related text-processing work.

## Repository layout

- `corpus/`: UTF-8 plain-text files for next-token / next-byte language-modeling experiments. Blank lines separate text blocks; each titled section begins with `عنوان:`.
- `conversations/`: UTF-8 plain-text instruction/response examples. Train, validation, and test are separate files.
- `manifest.json`: dataset provenance, intended uses, limitations, normalization policy, and measured statistics.
- `docs/DATASET_CARD.fa.md`: Persian-language data card describing scope, provenance, formats, risks, and licensing status.
- `docs/REVIEW_GUIDE.fa.md`: Persian checklist for human review, source tracking, split discipline, and quality control.
- `tools/validate_dataset.py`: standard-library-only structural validator and statistics report.
- `.github/workflows/validate-dataset.yml`: runs the validator on relevant pushes and pull requests.

## Data card

See [کارت دادهٔ فارسی](docs/DATASET_CARD.fa.md), the [راهنمای بازبینی انسانی](docs/REVIEW_GUIDE.fa.md), and the [راهنمای پیکره‌های بزرگ بیرونی](docs/EXTERNAL_CORPORA.fa.md).

## Current snapshot

Snapshot measured on 2026-11-21:

| Dataset | Files | Sections / examples | Size |
|---|---:|---:|---:|
| Plain-text corpus | 37 | 683 titled sections; 3031 blank-line-separated text blocks | 1,226,018 bytes |
| Plain-text dialogue | 3 | 242 پرسش/پاسخ records (226 train, 8 validation, 8 test) | 122,088 bytes |
| **Total** | **40** | **683 sections + 242 dialogue records** | **1,348,106 bytes** |

The raw text corpus contains 124,113 whitespace-separated words. Dialogue records are stored separately. This is a structural count, not a tokenizer-specific token count. The current text blocks and conversation pairs have no exact normalized duplicates according to the repository validator. Semantic near-duplicates are not automatically detected.

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

- `fa_computer_science_0001.txt`: binary representation, memory hierarchy, operating systems, networking, APIs, software testing, and maintenance.
- `fa_astronomy_0001.txt`: sky observation, stars and planets, lunar phases, spectra, telescopes, cosmic distances, and light pollution.
- `fa_chemistry_0001.txt`: matter, atoms, chemical bonds, reactions, acids and bases, solutions, and reaction rates.
- `fa_statistics_0001.txt`: sampling, descriptive statistics, correlation, uncertainty, hypothesis testing, missing data, and visualization.
- `fa_geography_0001.txt`: map scales, projections, coordinates, climate, watersheds, urban heat, and human geography.
- `fa_engineering_0001.txt`: requirements, prototyping, tolerances, energy efficiency, safety, repairability, and life-cycle assessment.
- `fa_literature_0001.txt`: narrative perspective, characterization, dialogue, metaphor, editing, and literary criticism.
- `fa_law_civics_0001.txt`: legal rules, rights and responsibilities, contracts, privacy, public institutions, and dispute resolution.

- `fa_programming_languages_0001.txt`: language design, compilation, type systems, memory, concurrency, debugging, and code readability.
- `fa_algorithms_0001.txt`: algorithm analysis, searching, sorting, data structures, graph traversal, dynamic programming, and correctness proofs.
- `fa_machine_learning_0001.txt`: dataset splits, leakage, loss functions, optimization, neural networks, byte-level language models, and evaluation.
- `fa_electronics_0001.txt`: charge, current, voltage, resistance, circuits, capacitors, diodes, transistors, and circuit diagrams.
- `fa_education_0001.txt`: learning objectives, active recall, spaced review, feedback, problem solving, note-taking, and assessment.
- `fa_sound_0001.txt`: sound waves, reflection, timbre, rhythm, recording quality, and hearing safety.
- `fa_agriculture_0001.txt`: soil, irrigation, biodiversity, integrated pest management, germination, and harvest storage.
- `fa_energy_systems_0001.txt`: energy conversion, electricity grids, solar generation, building insulation, storage, and efficiency.

Dialogue files:

- `fa_dialogue_train_0001.txt`: 226 training examples.
- `fa_dialogue_validation_0001.txt`: 8 held-out validation examples.
- `fa_dialogue_test_0001.txt`: 8 held-out test examples.

Each record contains a numbered sample, `پرسش:`, and `پاسخ:`. The split is represented by the filename; never mix validation or test into training.

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

The validator checks UTF-8 decoding, NFC, Persian yeh/kaf code points, final newlines, trailing whitespace, duplicate text blocks, numbered dialogue-record structure, train/validation/test file naming, repeated prompts, manifest inventory, and measured statistics. It is a structural check only: it does not verify factual claims, safety, copyright status, semantic similarity, or expert-level linguistic quality.

## Training guidance

Use files under `corpus/` for raw prose and `conversations/fa_dialogue_train_0001.txt` for dialogue training. Keep validation and test files held out. Never train on the validation or test records when using them for evaluation. Because the corpus is small and synthetic, start with pipeline smoke tests and inspect generated samples; do not interpret a falling training loss as evidence that the model has learned reliable facts or conversational ability.

The repository is deliberately text-only and small. It avoids model weights, archives, and other large binary assets so it remains practical to clone and inspect on low-storage, CPU-only computers.

## Contribution rules

1. Add original material or material whose source and license have been verified.
2. Record provenance, generation or collection date, intended use, transformations, and limitations in `manifest.json`.
3. Never invent source attribution, factual certainty, or license terms.
4. Keep raw language-model text separate from instruction/conversation records.
5. Normalize and deduplicate before committing; run the validator after each meaningful batch.
6. Prefer small, reviewable UTF-8 files and meaningful commit messages.


### Large synthetic expansion (2026-11-21)

A new multi-domain TXT volume adds advanced material on networking, database systems, defensive cybersecurity, operating systems, compiler architecture, robotics and control, signal processing, numerical methods, geology and climate, public policy, media literacy, research methods, economics, biology, and product design. The material is assistant-authored synthetic prose, not an independently verified reference corpus; human review is still required.


A second large synthetic volume adds advanced Persian material on astronomy, geographic information systems, logistics, AI ethics, learning science, manufacturing, energy, applied statistics, cultural heritage, food systems, water resources, digital forensics, biotechnology, transport, environmental management, linguistics, research ethics, and software testing. All new material is explicitly labeled synthetic and awaits human review.
