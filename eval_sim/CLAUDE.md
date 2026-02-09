# Project: AI Evaluation Ecosystem Simulation (eval_sim)

## Environment

- **OS:** Windows (native, NOT WSL)
- **Shell:** PowerShell / cmd — do NOT use bash-isms (e.g. `uname`, `make`, `zip`)
- **Python:** 3.12
- **Paths:** Use forward slashes or raw strings. Never assume Unix paths.
- **Package manager:** pip

## Project Paths

- **Project root:** `C:\Users\yashd\Desktop\generative_agents\eval_sim\`
- Always search from the project root, not from `/` or `~`
- Key entry points:
  - `run_experiment.py` — editable experiment config file (edit & run)
  - `run_llm_now.py` — CLI-driven quick experiments
  - `simulation.py` — core sim loop, provider config presets

## Working Style

- When the user asks to investigate or fix something, ask for context if unsure rather than spending many turns exploring the codebase
- Do not solve extra problems or add unrequested features
- When editing JSON files (especially `experiments/index.json`), validate syntax after editing — trailing commas have caused failures multiple times
- Before long-running experiments, do a preflight check: validate JSON configs, test LLM provider connectivity, verify output directory exists

## Jupyter Notebooks

- Do NOT use NotebookEdit to create or edit notebooks — it fails frequently
- Instead, provide code as copy-paste snippets in chat
- When working on homework problems, only address the specific problem requested

## Simulation Architecture

- Three-tier visibility: PublicState, PrivateState, GroundTruth (held by sim)
- Actors: ModelProvider, Evaluator, Consumer, Policymaker, Funder
- Provider investment portfolio: fundamental_research, training_optimization, evaluation_engineering, safety_alignment
- Providers use either heuristic or LLM mode for planning
- LLM providers: openai, anthropic, ollama, gemini (set via `LLM_PROVIDER` env var)
- Experiment results logged to `experiments/` via ExperimentLogger
- Incremental round logging: `rounds.jsonl` (one JSON line per round, written live)
