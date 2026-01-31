# Reputational Damage: AI Ecosystem Stakeholders

## 1. Individual Consumer

**Role:** End-user deciding whether and how to use or deploy AI models for personal or professional tasks.

### Internal State (What they have)
- Possible AI use cases
- Set of tasks they might engage in
- Prior beliefs about model capabilities
- Prior beliefs about leaderboard usefulness and trustworthiness
  - Including which evaluations matter for their use cases
- Available resources (time, money)

### Observable Inputs (What they observe)
- Leaderboard rankings
- Model scores
- Popularity of each leaderboard
- Popularity of each model
- Availability of relevant evaluations
- Perceived quality of evaluations

### Observable Outputs (What they can do)
- Subscribe to a model provider
- Query a model
- Participate in LM Arena
- Visit leaderboard websites
- Decide to abstain or commit to using/deploying a model
- Aggregate outputs across multiple models

## 2. Organizational Consumer (e.g., Hospitals, Enterprises)

**Role:** Institutions adopting AI systems under operational, regulatory, and integration constraints.

### Internal State (What they have)
- Institutional needs for AI-supported tasks
- Integration friction with existing systems
- Budget and resource allocation constraints
- Organizational expertise
- Open question: how private internal knowledge can inform evaluations

### Observable Inputs (What they observe)
- Leaderboard rankings
- Regulatory and compliance requirements (e.g., HIPAA, GDPR)
- Cost of certification and compliance
- Operational costs of organizational subscriptions
- Decision-making timelines (longer than individuals)
- Population of clients/users/patients
- External incentives to signal AI adoption (e.g., for investment)

### Observable Outputs (What they can do)
- Develop lightweight or specialized model alternatives
- Combine multiple models into compound AI systems
- Design human–AI team workflows
- Influence outcomes for clients/users/patients

## 3. Policymaker

**Role:** Regulatory and governance actor shaping AI deployment, evaluation, and compliance.

### Internal State (What they have)
- Policy priorities and objectives
- Prior beliefs about risks and societal benefits of models
- Prior beliefs about leaderboard trustworthiness
- Beliefs about which evaluations are useful
- Resources (time, money)
- Expertise to interpret evaluations correctly

### Observable Inputs (What they observe)
- Leaderboard rankings
- Model scores
- Availability of relevant evaluations
- Perceived legitimacy and quality of evaluations
- Non-public information from model developers
  - e.g., compliance or reporting requirements

### Observable Outputs (What they can do)
- Require developers to run specific evaluations
- Propose new regulations
- Commission new evaluation designs
- Request third-party evaluations (e.g., via AISI)
- Negotiate with developers
- Enforce sanctions or fines
- Issue warnings or information requests
- Signal policy direction
- Define thresholds for regulatory action

## 4. Model Provider (e.g., OpenAI)

**Role:** Developer and distributor of AI models, optimizing performance, adoption, and valuation.

### Internal State (What they have)
- Financial and compute resources
- Technical expertise (model development, evaluation optimization)
- Beliefs about investor priorities
- Stock market valuation
- Costs associated with development effort
- Data access
- Internal performance metrics

### Observable Inputs (What they observe)
- Leaderboard rankings
- Model outputs (including rich internal performance data)
- User engagement metrics and pairwise comparisons
- Competitor actions
- Contract negotiations among other actors
- Public benchmark design choices (e.g., Elo ratings)
- Data released by evaluation providers
- Popularity of leaderboards

### Observable Outputs (What they can do)
- Release new models
- Adjust training and optimization effort (e.g., RLHF, data scaling)
- Design ML pipelines (data collection, fine-tuning decisions)
- Lobby policymakers
- Withdraw models from the market
- Invest in specific research directions
- Negotiate contracts (compute, data centers, funding)

## 5. Evaluation Provider (e.g., HELM, METR)

**Role:** Designer and operator of benchmarks, evaluations, and metrics.

### Internal State (What they have)
- Financial and compute resources
- Benchmark and metric design choices (e.g., Elo, retries, cost)
- Conceptual ideas for evaluation constructs
- Societal concerns and priorities
- Risk-based prioritization of task types and use cases

### Observable Inputs (What they observe)
- Benchmark popularity (e.g., citations in reports)
- Demand from model providers and policymakers
- Funding availability
- Policy and regulatory changes
- Emerging tools and use cases
- New AI products
- Leaderboard rankings and benchmark scores
- Individual prediction-level data

