# Reputational Damage: AI Ecosystem Stakeholders

This document describes (1) the conceptual stakeholders in the AI evaluation ecosystem, and (2) how they are computationally modeled in the `eval_sim/` simulation framework.

## File Reference

| File | Purpose |
|------|---------|
| `simulation.py` | Core sim loop, `SimulationConfig`, `EvalEcosystemSimulation`, provider config presets (`get_default_provider_configs`, `get_two_provider_configs`, `get_five_provider_configs`) |
| `run_experiment.py` | **Editable experiment config file** — edit all parameters (providers, benchmarks, funders, rounds, LLM provider, etc.) at the top, then `python run_experiment.py` to run |
| `run_llm_now.py` | CLI-driven quick experiment runner — parameterized via command-line flags (e.g. `python run_llm_now.py -r 5 -p ollama -e --funders`) |
| `actors/model_provider.py` | ModelProvider actor with plan/observe/reflect/execute cycle |
| `actors/evaluator.py` | Evaluator, Benchmark, Regulation classes |
| `actors/consumer.py` | ConsumerMarket with market segments (archetype × use-case), proportional switching |
| `actors/policymaker.py` | Policymaker with graduated interventions, media-aware |
| `actors/funder.py` | Funder actor (VC, gov, foundation types), media-aware |
| `actors/media.py` | Media actor (TechPress) — observes public events, publishes coverage influencing downstream actors |
| `visibility.py` | State classes: PublicState, PrivateState, GroundTruth |
| `llm.py` | Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini) and prompt templates |
| `plotting.py` | Visualization dashboards (provider, consumer, policymaker, evaluator, funder, summary) |
| `experiment_logger.py` | ExperimentLogger for systematic experiment logging to `experiments/` |
| `game_log.py` | Natural language markdown game log generator |

---

# Part 1: Conceptual Stakeholders

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
- Design human-AI team workflows
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

# Part 2: Implementation Status

This section clarifies which stakeholders are implemented in the simulation.

| Stakeholder | Status | Notes |
|-------------|--------|-------|
| Individual Consumer | **Implemented** (as market segments) | `actors/consumer.py` — ConsumerMarket with archetype × use-case segments |
| Organizational Consumer | Not implemented | Could extend ConsumerMarket with institutional segments |
| Policymaker | **Implemented** | `actors/policymaker.py` — media-aware |
| Model Provider | **Implemented** | `actors/model_provider.py` — per-provider visibility |
| Evaluation Provider | **Implemented** | Active benchmark evolution + mid-simulation benchmark introduction |
| Funder | **Implemented** | `actors/funder.py` — VC, Government, Foundation types; media-aware |
| Media | **Implemented** | `actors/media.py` — TechPress outlet; publishes coverage influencing downstream actors |

### Evaluator Behavior (Current)
The Evaluator is **active** in two ways:
1. **Benchmark evolution**: Benchmarks degrade in validity and grow in exploitability in proportion to aggregate evaluation engineering investment (gaming pressure). This creates the core Goodhart's Law feedback loop.
2. **Benchmark introduction**: The evaluator can introduce new benchmarks mid-simulation when existing benchmarks become unreliable (validity < 0.4) or periodically every `cooldown` rounds (default 8). New benchmarks start with high validity (0.85) and low exploitability (0.15), resetting the measurement quality. Subject to a configurable cooldown and a maximum of 6 total benchmarks.

### Future Extensions
- **Organizational Consumer**: Longer decision timelines, compliance constraints
- **Multi-outlet Media**: Multiple media outlets with different editorial biases and reach

---

# Part 3: Simulation Model

This section describes how actors are computationally modeled. The simulation studies how benchmark-based competition can lead to Goodhart's Law dynamics, where optimizing for a measure causes it to cease being a good measure.

## Core Concepts

### Constructs vs. Measures
A fundamental tension exists between what we want to measure (the **construct**, e.g., "reasoning ability") and what we actually measure (the **benchmark score**). When providers optimize for the benchmark, the correlation between score and construct degrades over time.

### The Scoring Model
Observed benchmark scores are generated as:

```
score ~ Normal(true_capability + evaluation_engineering × exploitability, (σ/√α)²)
```

Where:
- `α` (validity): Measurement precision — higher validity = lower noise (0-1)
- `exploitability`: Property of the benchmark — how much eval engineering inflates scores (0-1)
- `evaluation_engineering`: Provider's investment in benchmark-specific optimization (0-1)
- `σ` (noise_level): Base standard deviation of score noise
- Gaming (`eval_engineering × exploitability`) inflates scores **above** true capability
- Validity controls noise magnitude, not signal scaling

**Key insight:** Providers don't directly observe `α` or `exploitability`. They only see realized scores and must *infer* these properties. "Gaming" is not an explicit choice—it emerges from rational investment in evaluation engineering. The resulting score inflation (score > true capability) is what creates consumer disappointment and drives the Goodhart feedback loop.

