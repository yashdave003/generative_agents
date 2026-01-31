# Eval Sim Enhancement Implementation Summary

**Date**: January 27, 2026
**Status**: Complete

---

## Overview

Three major enhancements were implemented to the evaluation ecosystem simulation:

1. **Visibility System** - Formalized public/private/invisible attribute access
2. **Multi-LLM Support** - Added OpenAI and Ollama provider support
3. **Actor Expansion** - Added Consumer and Policymaker actors

---

## 1. Visibility System

### Design Principle
Invisible state (ground truth) is held **externally by the simulation**, not inside actors. This makes it structurally impossible for LLM prompts to access invisible information.

### Implementation

**New file**: `eval_sim/visibility.py`

```
Actor object (what the actor "knows")
├── public_state: name, published_scores, current_round
└── private_state: beliefs, strategies, history

Simulation object (ground truth, held externally)
└── ground_truth[actor_name]: true_capability, true_satisfaction, etc.
```

### Data Classes

| Class | Visibility | Contents |
|-------|------------|----------|
| `PublicState` | All actors | name, current_round, published_scores |
| `ProviderPrivateState` | Self only | beliefs, strategies, competitor observations |
| `ConsumerPrivateState` | Self only | model quality beliefs, satisfaction history |
| `PolicymakerPrivateState` | Self only | risk beliefs, past interventions |
| `ProviderGroundTruth` | Simulation only | true_capability |
| `ConsumerGroundTruth` | Simulation only | true_satisfaction, true_quality_sensitivity |
| `PolicymakerGroundTruth` | Simulation only | true_risk_tolerance, true_intervention_effectiveness |

### Key Changes
- `ModelProvider` now has `public_state` and `private_state` attributes
- Legacy `scratch` attribute maintained for backwards compatibility
- `Evaluator.evaluate_all()` accepts optional `ground_truth` dict parameter
- `Simulation` holds `ground_truth` dict and passes it to evaluator

---

## 2. Multi-LLM Support

### Architecture

**Modified file**: `eval_sim/llm.py`

```
LLMProvider (Abstract Base Class)
├── OpenAIProvider (GPT-4, GPT-4o-mini)
└── OllamaProvider (llama3, mistral, phi, gemma)
```

### Configuration

Environment variables:
```bash
LLM_PROVIDER=ollama          # or "openai" (default)
LLM_MODEL=llama3             # provider-specific model name
OLLAMA_BASE_URL=http://localhost:11434  # for Ollama
OPENAI_API_KEY=sk-...        # for OpenAI
```

### Usage

```python
from llm import create_llm_provider, get_provider, set_provider

# Create provider from environment
provider = create_llm_provider()

# Or specify explicitly
provider = create_llm_provider("ollama", model="mistral")

# Use for generation
response = provider.generate("Hello", system_prompt="Be helpful")
json_result = provider.generate_json("Output JSON with 'value' key")
```

### Key Interface
```python
class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt, system_prompt=None, temperature=0.7, max_tokens=500) -> str

    @abstractmethod
    def generate_json(self, prompt, system_prompt=None, retries=3, fail_safe=None) -> dict
```

---

## 3. Actor Expansion

### Consumer Actor

**New file**: `eval_sim/actors/consumer.py`

**Purpose**: End user deciding which model to use based on leaderboard

**Behavior Loop**:
1. **Observe**: See leaderboard rankings
2. **Reflect**: Update quality beliefs based on actual experience vs expectations
3. **Plan**: Decide whether to switch models
4. **Execute**: Subscribe/unsubscribe

**Key Dynamic**: Gaming creates satisfaction gap - high score but low true capability leads to disappointed users who switch providers.

**State**:
- PUBLIC: name, current_subscription
- PRIVATE: believed_model_quality, use_cases, budget, satisfaction_history
- INVISIBLE: true_satisfaction

### Policymaker Actor

**New file**: `eval_sim/actors/policymaker.py`

**Purpose**: Regulator who can mandate evaluations or set requirements

**Behavior Loop**:
1. **Observe**: See leaderboard, consumer satisfaction, validity correlation
2. **Reflect**: Update risk assessments
3. **Plan**: Decide whether to intervene
4. **Execute**: Issue regulations

**Intervention Types**:
- `mandate_benchmark`: Change benchmark validity/exploitability
- `require_disclosure`: Require capability/gaming disclosure
- `set_threshold`: Set minimum requirements

**State**:
- PUBLIC: name, active_regulations, public_statements
- PRIVATE: policy_objectives, risk_beliefs, regulatory_capacity
- INVISIBLE: true_risk_tolerance, true_intervention_effectiveness

---

## 4. Simulation Updates

**Modified file**: `eval_sim/simulation.py`

### New Config Options
```python
@dataclass
class SimulationConfig:
    # ... existing fields ...
    enable_consumers: bool = False
    enable_policymakers: bool = False
    n_consumers: int = 10
    n_policymakers: int = 1
```

### Updated Round Flow
```
Each Round:
1. PROVIDERS: plan() → execute() (R&D updates capability in ground_truth)
2. EVALUATOR: evaluate_all(ground_truth) → publish_scores()
3. PROVIDERS: observe() → reflect()
4. CONSUMERS: observe(leaderboard) → reflect() → plan() → execute()
5. POLICYMAKERS: observe(ecosystem_state) → reflect() → plan() → execute()
6. RECORD: Log all actor states and ground truth
```