### Observable Outputs (What they can do)
- Develop new evaluation content
- Design or revise metrics and benchmark structure
- Discontinue existing evaluations
- Incentivize capability development via benchmarks
- Sell metrics, benchmarks, or data
  - To providers, policymakers, or product designers
  - Includes auditing tools and services

## 6. Funder (e.g., AISI, Foundations, Venture Capital)

**Role:** Capital allocator influencing which models, evaluations, and research directions advance.

### Internal State (What they have)
- Financial and compute resources
- Desired financial or political returns on investment
- Mission-driven beliefs about beneficial AI advancements
- Committees of decision-makers and experts

### Observable Inputs (What they observe)
- Leaderboard rankings
- Benchmark popularity
- Success and growth of model providers
- Leadership positioning of providers

### Observable Outputs (What they can do)
- Issue calls for funding proposals
- Decide funding amounts
- Select priority evaluation constructs or research areas
- Choose which actors or projects to fund

---

# Simulation Model: Evaluation Ecosystem Dynamics

This section describes how actors are computationally modeled in the `eval_sim/` simulation framework. The simulation studies how benchmark-based competition between model providers can lead to Goodhart's law dynamics, where optimizing for a measure causes it to cease being a good measure of the underlying construct.

## Core Concepts

### Constructs vs. Measures
A fundamental tension exists between what we want to measure (the **construct**, e.g., "reasoning ability") and what we actually measure (the **benchmark score**). When providers optimize for the benchmark, the correlation between score and construct degrades over time.

### The Scoring Model
Observed benchmark scores are generated as:

```
score ~ Normal(α × true_capability + β × evaluation_engineering × exploitability, σ²)
```

Where:
- `α` (validity): How well the benchmark measures the true construct
- `β` (exploitability): Property of the benchmark (how susceptible to optimization)
- `evaluation_engineering`: Provider's investment in benchmark-specific optimization
- `σ²` (noise): Irreducible variance in evaluation

**Key insight:** Providers don't directly observe `α`, `β`, or `exploitability`. They only see realized scores and must *infer* these properties. Crucially, "gaming" is not an explicit choice—it emerges from rational investment in evaluation engineering.

---

## Simulated Actor: Model Provider

**Purpose:** Represents organizations developing and releasing AI models in a competitive market.

### State Variables

#### Observable State (known to the provider)
| Variable | Description |
|----------|-------------|
| `name` | Unique identifier |
| `last_score` | Most recent benchmark score received |
| `past_scores` | History of all scores |
| `past_strategies` | History of strategy choices |
| `competitor_scores` | Published scores of other providers |

#### Hidden State (ground truth, not directly observable)
| Variable | Description |
|----------|-------------|
| `true_capability` | Actual capability level (what benchmarks should measure) |

#### Belief State (uncertain estimates, updated over time)
| Variable | Description |
|----------|-------------|
| `believed_own_capability` | Provider's estimate of their true capability |
| `believed_benchmark_exploitability` | Provider's estimate of how gameable the benchmark is |
| `believed_competitor_capabilities` | Estimates of competitors' true capabilities |

#### Investment Portfolio (decisions made each round)
Providers allocate resources across four investment areas. These must sum to 1.0 (100% of effort budget).

| Investment | Description | Effect on Capability | Effect on Score |
|------------|-------------|---------------------|-----------------|
| `fundamental_research` | Novel architectures, pre-training improvements, breakthrough research | High (1.5× efficiency), high variance | Indirect (via capability) |
| `training_optimization` | Scaling, data quality, fine-tuning, infrastructure | Moderate (1.0× efficiency), reliable | Indirect (via capability) |
| `evaluation_engineering` | Benchmark-specific optimization, prompt tuning for evals | Minimal (0.1× efficiency) | Direct boost via exploitability |
| `safety_alignment` | RLHF, red-teaming, reliability, responsible deployment | None directly | None directly, but affects consumer satisfaction |

**Key dynamics:**
- `fundamental_research` + `training_optimization` = capability-building investments
- `evaluation_engineering` is "legitimate optimization" that *happens* to inflate scores
- `safety_alignment` is a trade-off: no immediate benefit, but may improve consumer trust and regulatory standing