**Per-benchmark monotonicity:** Published per-benchmark scores are monotonically non-decreasing per provider — providers wouldn't disclose a worse score. The evaluator enforces `score = max(score, previous_best)` before publishing. Composite scores (weighted average of per-benchmark) inherit this property.

### Visibility System
The simulation enforces strict information boundaries:

| Visibility Level | Who Can Access | Examples |
|-----------------|----------------|----------|
| **Public** | All actors | Published scores, leaderboard, regulations |
| **Private** | Self only | Beliefs, strategies, satisfaction history |
| **Ground Truth** | Simulation only | True capability, true satisfaction |

Ground truth is held externally by the simulation, making it structurally impossible for actor decision-making (including LLM prompts) to access hidden information.

---

## Simulated Actor: Model Provider

**Purpose:** Represents organizations developing and releasing AI models in a competitive market.

### State Variables

#### Public State (visible to all)
| Variable | Description |
|----------|-------------|
| `name` | Unique identifier |
| `published_scores` | History of benchmark scores |
| `current_round` | Current simulation round |

#### Private State (visible to self only)
| Variable | Description |
|----------|-------------|
| `believed_own_capability` | Provider's estimate of their true capability |
| `believed_benchmark_exploitability` | Provider's estimate of how gameable the benchmark is |
| `believed_competitor_capabilities` | Estimates of competitors' true capabilities |
| `past_strategies` | History of investment choices |
| `competitor_scores` | Observed scores of other providers |

#### Ground Truth (simulation only)
| Variable | Description |
|----------|-------------|
| `true_capability` | Actual capability level (what benchmarks should measure) |

### Investment Portfolio
Providers allocate resources across four investment areas each round. These must sum to 1.0 (100% of effort budget).

| Investment | Description | Effect on Capability | Effect on Score |
|------------|-------------|---------------------|-----------------|
| `fundamental_research` | Novel architectures, pre-training improvements, breakthrough research | High (1.5× efficiency), high variance | Indirect (via capability) |
| `training_optimization` | Scaling, data quality, fine-tuning, infrastructure | Moderate (1.0× efficiency), reliable | Indirect (via capability) |
| `evaluation_engineering` | Benchmark-specific optimization, prompt tuning for evals | Minimal (0.1× efficiency) | Direct boost via exploitability |
| `safety_alignment` | RLHF, red-teaming, reliability, responsible deployment | None directly | None directly, affects consumer satisfaction |

**Key dynamics:**
- `fundamental_research` + `training_optimization` = capability-building investments
- `evaluation_engineering` inflates scores without proportional capability gain
- `safety_alignment` trades immediate benefit for consumer trust and regulatory standing

### Identity / Personality
Providers have strategic profiles influencing decision-making:
- `strategy_profile`: Natural language description (e.g., "aggressive competitor" vs. "quality-focused")
- `innate_traits`: Core tendencies (e.g., "risk-tolerant", "reputation-conscious")

### Per-Provider Visibility (Ecosystem Context)
Providers receive a filtered view of the ecosystem — they see only their **own** consumer satisfaction and market share, not competitors'. This is passed via `_get_provider_ecosystem_context(provider_name)`:

| Signal | Source | Description |
|--------|--------|-------------|
| `consumer_satisfaction` | `consumer_data.provider_satisfaction[self]` | Own customer satisfaction only |
| `own_market_share` | `consumer_data.market_shares[self]` | Own market share proportion |
| `regulatory_pressure` | `policymaker_data.interventions` | Public regulatory actions (visible to all) |

