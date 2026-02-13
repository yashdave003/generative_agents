# Heuristic Experiments

This directory contains fast heuristic-mode experiments (no LLM planning).

## Numbering

Heuristic experiments use a **separate numbering sequence** from the main experiments:
- Main experiments: `exp_001_...`, `exp_002_...` (tracked in `../index.json`)
- Heuristic experiments: `heur_001_...`, `heur_002_...` (tracked in `heuristic_index.json`)

This separation allows for rapid iteration with heuristic runs without polluting the main experiment numbering sequence.

## Directory Structure

```
experiments/
├── index.json              # Main experiments (LLM mode, curated runs)
├── exp_001_name/
├── exp_002_name/
└── heuristic/
    ├── heuristic_index.json    # Heuristic experiments only
    ├── heur_001_name/
    ├── heur_002_name/
    └── README.md (this file)
```

## Running Heuristic Experiments

Set `llm_mode = False` in `run_experiment.py` and the logger will automatically use this subdirectory.

## Purpose

Heuristic mode is useful for:
- Fast iteration on simulation mechanics
- Parameter sweeps
- Debugging
- Baseline comparisons
- Quick what-if scenarios

LLM mode (main experiments/) is for:
- Final runs
- Publishable results
- Deep agent behavior analysis
- Experiments with emergent LLM reasoning
