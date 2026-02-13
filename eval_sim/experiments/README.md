# Experiments Directory

This directory contains all simulation experiments, organized into two tracks:

## Directory Structure

```
experiments/
├── index.json                  # Main experiments (LLM mode, curated)
├── exp_001_name/              # Main experiment
├── exp_002_name/
├── ...
└── heuristic/                 # Heuristic experiments (separate numbering)
    ├── heuristic_index.json
    ├── heur_001_name/
    ├── heur_002_name/
    └── ...
```

## Two Experiment Tracks

### Main Experiments (`exp_XXX_*`)
- **Purpose**: Curated, important experiments with LLM planning
- **Numbering**: Sequential (`exp_001`, `exp_002`, ...) tracked in `index.json`
- **When to use**: Final runs, publishable results, deep agent reasoning analysis
- **Settings**: `llm_mode = True` in `run_experiment.py`

### Heuristic Experiments (`heuristic/heur_XXX_*`)
- **Purpose**: Fast iteration, parameter sweeps, debugging, baselines
- **Numbering**: Separate sequence (`heur_001`, `heur_002`, ...) tracked in `heuristic/heuristic_index.json`
- **When to use**: Quick what-if scenarios, mechanics testing, rapid iteration
- **Settings**: `llm_mode = False` in `run_experiment.py`

## Rationale

Heuristic runs are 10-100x faster than LLM runs, making them ideal for:
- Testing new features
- Parameter exploration
- Debugging simulation logic
- Baseline comparisons

By keeping them in a separate subdirectory with separate numbering, you can run hundreds of heuristic experiments without polluting the main experiment sequence.

## Experiment Data

Each experiment directory (both main and heuristic) contains:
- `metadata.json` - Description, tags, timestamp, git commit
- `config.json` - Full simulation configuration
- `history.json` - Round-by-round data
- `rounds.jsonl` - Streaming round data (one JSON per line)
- `summary.json` - Final aggregate metrics
- `ground_truth.json` - True capability values
- `game_log.md` - Human-readable narrative
- `plots/` - Visualization dashboards
- `providers/`, `consumer_market/`, `policymakers/`, `funders/` - Actor state snapshots

## Finding Experiments

**List all main experiments:**
```bash
cat experiments/index.json
```

**List all heuristic experiments:**
```bash
cat experiments/heuristic/heuristic_index.json
```

**Count experiments:**
```bash
ls -d exp_* | wc -l                    # Main experiments
ls -d heuristic/heur_* | wc -l         # Heuristic experiments
```