### History Data Structure
```python
round_data = {
    "round": int,
    "scores": {provider_name: score},
    "true_capabilities": {provider_name: capability},
    "believed_capabilities": {provider_name: belief},
    "strategies": {provider_name: {"rnd": float, "gaming": float}},
    "leaderboard": [(name, score), ...],
    "consumer_data": {  # if consumers enabled
        "subscriptions": {consumer_name: provider_name},
        "satisfaction": {consumer_name: float},
        "avg_satisfaction": float,
        "switches": int,
    },
    "policymaker_data": {  # if policymakers enabled
        "interventions": [{"type": str, "details": dict}, ...],
        "active_regulations": [str, ...],
    },
}
```

---

## 5. Logging Updates

**Modified file**: `eval_sim/experiment_logger.py`

### New Methods
```python
logger.log_consumers(consumers)
logger.log_policymakers(policymakers)
logger.log_ground_truth(ground_truth)
```

### Enhanced Summary
`generate_summary()` now includes:
- `consumer_summary`: n_consumers, mean_satisfaction, final_satisfaction, total_switches
- `policymaker_summary`: n_policymakers, total_interventions, intervention_types, active_regulations

---

## 6. Plotting Updates

**Modified file**: `eval_sim/plotting.py`

### New Functions

```python
# Consumer satisfaction over time + subscription switches
plot_consumer_satisfaction(history, save_path=None, show=True)

# Validity correlation with intervention markers
plot_policymaker_interventions(history, save_path=None, show=True)

# Comprehensive 6-panel dashboard
plot_ecosystem_dashboard(history, save_path=None, show=True)
```

### Dashboard Panels
1. Benchmark Scores Over Time
2. True vs Believed Capability
3. Gaming Investment Over Time
4. Validity Correlation Over Time
5. Consumer Satisfaction (if enabled)
6. Regulatory Interventions (if enabled)

---

## Files Modified/Created

| File | Status | Description |
|------|--------|-------------|
| `eval_sim/visibility.py` | **Created** | Visibility state dataclasses |
| `eval_sim/actors/consumer.py` | **Created** | Consumer actor |
| `eval_sim/actors/policymaker.py` | **Created** | Policymaker actor |
| `eval_sim/actors/model_provider.py` | Modified | Added public/private state split |
| `eval_sim/actors/evaluator.py` | Modified | Accept ground_truth parameter, added Regulation class |
| `eval_sim/actors/__init__.py` | Modified | Export new actors |
| `eval_sim/llm.py` | Modified | Abstract LLMProvider, OpenAI & Ollama providers |
| `eval_sim/simulation.py` | Modified | External ground_truth, consumer/policymaker integration |
| `eval_sim/experiment_logger.py` | Modified | Log new actor states |
| `eval_sim/plotting.py` | Modified | New visualization functions |

---

## Usage Examples

### Basic Simulation (Backwards Compatible)
```python
from simulation import run_default_simulation
sim = run_default_simulation()
```

### Full Ecosystem Simulation
```python
from simulation import EvalEcosystemSimulation, SimulationConfig, get_default_provider_configs

config = SimulationConfig(
    n_rounds=50,
    seed=42,
    enable_consumers=True,
    enable_policymakers=True,
    n_consumers=10,
    llm_mode=False,  # Use heuristics (fast)
)

sim = EvalEcosystemSimulation(config)
sim.setup(get_default_provider_configs())
sim.run()

# Access ground truth (invisible to actors)
print(sim.ground_truth["AlphaTech"].true_capability)
```

### Using Ollama for LLM Mode
```bash
# Start Ollama
ollama serve

# Set environment
export LLM_PROVIDER=ollama
export LLM_MODEL=llama3

# Run simulation with LLM
python -c "
from simulation import EvalEcosystemSimulation, SimulationConfig, get_default_provider_configs
config = SimulationConfig(n_rounds=10, llm_mode=True)
sim = EvalEcosystemSimulation(config)
sim.setup(get_default_provider_configs())
sim.run()
"
```

---

## Verification Checklist

- [x] Providers can't access each other's private state
- [x] LLM prompts contain only public + private state (no ground truth)
- [x] Logger can access all state including ground truth
- [x] `LLM_PROVIDER=openai` works (existing behavior)
- [x] `LLM_PROVIDER=ollama` works with local models
- [x] Consumer observes leaderboard and subscribes to top-ranked model
- [x] Consumer experiences true satisfaction based on true_capability
- [x] Gaming leads to satisfaction gap
- [x] Policymaker observes leaderboard and consumer incidents
- [x] Policymaker can issue regulations
- [x] Full integration with all actors works

---

## Future Enhancements (Not Implemented)

1. **Funder Actor**: Capital allocator influencing which providers/evaluations survive
2. **Enhanced Evaluator**: Active benchmark adaptation, gaming detection
3. **vLLM Provider**: High-throughput local inference
4. **HuggingFace Provider**: Direct model loading
5. **Anthropic Provider**: Claude API support

---

## Dependencies

Required:
- `numpy`
- `matplotlib`

Optional (for LLM mode):
- `openai` (for OpenAI provider)
- `requests` (for Ollama provider)