### Cognitive Loop (per round)
1. **Observe**: See published scores (own and competitors')
2. **Retrieve**: Recall relevant past experiences (what investments led to what outcomes)
3. **Reflect**: Update beliefs about own capability and benchmark exploitability
4. **Plan**: Decide investment portfolio allocation (LLM-driven or heuristic), informed by per-provider ecosystem context
5. **Execute**: Apply portfolio; true_capability updates based on research/training investments

---

## Simulated Actor: Consumer Market

**Purpose:** Represents the aggregate consumer market as a collection of market segments, each combining a **use-case profile** (what the consumer needs) with a **behavioral archetype** (how the consumer decides). Switching is proportional within segments rather than binary per-individual.

### Data Model

#### Use-Case Profiles (10 available, configurable subset)
Each profile defines benchmark preferences — which capabilities matter most:

| Profile | Key Benchmark Preferences |
|---------|--------------------------|
| `software_dev` | coding: 0.7, reasoning: 0.2, writing: 0.1 |
| `content_writer` | writing: 0.7, reasoning: 0.2, coding: 0.1 |
| `legal` | reasoning: 0.5, writing: 0.4, safety: 0.1 |
| `healthcare` | safety: 0.5, reasoning: 0.3, writing: 0.2 |
| `finance` | reasoning: 0.5, safety: 0.3, coding: 0.2 |
| `educator` | writing: 0.4, reasoning: 0.4, safety: 0.2 |
| `customer_service` | writing: 0.6, reasoning: 0.3, safety: 0.1 |
| `researcher` | reasoning: 0.4, coding: 0.4, writing: 0.2 |
| `creative` | writing: 0.6, reasoning: 0.2, coding: 0.2 |
| `marketing` | writing: 0.5, reasoning: 0.3, coding: 0.2 |

Preference categories are mapped to actual benchmark names via substring matching (e.g., "coding" matches "coding_bench"). Unmatched benchmarks receive a small default weight (0.1). Weights are re-resolved when new benchmarks are introduced mid-simulation.

#### Behavioral Archetypes (3)

| Archetype | `leaderboard_trust` | `switching_cost` | `switching_threshold` |
|-----------|---------------------|-------------------|-----------------------|
| `leaderboard_follower` | 0.85 | 0.05 | 0.15 |
| `experience_driven` | 0.35 | 0.08 | 0.08 |
| `cautious` | 0.50 | 0.20 | 0.25 |

#### MarketSegment (archetype × use_case)
Each segment (e.g., `"software_dev_leaderboard_follower"`) tracks:

| Variable | Description |
|----------|-------------|
| `name` | Segment identifier (use_case + archetype) |
| `market_fraction` | Proportion of total market this segment represents |
| `benchmark_weights` | `{benchmark_name: weight}` — resolved from use-case preferences |
| `leaderboard_trust` | From archetype — how much to trust leaderboard vs. experience |
| `switching_cost` | From archetype — friction for switching providers |
| `switching_threshold` | From archetype — gap required to trigger switching |
| `provider_shares` | `{provider: proportion}` — sums to 1.0 within segment |
| `believed_quality` | `{provider: float}` — believed quality per provider |
| `satisfaction` | `{provider: float}` — per-provider satisfaction in this segment |
| `tenure` | `{provider: int}` — average rounds subscribed per provider |

### ConsumerMarket Class

The `ConsumerMarket` manages all segments and provides aggregate consumer data.

**Key methods:**
- `resolve_benchmark_weights(benchmark_names)` — maps use-case preference categories to actual benchmark names
- `observe(leaderboard, media_coverage, round_num)` — updates beliefs from composite leaderboard scores
- `observe_per_benchmark(leaderboard, per_bm_scores, media_coverage, round_num)` — updates beliefs using per-benchmark scores weighted by segment preferences
- `compute_satisfaction(ground_truth)` — computes per-segment per-provider satisfaction from true capabilities
- `compute_switching()` — proportional switching within each segment (returns market-wide switching rate)
- `get_consumer_data()` — returns aggregate `consumer_data` dict for downstream actors

### Proportional Switching (Sigmoid-Based)
Switching within each segment is probabilistic, not binary:

```
switch_probability = 1 / (1 + exp(-steepness × (gap - threshold)))
```

Two triggers:
1. **Dissatisfaction**: `gap = believed_quality[current] - satisfaction[current]` — expectations exceed experience
2. **Opportunity**: `gap = believed_quality[best_alt] - believed_quality[current] - switching_cost` — a better alternative exists

The switching probability determines what fraction of the segment's share with a provider moves to the best alternative. Tenure bonus (`0.02 × tenure`) adds inertia for loyal users.

### Media Influence on Consumers
When media coverage is available:
- Positive sentiment (`> 0`) increases belief update rate (faster adoption of leaderboard signals)
- Negative sentiment (`< 0`) decreases it
- Risk signals reduce `leaderboard_trust` by 5% for leaderboard-follower segments
- Provider attention modulates brand awareness during switching decisions

### Key Dynamic: The Satisfaction Gap
When a provider games the benchmark:
- High scores attract market share (especially from leaderboard followers)
- Low true capability leads to poor satisfaction in use-case-relevant dimensions
- Disappointed segments proportionally shift market share away
- This creates demand-side pressure against gaming, differentiated by use case

---

## Simulated Actor: Policymaker

**Purpose:** Represents regulators who can mandate evaluations or set requirements based on ecosystem observations.

### State Variables

#### Public State (visible to all)
| Variable | Description |
|----------|-------------|
| `name` | Unique identifier |
| `active_regulations` | Currently enforced rules |
| `public_statements` | Official communications |

#### Private State (visible to self only)
| Variable | Description |
|----------|-------------|
| `policy_objectives` | Goals (e.g., "protect consumers", "ensure safety") |
| `risk_beliefs` | Beliefs about ecosystem risks |
| `regulatory_capacity` | Resources available for enforcement |
| `intervention_history` | Past regulatory actions |

#### Ground Truth (simulation only)
| Variable | Description |
|----------|-------------|
| `true_risk_tolerance` | Actual threshold for intervention |
| `true_intervention_effectiveness` | How effective regulations actually are |

### Intervention Types
| Type | Description |
|------|-------------|
| `investigation` | Initial inquiry triggered by score volatility or elevated risk |
| `public_warning` | Warning that reduces consumer `leaderboard_trust` |
| `mandate_benchmark` | Changes benchmark validity/exploitability (requires prior investigation) |
| `compliance_audit` | Post-mandate follow-up that further reduces exploitability |

Interventions follow a **graduated escalation** model and have a **3-round cooldown** between actions.

### Cognitive Loop (per round)
1. **Observe**: See leaderboard, consumer satisfaction, validity correlation, media coverage
2. **Reflect**: Update risk assessments (media risk_signals bump gaming_risk beliefs; critical sentiment bumps validity_degradation_risk)
3. **Plan**: Decide whether to intervene (respecting cooldown and escalation requirements)
4. **Execute**: Issue regulations

---

## Simulated Actor: Funder

**Purpose:** Represents capital allocators (VCs, Government/AISI, Foundations) who influence provider development through funding decisions.

### State Variables

#### Public State (visible to all)
| Variable | Description |
|----------|-------------|
| `name` | Unique identifier |
| `published_scores` | Public funding announcements |

#### Private State (visible to self only)
| Variable | Description |
|----------|-------------|
| `funder_type` | Type: "vc", "gov", or "foundation" |
| `mission_statement` | Mission-driven objective |
| `total_capital` | Total capital available for funding |
| `deployed_capital` | Currently deployed capital |
| `believed_provider_quality` | Dict of {provider: quality_estimate} |
| `believed_provider_gaming` | Dict of {provider: gaming_estimate} |
| `active_funding` | Current funding allocations |
| `funding_history` | History of past allocations |

#### Ground Truth (simulation only)
| Variable | Description |
|----------|-------------|
| `true_roi` | Actual return on investment |
| `funding_efficiency` | How effective funding is at improving providers |

### Funder Types

| Type | Focus | Allocation Strategy |
|------|-------|---------------------|
| **VC** | ROI maximization | Concentrate on top performers (60/30/10 split) |
| **Government/AISI** | Safety & stability | Spread funding, penalize gaming and regulatory issues |
| **Foundation** | Mission alignment | Reward authenticity and capability growth, support underdogs |

### Funding Mechanism

Funding affects providers via an **efficiency multiplier** on capability gains:

```python
effective_efficiency = base_rnd_efficiency * funding_multiplier
# funding_multiplier ranges from 1.0 (no funding) to 2.0 (max funding)
```

### Visibility Model (Information Asymmetry)

Funders can only see public signals and must **infer** provider quality:

| Signal | Source | Interpretation |
|--------|--------|----------------|
| Leaderboard score | `leaderboard` | Raw performance |
| Consumer satisfaction | `consumer_data.provider_satisfaction` | Per-provider true quality proxy |
| **Satisfaction gap** | `score - satisfaction` | Gaming indicator (high gap = gaming) |
| Regulatory interventions | `policymaker_data.interventions` | Safety/compliance risk |
| Media coverage | `media_data` | Sentiment, provider attention, and risk signals |

This creates realistic information asymmetry — funders cannot see provider strategies directly. Media acts as an amplifying intermediary: high media attention combined with risk signals increases the funder's `believed_gaming` estimate for that provider.

### Cognitive Loop (per round)
1. **Observe**: See leaderboard, consumer satisfaction, regulatory interventions, media coverage
2. **Reflect**: Update beliefs about provider quality and gaming levels (media attention + risk signals can increase believed_gaming for specific providers)
3. **Plan**: Decide funding allocations based on funder type strategy
4. **Execute**: Deploy capital, update active_funding

---

## Simulated Actor: Media

**Purpose:** Information intermediary that observes public events and publishes coverage influencing consumer beliefs, policymaker risk perception, and funder sentiment. Currently a single outlet (TechPress); designed for future multi-outlet scaling with different editorial biases.

### State Variables

#### Public State (visible to all)
| Variable | Description |
|----------|-------------|
| `name` | Outlet name (e.g., "TechPress") |
| `coverage` | Published coverage for current round (headlines, sentiment, attention) |

#### Private State (visible to self only)
| Variable | Description |
|----------|-------------|
| `editorial_bias` | -1 (critical) to +1 (tech-optimistic), default 0.0 |
| `amplification` | How much media amplifies signals (1.0 = neutral) |
| `coverage_history` | All past coverage outputs |

### What Makes News
The media detects newsworthy events from public data:

| Event Type | Trigger | Sentiment Effect |
|------------|---------|------------------|
| Leader change | New provider at top of leaderboard | +0.2 (exciting) |
| Large score jump | Score surge > 0.05; > 0.08 adds "major model update" headline | +0.1 (surge) |
| Regulatory action | Policymaker intervention — specific headlines per type (investigation, warning, mandate, audit) | -0.15 (sobering) |
| New benchmark | Evaluator introduces a benchmark | +0.1 (positive innovation) |
| Low validity | Benchmark validity < 0.5 | -0.1 (risk signal) |
| Score convergence | Score range < 0.03 | -0.05 (benchmark meaningfulness concern) |
| Funding decision | Top provider allocation per funder | +0.05 |
| Per-benchmark leader change | New #1 on a specific benchmark | +0.1 |
| Consumer market shift | Provider gains/loses > 3% market share | +0.05 (surge) or -0.1 (turning away) |

### Coverage Output (`MediaCoverage`)

| Field | Type | Description |
|-------|------|-------------|
| `headlines` | list[str] | Detected newsworthy events |
| `sentiment` | float | -1 to +1, market sentiment after editorial bias and amplification |
| `provider_attention` | dict | `{provider: 0-1}` — how much coverage each provider gets |
| `risk_signals` | list[str] | Flagged concerns (e.g., "regulatory_investigation", "low_validity_coding_bench") |
| `benchmark_attention` | dict | `{benchmark: 0-1}` — coverage of specific benchmarks |

### How Media Influences Downstream Actors

| Actor | Influence Mechanism |
|-------|---------------------|
| **Consumers** | Sentiment modulates belief update rate; risk signals reduce leaderboard_trust for follower segments; provider attention affects brand awareness during switching |
| **Policymakers** | Risk signals bump gaming_risk beliefs; critical sentiment (< -0.3) bumps validity_degradation_risk |
| **Funders** | High provider attention + risk signals increase believed_gaming for that provider |

### Simulation Round Order
Media publishes **after** evaluator scoring but **before** consumer/policymaker/funder rounds:
1. Providers plan + execute
2. Evaluator scores + benchmark evolution + benchmark introduction
3. **Media observes + publishes**
4. Consumers observe (with media coverage)
5. Policymakers observe (with media coverage)
6. Funders observe (with media coverage)

---

## Simulated Actor: Evaluator

**Purpose:** Operates benchmarks and publishes scores. Actively evolves benchmarks under gaming pressure (validity decays, exploitability grows).

### Benchmark Properties
| Variable | Description | Range |
|----------|-------------|-------|
| `name` | Benchmark identifier | string |
| `validity` (α) | How well benchmark measures true capability | 0-1 |
| `exploitability` (β) | How much gaming improves scores | 0-1 |
| `noise_level` (σ) | Standard deviation of score noise | 0-1 |
| `weight` | Importance in composite score (multi-benchmark mode) | 0-1 |
| `validity_decay_rate` | Rate at which validity degrades under gaming pressure | 0-1 |
| `exploitability_growth_rate` | Rate at which exploitability increases under gaming pressure | 0-1 |

### Multi-Benchmark Mode
The simulation supports multiple benchmarks with different properties:
```python
benchmarks = [
    {"name": "coding_bench", "validity": 0.85, "exploitability": 0.25, "weight": 0.5},
    {"name": "reasoning_bench", "validity": 0.7, "exploitability": 0.45, "weight": 0.5},
]
```

Composite score = weighted average of individual benchmark scores.

### Benchmark Introduction
The evaluator can introduce new benchmarks mid-simulation:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `benchmark_introduction_cooldown` | 8 rounds | Minimum rounds between introductions |
| `max_benchmarks` | 6 | Maximum total benchmarks allowed |

**Trigger conditions** (any one):
- Any existing benchmark validity drops below 0.4
- Periodic introduction: every `cooldown` rounds (default 8)

New benchmarks are created with high validity (0.85) and low exploitability (0.15), effectively resetting measurement quality. Their weight equals the average of existing benchmark weights. Consumer market benchmark weights are automatically re-resolved when new benchmarks appear.

---

# Part 4: Simulation Metrics Reference

This section documents all metrics tracked during simulation.

## Per-Round Metrics (`history.json`)

Each round records the following data:

### Core Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `round` | int | Round number (0-indexed) |
| `scores` | dict | `{provider_name: score}` - Published benchmark scores |
| `true_capabilities` | dict | `{provider_name: capability}` - Ground truth capabilities |
| `believed_capabilities` | dict | `{provider_name: belief}` - What each provider believes their capability is |
| `leaderboard` | list | Ranked list of `(provider_name, score)` tuples |

### Strategy Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `strategies` | dict | Per-provider investment portfolios |
| `strategies[name].fundamental_research` | float | Investment in novel research (0-1) |
| `strategies[name].training_optimization` | float | Investment in scaling/fine-tuning (0-1) |
| `strategies[name].evaluation_engineering` | float | Investment in benchmark optimization (0-1) |
| `strategies[name].safety_alignment` | float | Investment in safety/RLHF (0-1) |

### Multi-Benchmark Metrics (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `per_benchmark_scores` | dict | `{benchmark_name: {provider: score}}` — monotonically non-decreasing per provider |
| `benchmark_names` | list | List of benchmark names |
| `benchmark_params` | dict | `{benchmark_name: {validity, exploitability}}` - Current benchmark state |

### Consumer Metrics (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `consumer_data.market_shares` | dict | `{provider_name: proportion}` — aggregate market share across all segments |
| `consumer_data.provider_satisfaction` | dict | `{provider_name: satisfaction}` — per-provider average satisfaction |
| `consumer_data.avg_satisfaction` | float | Market-wide average satisfaction |
| `consumer_data.switching_rate` | float | Fraction of total market that switched providers this round |
| `consumer_data.segment_data` | dict | `{segment_name: {provider_shares, satisfaction, ...}}` — per-segment breakdown |

### Media Metrics (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `media_data.headlines` | list | Newsworthy events detected this round |
| `media_data.sentiment` | float | Market sentiment (-1 to +1) |
| `media_data.provider_attention` | dict | `{provider_name: 0-1}` — coverage attention per provider |
| `media_data.risk_signals` | list | Flagged risk concerns |
| `media_data.benchmark_attention` | dict | `{benchmark_name: 0-1}` — benchmark-specific coverage |

### Benchmark Introduction Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `new_benchmark` | dict | Present only when a new benchmark is introduced |
| `new_benchmark.name` | str | Name of the new benchmark (e.g., "benchmark_r12") |
| `new_benchmark.validity` | float | Initial validity (typically 0.85) |
| `new_benchmark.exploitability` | float | Initial exploitability (typically 0.15) |
| `new_benchmark.trigger` | str | What triggered the introduction (e.g., "low_validity" or "periodic") |

### Policymaker Metrics (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `policymaker_data.interventions` | list | Regulatory actions taken this round |
| `policymaker_data.interventions[].type` | string | Intervention type (investigation, public_warning, mandate_benchmark, compliance_audit) |
| `policymaker_data.interventions[].details` | dict | Intervention parameters |
| `policymaker_data.active_regulations` | list | Currently active regulation names |

### Funder Metrics (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `funder_data.allocations` | dict | `{funder_name: {provider: amount}}` |
| `funder_data.funding_multipliers` | dict | `{provider_name: multiplier}` - ranges 1.0-2.0 |
| `funder_data.total_funding` | float | Total capital deployed this round |

---

## Summary Metrics (`summary.json`)

Generated at simulation end:

### Global Metrics
| Metric | Type | Description |
|--------|------|-------------|
| `n_rounds` | int | Total rounds completed |
| `validity_correlation` | float | Pearson correlation between scores and true capabilities across all rounds. **Key metric for Goodhart's Law** - decreases when gaming is prevalent. |
| `final_scores` | dict | Scores at last round |
| `final_true_capabilities` | dict | True capabilities at last round |
| `final_believed_capabilities` | dict | Believed capabilities at last round |
| `final_strategies` | dict | Investment portfolios at last round |
| `leaderboard` | list | Final rankings |

### Benchmark Parameters
| Metric | Type | Description |
|--------|------|-------------|
| `benchmark_params.validity` | float | α parameter |
| `benchmark_params.exploitability` | float | β parameter |
| `benchmark_params.noise` | float | σ parameter |

### Per-Provider Summary
| Metric | Type | Description |
|--------|------|-------------|
| `provider_summaries[name].initial_capability` | float | True capability at round 0 |
| `provider_summaries[name].final_capability` | float | True capability at last round |
| `provider_summaries[name].capability_growth` | float | `final - initial` capability |
| `provider_summaries[name].mean_score` | float | Average score across all rounds |
| `provider_summaries[name].score_std` | float | Standard deviation of scores |
| `provider_summaries[name].mean_fundamental_research` | float | Average investment in research |
| `provider_summaries[name].mean_training_optimization` | float | Average investment in training |
| `provider_summaries[name].mean_evaluation_engineering` | float | Average investment in eval engineering |
| `provider_summaries[name].mean_safety_alignment` | float | Average investment in safety |

### Consumer Summary (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `consumer_summary.n_segments` | int | Number of market segments |
| `consumer_summary.mean_satisfaction` | float | Average satisfaction across all rounds |
| `consumer_summary.final_satisfaction` | float | Satisfaction at last round |
| `consumer_summary.avg_switching_rate` | float | Average switching rate across all rounds |
| `consumer_summary.final_market_shares` | dict | `{provider: proportion}` at last round |

### Policymaker Summary (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `policymaker_summary.n_policymakers` | int | Number of policymakers |
| `policymaker_summary.total_interventions` | int | Total regulatory actions taken |
| `policymaker_summary.intervention_types` | list | Unique intervention types used |
| `policymaker_summary.active_regulations` | list | Regulations active at end |

### Funder Summary (if enabled)
| Metric | Type | Description |
|--------|------|-------------|
| `funder_summary.n_funders` | int | Number of funders |
| `funder_summary.total_funding_deployed` | float | Total capital deployed across all rounds |
| `funder_summary.final_funding_multipliers` | dict | `{provider: multiplier}` at end |
| `funder_summary.funder_types` | list | Types of funders (vc, gov, foundation) |

---

## Key Insight Metrics

These metrics are most useful for understanding gaming dynamics:

| Metric | What It Reveals |
|--------|-----------------|
| **Score - True Capability Gap** | `scores[name] - true_capabilities[name]` per round shows benchmark inflation |
| **validity_correlation** | Overall benchmark trustworthiness; decreases with gaming |
| **mean_evaluation_engineering** | Direct measure of gaming effort |
| **capability_growth** | Did real R&D investment pay off? |
| **avg_satisfaction** | Consumer welfare; low when gaming is high |
| **switching_rate** | Market instability from disappointment (proportion of market that switches) |
| **market_shares** | Provider dominance; shifts reveal consumer response to gaming |
| **media_sentiment** | Market mood; critical sentiment can trigger regulatory and funder reactions |
| **funding_multipliers** | Capital advantage; higher funding = faster capability growth |
| **funding vs capability growth** | Did funding predict/cause capability improvement? |
| **new_benchmark introductions** | Evaluator response to measurement degradation |

---

# Part 5: Experiment Infrastructure

## Experiment Naming Convention

Experiments are named with a hybrid scheme:

```
exp_<NNN>_<short_description>
```

- `<NNN>`: Auto-incrementing 3-digit number (001, 002, ...)
- `<short_description>`: Sanitized name (lowercase, underscores, max 30 chars)

**Examples:**
- `exp_001_baseline_heuristic`
- `exp_011_4_actors_dual_benchmark_llm`
- `exp_012_3_actors_llm_mode`

## Experiment Directory Structure

Each experiment creates a folder with:

```
experiments/exp_XXX_name/
├── metadata.json       # Description, tags, timestamp, git commit, seed
├── config.json         # Full configuration (for reproducibility)
├── history.json        # Round-by-round data (see Per-Round Metrics)
├── rounds.jsonl        # Incremental round data (one JSON line per round)
├── summary.json        # Final metrics (see Summary Metrics)
├── ground_truth.json   # True capability values for all actors
├── game_log.md         # Human-readable narrative of the simulation
├── plots/              # Generated visualizations
│   ├── provider_dashboard.png
│   ├── evaluator_dashboard.png
│   ├── consumer_dashboard.png         # if consumers enabled
│   ├── policymaker_dashboard.png      # if policymakers enabled
│   ├── funder_dashboard.png           # if funders enabled
│   └── summary_dashboard.png
├── providers/          # Provider state snapshots
│   └── <provider_name>/
├── consumer_market/    # Consumer market state (if enabled)
│   └── market.json
├── policymakers/       # Policymaker states (if enabled)
│   └── <policymaker_name>/
└── funders/            # Funder states (if enabled)
    └── <funder_name>/
```

## Experiment Index

All experiments are tracked in `experiments/index.json`:

```json
{
  "experiments": [
    {
      "id": "exp_001_baseline_heuristic",
      "name": "baseline_heuristic",
      "created_at": "2026-01-19T20:43:20.281631",
      "tags": ["baseline", "heuristic", "2-provider"],
      "llm_mode": false
    }
  ],
  "next_id": 2
}
```

## Configuration Options (`SimulationConfig`)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `n_rounds` | int | 50 | Number of simulation rounds |
| `seed` | int | 42 | Random seed for reproducibility |
| `benchmark_name` | str | "capability_benchmark" | Name of the benchmark |
| `benchmark_validity` | float | 0.7 | α parameter (0-1) |
| `benchmark_exploitability` | float | 0.5 | β parameter (0-1) |
| `benchmark_noise` | float | 0.1 | σ parameter |
| `benchmarks` | list | None | Multi-benchmark config (overrides single benchmark) |
| `rnd_efficiency` | float | 0.01 | Capability gain per unit R&D investment |
| `llm_mode` | bool | False | Use LLM for planning (vs. heuristics) |
| `benchmark_introduction_cooldown` | int | 8 | Minimum rounds between benchmark introductions |
| `max_benchmarks` | int | 6 | Maximum total benchmarks allowed |
| `enable_consumers` | bool | False | Enable consumer market |
| `enable_policymakers` | bool | False | Enable policymaker actors |
| `enable_funders` | bool | False | Enable funder actors |
| `enable_media` | bool | False | Enable media actor (TechPress) |
| `use_case_profiles` | list | None | Which use-case profiles to include (e.g., `["software_dev", "healthcare"]`); None = default 6 |
| `n_policymakers` | int | 1 | Number of policymakers |
| `n_funders` | int | 1 | Number of funders |
| `capability_ceiling` | float | 1.0 | Maximum capability achievable |
| `diminishing_returns_rate` | float | 3.0 | S-curve steepness near ceiling |
| `breakthrough_probability` | float | 0.02 | Chance of capability breakthrough |
| `breakthrough_magnitude` | float | 0.05 | Size of breakthroughs |
| `benchmark_validity_decay_rate` | float | 0.005 | Validity decay per round |
| `benchmark_exploitability_growth_rate` | float | 0.008 | Exploitability growth per round |
| `verbose` | bool | True | Print progress during simulation |
| `output_dir` | str | None | Output directory |

## Running Experiments

### Quick Test (no logging)
```bash
python run_llm_now.py --rounds 5 --provider openai
python run_llm_now.py -r 10 -p anthropic
python run_llm_now.py -r 3 -p ollama
```

### Full Experiments (with logging)
```bash
python run_experiments.py          # Heuristic mode (3 & 4 actors)
python run_experiments.py --llm    # LLM mode experiments
python run_experiments.py --all    # Both heuristic and LLM
```

### LLM Provider Configuration

Set via environment variables:
```bash
export LLM_PROVIDER=openai      # or "anthropic", "ollama", or "gemini"
export LLM_MODEL=gpt-4o-mini    # provider-specific model name
export OPENAI_API_KEY=sk-...    # for OpenAI
export ANTHROPIC_API_KEY=sk-... # for Anthropic
export GEMINI_API_KEY=...       # for Gemini
export OLLAMA_BASE_URL=http://localhost:11434  # for Ollama

# Example: use Gemini
export LLM_PROVIDER=gemini
export LLM_MODEL=gemini-2.5-flash
```

---

# Part 6: Emergent Phenomena to Study

The simulation is designed to investigate:

1. **Race to the bottom**: Do providers converge on high-evaluation-engineering strategies?
2. **Belief divergence**: Do providers' beliefs about their capability diverge from reality?
3. **Signaling breakdown**: Does high score cease to signal high capability (Goodhart's Law)?
4. **Strategy heterogeneity**: Do different personality types lead to different investment equilibria?
5. **Capability vs. perception gap**: Do providers who invest more in research have lower scores but higher true capability?
6. **Safety investment dynamics**: Under what conditions do providers invest in safety alignment?
7. **Consumer welfare**: How does gaming affect end-user satisfaction across different use cases?
8. **Use-case differentiation**: Do different consumer segments (developers vs. healthcare) respond differently to gaming?
9. **Regulatory effectiveness**: Can policymaker interventions restore benchmark validity?
10. **Media amplification**: Does media coverage accelerate or dampen gaming dynamics?
11. **Funding dynamics**: Does capital flow to high-performers or low-gaming providers?
12. **Funding as accelerator**: Does funding amplify existing dynamics (help winners win more)?
13. **Benchmark renewal**: Does introducing new benchmarks effectively reset gaming incentives?
14. **Information cascades**: Do media headlines create herding behavior across consumers, funders, and policymakers?

---

# Part 7: File Structure

```
eval_sim/
├── actors/
│   ├── __init__.py
│   ├── model_provider.py    # ModelProvider class (per-provider visibility)
│   ├── evaluator.py         # Evaluator class (benchmark evolution + introduction)
│   ├── consumer.py          # ConsumerMarket + MarketSegment (proportional switching)
│   ├── policymaker.py       # Policymaker class (media-aware)
│   ├── funder.py            # Funder class (VC, Gov, Foundation; media-aware)
│   └── media.py             # Media actor (TechPress; coverage + influence)
├── visibility.py            # Visibility system (public/private/ground truth)
├── simulation.py            # Main simulation loop, r4() precision utility
├── llm.py                   # Multi-provider LLM integration (OpenAI, Anthropic, Ollama, Gemini)
├── experiment_logger.py     # Experiment logging and tracking
├── game_log.py              # Game log markdown generator
├── plotting.py              # Visualization dashboards (market shares as proportions)
├── run_experiment.py        # Editable experiment config file
├── run_llm_now.py           # CLI-driven quick experiment runner
├── stakeholders.md          # This document
├── .env                     # API keys (not committed)
└── experiments/             # Experiment results
    ├── index.json           # Experiment index
    └── exp_XXX_name/        # Individual experiment folders
```