### Identity / Personality
Providers have different strategic profiles that influence their decision-making:
- `strategy_profile`: Natural language description (e.g., "aggressive competitor who prioritizes market position" vs. "quality-focused organization that prioritizes genuine capability")
- `innate_traits`: Core tendencies (e.g., "risk-tolerant", "reputation-conscious")

### Cognitive Loop (per round)
1. **Observe**: See published scores (own and competitors')
2. **Retrieve**: Recall relevant past experiences from memory (what investments led to what outcomes)
3. **Reflect**: Update beliefs about own capability and benchmark exploitability based on observations
4. **Plan**: Decide investment portfolio allocation — this is LLM-driven (or heuristic), using personality and beliefs as context
5. **Execute**: Apply chosen portfolio; true_capability updates based on research and training investments

### Key Dynamics Captured
- **Imperfect self-knowledge**: Providers don't know their true capability; they infer it from noisy scores
- **Competitive pressure**: Observing competitor scores creates pressure to match or exceed them
- **Investment uncertainty**: Providers don't know exactly how much each investment type affects scores
- **Emergent gaming**: Over-investment in evaluation engineering emerges from rational choice, not explicit "gaming"
- **Long-term vs. short-term tradeoffs**: Research has delayed payoff; evaluation engineering has immediate payoff
- **Learning over time**: Beliefs update based on accumulated experience

---

## Simulated Actor: Evaluator (Evaluation Provider)

**Purpose:** Represents organizations that design and operate benchmarks.

### State Variables

#### Benchmark Properties (define the scoring function)
| Variable | Description |
|----------|-------------|
| `benchmark_name` | Identifier for the benchmark |
| `validity` (α) | How well benchmark measures true capability (0-1) |
| `exploitability` (β) | How much gaming improves scores (0-1) |
| `noise_level` (σ) | Standard deviation of score noise |

#### Operational State
| Variable | Description |
|----------|-------------|
| `published_scores` | History of all scores published |
| `known_gaming_strategies` | Strategies the evaluator has detected (if any) |

### Behavior (Current Implementation)
In the initial simulation, the Evaluator is **passive**:
- Runs the benchmark on submitted models
- Publishes scores
- Does not adapt the benchmark in response to gaming

### Future Extensions
The Evaluator could become an active agent that:
- Detects when scores diverge from construct validity
- Updates benchmarks to reduce exploitability
- Creates new benchmarks targeting different constructs
- Observes provider behavior patterns and adjusts accordingly

---

## Simulation Parameters

### Initial Configuration
| Parameter | Description | Example Value |
|-----------|-------------|---------------|
| `n_providers` | Number of model providers | 2 |
| `n_rounds` | Number of simulation rounds | 50 |
| `initial_capability_range` | Starting capability distribution | [0.3, 0.7] |
| `benchmark_validity` | α parameter | 0.7 |
| `benchmark_exploitability` | β parameter | 0.5 |
| `score_noise` | σ parameter | 0.1 |

### Emergent Phenomena to Study
1. **Race to the bottom**: Do providers converge on high-evaluation-engineering strategies?
2. **Belief divergence**: Do providers' beliefs about their capability diverge from reality?
3. **Signaling breakdown**: Does high score cease to signal high capability (Goodhart's Law)?
4. **Strategy heterogeneity**: Do different personality types lead to different investment equilibria?
5. **Capability vs. perception gap**: Do providers who invest more in research have lower scores but higher true capability?
6. **Safety investment dynamics**: Under what conditions do providers invest in safety alignment?

---

## File Structure

```
eval_sim/
├── actors/
│   ├── __init__.py
│   ├── model_provider.py    # ModelProvider class
│   ├── evaluator.py         # Evaluator class
│   ├── consumer.py          # Consumer class (demand-side feedback)
│   └── policymaker.py       # Policymaker class (regulatory intervention)
├── memory_structures/
│   └── ...                  # Memory structures (if needed)
├── simulation.py            # Main simulation loop
├── visibility.py            # Visibility system (public/private/ground truth)
├── llm.py                   # Multi-provider LLM integration
├── experiment_logger.py     # Experiment logging and tracking
├── game_log.py              # Game log markdown generator
├── plotting.py              # Visualization utilities
├── run_experiments.py       # Script to run predefined experiments
└── experiments/             # Experiment results and logs
```
