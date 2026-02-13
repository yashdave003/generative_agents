# Game Log: 5p_2b_3funder_highcap

**Experiment ID:** heur_003_5p_2b_3funder_highcap
**Mode:** Heuristic
**Total Rounds:** 30

**Benchmarks (2):**
- **coding_bench**: validity=0.55, exploitability=0.35, weight=0.5
- **reasoning_bench**: validity=0.7, exploitability=0.45, weight=0.5

---

## Round 0

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.837 | 0.680 | 30% | 25% | 15% | 30% |
| 2 | OpenAI | 0.774 | 0.720 | 20% | 40% | 25% | 15% |
| 3 | DeepMind | 0.748 | 0.700 | 35% | 30% | 15% | 20% |
| 4 | Meta_AI | 0.678 | 0.650 | 25% | 35% | 20% | 20% |
| 5 | NovaMind | 0.507 | 0.550 | 15% | 30% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| Anthropic | 0.814 | 0.860 |
| OpenAI | 0.840 | 0.708 |
| DeepMind | 0.766 | 0.730 |
| Meta_AI | 0.718 | 0.638 |
| NovaMind | 0.462 | 0.552 |

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,453,740 to Anthropic

### Consumer Market
- Avg Satisfaction: 0.688
- Switching Rate: 34.5%
- Market Shares: Anthropic: 51.8%, OpenAI: 23.1%, DeepMind: 15.2%, Meta_AI: 8.8%, NovaMind: 1.0%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | DeepMind | 0.883 | 0.704 | 21% | 25% | 34% | 20% |
| 2 | OpenAI | 0.869 | 0.725 | 22% | 25% | 28% | 25% |
| 3 | Anthropic | 0.853 | 0.688 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.764 | 0.654 | 19% | 25% | 36% | 20% |
| 5 | NovaMind | 0.701 | 0.554 | 15% | 25% | 40% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| DeepMind | 0.766 | 1.000 |
| OpenAI | 0.840 | 0.897 |
| Anthropic | 0.814 | 0.892 |
| Meta_AI | 0.764 | 0.765 |
| NovaMind | 0.689 | 0.713 |

### Score Changes
- **OpenAI**: 0.774 -> 0.869 (+0.095)
- **Anthropic**: 0.837 -> 0.853 (+0.016)
- **NovaMind**: 0.507 -> 0.701 (+0.194)
- **DeepMind**: 0.748 -> 0.883 (+0.135)
- **Meta_AI**: 0.678 -> 0.764 (+0.086)

### Events
- **DeepMind** moved up from #3 to #1
- **Anthropic** moved down from #1 to #3
- **DeepMind** shifted strategy toward more eval engineering (19% change)
- **Meta_AI** shifted strategy toward more eval engineering (16% change)
- **Regulation** by Regulator: investigation
- **Consumer movement**: 19.9% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Score volatility detected
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,453,740 to Anthropic

### Media Coverage
- Sentiment: 0.85 (positive)
- DeepMind takes the lead from Anthropic
- DeepMind surges by 0.135
- DeepMind appears to release major model update
- OpenAI surges by 0.095
- OpenAI appears to release major model update
- Meta_AI surges by 0.086
- Meta_AI appears to release major model update
- NovaMind surges by 0.194
- NovaMind appears to release major model update
- Anthropic raises $120,000,000 from TechVentures
- Anthropic raises $30,000,000 from Horizon_Capital
- Anthropic raises $2,453,740 from AISI_Fund
- DeepMind takes #1 on reasoning_bench

### Consumer Market
- Avg Satisfaction: 0.700
- Switching Rate: 19.9%
- Market Shares: Anthropic: 48.0%, OpenAI: 35.4%, DeepMind: 11.0%, Meta_AI: 5.3%, NovaMind: 0.4%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.949 | 0.730 | 23% | 25% | 27% | 25% |
| 2 | DeepMind | 0.905 | 0.708 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.853 | 0.695 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.829 | 0.658 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.814 | 0.558 | 17% | 25% | 38% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.897 |
| DeepMind | 0.811 | 1.000 |
| Anthropic | 0.814 | 0.892 |
| Meta_AI | 0.764 | 0.895 |
| NovaMind | 0.760 | 0.867 |

### Score Changes
- **OpenAI**: 0.869 -> 0.949 (+0.080)
- **Anthropic**: 0.853 -> 0.853 (+0.000)
- **NovaMind**: 0.701 -> 0.814 (+0.113)
- **DeepMind**: 0.883 -> 0.905 (+0.022)
- **Meta_AI**: 0.764 -> 0.829 (+0.065)

### Events
- **OpenAI** moved up from #2 to #1
- **DeepMind** moved down from #1 to #2
- **Consumer movement**: 12.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,598,544 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes the lead from DeepMind
- OpenAI surges by 0.080
- Meta_AI surges by 0.065
- NovaMind surges by 0.113
- NovaMind appears to release major model update
- Regulator launches investigation into score_volatility
- OpenAI sees surge in adoption (market share +12.3%)
- Consumers are turning away from Anthropic (market share -3.8%)
- Consumers are turning away from DeepMind (market share -4.3%)
- Consumers are turning away from Meta_AI (market share -3.5%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.710
- Switching Rate: 12.2%
- Market Shares: OpenAI: 44.6%, Anthropic: 43.1%, DeepMind: 8.6%, Meta_AI: 3.4%, NovaMind: 0.2%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.949 | 0.737 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.916 | 0.713 | 23% | 25% | 32% | 20% |
| 3 | Meta_AI | 0.873 | 0.663 | 21% | 25% | 34% | 20% |
| 4 | Anthropic | 0.860 | 0.700 | 28% | 25% | 22% | 25% |
| 5 | NovaMind | 0.814 | 0.564 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.897 |
| DeepMind | 0.833 | 1.000 |
| Meta_AI | 0.852 | 0.895 |
| Anthropic | 0.814 | 0.906 |
| NovaMind | 0.760 | 0.867 |

### Score Changes
- **OpenAI**: 0.949 -> 0.949 (+0.000)
- **Anthropic**: 0.853 -> 0.860 (+0.007)
- **NovaMind**: 0.814 -> 0.814 (+0.000)
- **DeepMind**: 0.905 -> 0.916 (+0.011)
- **Meta_AI**: 0.829 -> 0.873 (+0.044)

### Events
- **Meta_AI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 15.2% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,598,544 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- OpenAI raises $2,598,544 from AISI_Fund
- OpenAI sees surge in adoption (market share +9.2%)
- Consumers are turning away from Anthropic (market share -4.8%)

### Consumer Market
- Avg Satisfaction: 0.719
- Switching Rate: 15.2%
- Market Shares: OpenAI: 50.3%, Anthropic: 31.2%, DeepMind: 15.9%, Meta_AI: 2.4%, NovaMind: 0.1%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.989 | 0.743 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.955 | 0.717 | 22% | 25% | 33% | 20% |
| 3 | Meta_AI | 0.873 | 0.667 | 20% | 25% | 35% | 20% |
| 4 | Anthropic | 0.860 | 0.704 | 26% | 25% | 24% | 25% |
| 5 | NovaMind | 0.814 | 0.569 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.979 |
| DeepMind | 0.909 | 1.000 |
| Meta_AI | 0.852 | 0.895 |
| Anthropic | 0.814 | 0.906 |
| NovaMind | 0.760 | 0.867 |

### Score Changes
- **OpenAI**: 0.949 -> 0.989 (+0.041)
- **Anthropic**: 0.860 -> 0.860 (+0.000)
- **NovaMind**: 0.814 -> 0.814 (+0.000)
- **DeepMind**: 0.916 -> 0.955 (+0.038)
- **Meta_AI**: 0.873 -> 0.873 (+0.000)

### Events
- **Consumer movement**: 12.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,802,331 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- OpenAI sees surge in adoption (market share +5.8%)
- Consumers are turning away from Anthropic (market share -11.9%)
- DeepMind sees surge in adoption (market share +7.3%)

### Consumer Market
- Avg Satisfaction: 0.729
- Switching Rate: 12.4%
- Market Shares: OpenAI: 58.1%, Anthropic: 22.1%, DeepMind: 18.0%, Meta_AI: 1.7%, NovaMind: 0.1%

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.989 | 0.750 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.955 | 0.722 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.888 | 0.709 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.873 | 0.671 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.814 | 0.574 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.979 |
| DeepMind | 0.909 | 1.000 |
| Anthropic | 0.870 | 0.906 |
| Meta_AI | 0.852 | 0.895 |
| NovaMind | 0.760 | 0.867 |

### Score Changes
- **OpenAI**: 0.989 -> 0.989 (+0.000)
- **Anthropic**: 0.860 -> 0.888 (+0.028)
- **NovaMind**: 0.814 -> 0.814 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.873 -> 0.873 (+0.000)

### Events
- **Anthropic** moved up from #4 to #3
- **Meta_AI** moved down from #3 to #4
- **Consumer movement**: 10.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,802,331 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +7.7%)
- Consumers are turning away from Anthropic (market share -9.1%)

### Consumer Market
- Avg Satisfaction: 0.738
- Switching Rate: 10.7%
- Market Shares: OpenAI: 67.1%, DeepMind: 15.9%, Anthropic: 15.7%, Meta_AI: 1.2%, NovaMind: 0.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.989 | 0.756 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.955 | 0.728 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.888 | 0.714 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.873 | 0.675 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.814 | 0.578 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.979 |
| DeepMind | 0.909 | 1.000 |
| Anthropic | 0.871 | 0.906 |
| Meta_AI | 0.852 | 0.895 |
| NovaMind | 0.760 | 0.867 |

### Score Changes
- **OpenAI**: 0.989 -> 0.989 (+0.000)
- **Anthropic**: 0.888 -> 0.888 (+0.001)
- **NovaMind**: 0.814 -> 0.814 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.873 -> 0.873 (+0.000)

### Events
- **Consumer movement**: 9.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,065,437 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +9.0%)
- Consumers are turning away from Anthropic (market share -6.5%)

### Consumer Market
- Avg Satisfaction: 0.747
- Switching Rate: 9.7%
- Market Shares: OpenAI: 76.8%, Anthropic: 11.2%, DeepMind: 11.0%, Meta_AI: 0.9%, NovaMind: 0.1%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.989 | 0.763 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.955 | 0.732 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.888 | 0.718 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.873 | 0.681 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.814 | 0.583 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 0.979 | 0.000 |
| DeepMind | 0.909 | 1.000 | 0.000 |
| Anthropic | 0.871 | 0.906 | 0.000 |
| Meta_AI | 0.852 | 0.895 | 0.000 |
| NovaMind | 0.760 | 0.867 | 0.000 |

### Score Changes
- **OpenAI**: 0.989 -> 0.989 (+0.000)
- **Anthropic**: 0.888 -> 0.888 (+0.000)
- **NovaMind**: 0.814 -> 0.814 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.873 -> 0.873 (+0.000)

### Events
- **Consumer movement**: 6.6% of market switched providers

### New Benchmark Introduced
- **reasoning** introduced (validity=0.50, exploitability=0.15)
  - Trigger: periodic_introduction:round_7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,065,437 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- New benchmark introduced: reasoning
- OpenAI sees surge in adoption (market share +9.7%)
- Consumers are turning away from Anthropic (market share -4.5%)
- Consumers are turning away from DeepMind (market share -4.9%)

### Consumer Market
- Avg Satisfaction: 0.756
- Switching Rate: 6.6%
- Market Shares: OpenAI: 83.3%, Anthropic: 8.1%, DeepMind: 7.8%, Meta_AI: 0.7%, NovaMind: 0.1%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.900 | 0.723 | 26% | 25% | 24% | 25% |
| 2 | Meta_AI | 0.841 | 0.686 | 21% | 25% | 34% | 20% |
| 3 | OpenAI | 0.840 | 0.769 | 25% | 25% | 25% | 25% |
| 4 | NovaMind | 0.822 | 0.587 | 19% | 25% | 36% | 20% |
| 5 | DeepMind | 0.817 | 0.736 | 23% | 25% | 32% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.871 | 0.906 | 0.912 |
| Meta_AI | 0.852 | 0.895 | 0.809 |
| OpenAI | 1.000 | 0.979 | 0.691 |
| NovaMind | 0.806 | 0.867 | 0.807 |
| DeepMind | 0.909 | 1.000 | 0.679 |

### Score Changes
- **OpenAI**: 0.989 -> 0.840 (-0.149)
- **Anthropic**: 0.888 -> 0.900 (+0.012)
- **NovaMind**: 0.814 -> 0.822 (+0.008)
- **DeepMind**: 0.955 -> 0.817 (-0.138)
- **Meta_AI**: 0.873 -> 0.841 (-0.032)

### Events
- **Anthropic** moved up from #3 to #1
- **Meta_AI** moved up from #4 to #2
- **OpenAI** moved down from #1 to #3
- **NovaMind** moved up from #5 to #4
- **DeepMind** moved down from #2 to #5
- **Regulation** by Regulator: public_warning

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.30
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,200,839 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Anthropic takes the lead from OpenAI
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI sees surge in adoption (market share +6.6%)
- Consumers are turning away from Anthropic (market share -3.1%)
- Consumers are turning away from DeepMind (market share -3.2%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.763
- Switching Rate: 3.6%
- Market Shares: OpenAI: 87.0%, Anthropic: 6.3%, DeepMind: 6.1%, Meta_AI: 0.6%, NovaMind: 0.1%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.930 | 0.775 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.900 | 0.729 | 28% | 25% | 22% | 25% |
| 3 | DeepMind | 0.880 | 0.740 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.841 | 0.690 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.822 | 0.592 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.859 |
| Anthropic | 0.871 | 0.906 | 0.912 |
| DeepMind | 0.909 | 1.000 | 0.805 |
| Meta_AI | 0.852 | 0.895 | 0.809 |
| NovaMind | 0.806 | 0.867 | 0.807 |

### Score Changes
- **OpenAI**: 0.840 -> 0.930 (+0.090)
- **Anthropic**: 0.900 -> 0.900 (+0.000)
- **NovaMind**: 0.822 -> 0.822 (+0.000)
- **DeepMind**: 0.817 -> 0.880 (+0.063)
- **Meta_AI**: 0.841 -> 0.841 (+0.000)

### Events
- **OpenAI** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **DeepMind** moved up from #5 to #3
- **Meta_AI** moved down from #2 to #4
- **NovaMind** moved down from #4 to #5

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,200,839 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- OpenAI takes the lead from Anthropic
- OpenAI surges by 0.090
- OpenAI appears to release major model update
- DeepMind surges by 0.063
- Regulator issues public warning about AI safety concerns
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI takes #1 on reasoning_bench
- OpenAI sees surge in adoption (market share +3.6%)
- Risk signals: regulatory_public_warning, low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.771
- Switching Rate: 2.6%
- Market Shares: OpenAI: 89.6%, Anthropic: 5.1%, DeepMind: 4.9%, Meta_AI: 0.5%, NovaMind: 0.1%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.944 | 0.734 | 29% | 25% | 21% | 25% |
| 2 | OpenAI | 0.930 | 0.782 | 26% | 25% | 24% | 25% |
| 3 | DeepMind | 0.892 | 0.744 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.841 | 0.695 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.822 | 0.596 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.871 | 0.906 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.859 |
| DeepMind | 0.957 | 1.000 | 0.805 |
| Meta_AI | 0.852 | 0.895 | 0.809 |
| NovaMind | 0.806 | 0.867 | 0.807 |

### Score Changes
- **OpenAI**: 0.930 -> 0.930 (+0.000)
- **Anthropic**: 0.900 -> 0.944 (+0.044)
- **NovaMind**: 0.822 -> 0.822 (+0.000)
- **DeepMind**: 0.880 -> 0.892 (+0.012)
- **Meta_AI**: 0.841 -> 0.841 (+0.000)

### Events
- **Anthropic** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,957,555 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- Anthropic takes the lead from OpenAI
- Benchmark reasoning validity concerns (validity=0.50)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.778
- Switching Rate: 1.9%
- Market Shares: OpenAI: 91.5%, Anthropic: 4.2%, DeepMind: 4.0%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.965 | 0.740 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.930 | 0.788 | 25% | 25% | 25% | 25% |
| 3 | Meta_AI | 0.903 | 0.699 | 23% | 25% | 32% | 20% |
| 4 | DeepMind | 0.892 | 0.749 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.840 | 0.601 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.954 | 0.906 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.859 |
| Meta_AI | 0.994 | 1.000 | 0.809 |
| DeepMind | 0.957 | 1.000 | 0.805 |
| NovaMind | 0.840 | 0.867 | 0.825 |

### Score Changes
- **OpenAI**: 0.930 -> 0.930 (+0.000)
- **Anthropic**: 0.944 -> 0.965 (+0.021)
- **NovaMind**: 0.822 -> 0.840 (+0.018)
- **DeepMind**: 0.892 -> 0.892 (+0.000)
- **Meta_AI**: 0.841 -> 0.903 (+0.062)

### Events
- **Meta_AI** moved up from #4 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,957,555 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Meta_AI surges by 0.062
- Benchmark reasoning validity concerns (validity=0.50)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.785
- Switching Rate: 1.5%
- Market Shares: OpenAI: 92.9%, Anthropic: 3.5%, DeepMind: 3.2%, Meta_AI: 0.3%, NovaMind: 0.1%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.965 | 0.746 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.930 | 0.794 | 25% | 25% | 25% | 25% |
| 3 | Meta_AI | 0.927 | 0.703 | 23% | 25% | 32% | 20% |
| 4 | DeepMind | 0.892 | 0.753 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.840 | 0.606 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.954 | 0.906 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.859 |
| Meta_AI | 0.994 | 1.000 | 0.856 |
| DeepMind | 0.957 | 1.000 | 0.805 |
| NovaMind | 0.840 | 0.867 | 0.825 |

### Score Changes
- **OpenAI**: 0.930 -> 0.930 (+0.000)
- **Anthropic**: 0.965 -> 0.965 (+0.000)
- **NovaMind**: 0.840 -> 0.840 (+0.000)
- **DeepMind**: 0.892 -> 0.892 (+0.000)
- **Meta_AI**: 0.903 -> 0.927 (+0.023)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,915,534 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.50)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.791
- Switching Rate: 1.1%
- Market Shares: OpenAI: 94.0%, Anthropic: 2.9%, DeepMind: 2.7%, Meta_AI: 0.3%, NovaMind: 0.1%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.969 | 0.751 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.950 | 0.800 | 24% | 25% | 26% | 25% |
| 3 | Meta_AI | 0.928 | 0.709 | 23% | 25% | 32% | 20% |
| 4 | DeepMind | 0.905 | 0.757 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.840 | 0.610 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.968 | 0.906 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.900 |
| Meta_AI | 1.000 | 1.000 | 0.856 |
| DeepMind | 0.957 | 1.000 | 0.831 |
| NovaMind | 0.840 | 0.867 | 0.825 |

### Score Changes
- **OpenAI**: 0.930 -> 0.950 (+0.021)
- **Anthropic**: 0.965 -> 0.969 (+0.004)
- **NovaMind**: 0.840 -> 0.840 (+0.000)
- **DeepMind**: 0.892 -> 0.905 (+0.013)
- **Meta_AI**: 0.927 -> 0.928 (+0.002)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,915,534 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.50)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.798
- Switching Rate: 0.9%
- Market Shares: OpenAI: 95.0%, Anthropic: 2.5%, DeepMind: 2.2%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 1.000 | 0.714 | 23% | 25% | 32% | 20% |
| 2 | Anthropic | 0.969 | 0.756 | 30% | 25% | 20% | 25% |
| 3 | OpenAI | 0.950 | 0.806 | 24% | 25% | 26% | 25% |
| 4 | DeepMind | 0.905 | 0.761 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.840 | 0.615 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.000 |
| Anthropic | 0.968 | 0.906 | 1.000 | 0.000 |
| OpenAI | 1.000 | 1.000 | 0.900 | 0.000 |
| DeepMind | 0.957 | 1.000 | 0.831 | 0.000 |
| NovaMind | 0.840 | 0.867 | 0.825 | 0.000 |

### Score Changes
- **OpenAI**: 0.950 -> 0.950 (+0.000)
- **Anthropic**: 0.969 -> 0.969 (+0.000)
- **NovaMind**: 0.840 -> 0.840 (+0.000)
- **DeepMind**: 0.905 -> 0.905 (+0.000)
- **Meta_AI**: 0.928 -> 1.000 (+0.072)

### Events
- **Meta_AI** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **OpenAI** moved down from #2 to #3

### New Benchmark Introduced
- **question_answering** introduced (validity=0.85, exploitability=0.15)
  - Trigger: periodic_introduction:round_14

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,958,758 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- Meta_AI takes the lead from Anthropic
- Meta_AI surges by 0.072
- New benchmark introduced: question_answering
- Benchmark reasoning validity concerns (validity=0.49)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.804
- Switching Rate: 0.7%
- Market Shares: OpenAI: 95.7%, Anthropic: 2.2%, DeepMind: 1.9%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.983 | 0.720 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.906 | 0.812 | 24% | 25% | 26% | 25% |
| 3 | Anthropic | 0.901 | 0.760 | 30% | 25% | 20% | 25% |
| 4 | DeepMind | 0.874 | 0.765 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.812 | 0.619 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| OpenAI | 1.000 | 1.000 | 0.901 | 0.818 |
| Anthropic | 0.968 | 0.906 | 1.000 | 0.767 |
| DeepMind | 0.957 | 1.000 | 0.831 | 0.813 |
| NovaMind | 0.840 | 0.867 | 0.825 | 0.758 |

### Score Changes
- **OpenAI**: 0.950 -> 0.906 (-0.044)
- **Anthropic**: 0.969 -> 0.901 (-0.067)
- **NovaMind**: 0.840 -> 0.812 (-0.027)
- **DeepMind**: 0.905 -> 0.874 (-0.031)
- **Meta_AI**: 1.000 -> 0.983 (-0.017)

### Events
- **OpenAI** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,958,758 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.810
- Switching Rate: 0.6%
- Market Shares: OpenAI: 96.3%, Anthropic: 1.9%, DeepMind: 1.6%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.983 | 0.725 | 25% | 25% | 30% | 20% |
| 2 | OpenAI | 0.933 | 0.818 | 24% | 25% | 26% | 25% |
| 3 | DeepMind | 0.920 | 0.769 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.913 | 0.765 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.812 | 0.624 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| OpenAI | 1.000 | 1.000 | 0.901 | 0.899 |
| DeepMind | 0.957 | 1.000 | 0.836 | 0.946 |
| Anthropic | 0.968 | 0.975 | 1.000 | 0.767 |
| NovaMind | 0.840 | 0.867 | 0.825 | 0.758 |

### Score Changes
- **OpenAI**: 0.906 -> 0.933 (+0.027)
- **Anthropic**: 0.901 -> 0.913 (+0.012)
- **NovaMind**: 0.812 -> 0.812 (+0.000)
- **DeepMind**: 0.874 -> 0.920 (+0.045)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### Events
- **DeepMind** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,973,361 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.816
- Switching Rate: 0.5%
- Market Shares: OpenAI: 96.8%, Anthropic: 1.6%, DeepMind: 1.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.983 | 0.731 | 26% | 25% | 29% | 20% |
| 2 | Anthropic | 0.979 | 0.769 | 28% | 25% | 22% | 25% |
| 3 | OpenAI | 0.933 | 0.823 | 23% | 25% | 27% | 25% |
| 4 | DeepMind | 0.924 | 0.773 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.838 | 0.628 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| Anthropic | 0.968 | 1.000 | 1.000 | 0.953 |
| OpenAI | 1.000 | 1.000 | 0.901 | 0.899 |
| DeepMind | 0.982 | 1.000 | 0.836 | 0.946 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.758 |

### Score Changes
- **OpenAI**: 0.933 -> 0.933 (+0.000)
- **Anthropic**: 0.913 -> 0.979 (+0.066)
- **NovaMind**: 0.812 -> 0.838 (+0.026)
- **DeepMind**: 0.920 -> 0.924 (+0.004)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### Events
- **Anthropic** moved up from #4 to #2
- **OpenAI** moved down from #2 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,973,361 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- Anthropic surges by 0.066
- Benchmark reasoning validity concerns (validity=0.49)
- Anthropic takes #1 on question_answering
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.822
- Switching Rate: 0.4%
- Market Shares: OpenAI: 97.2%, Anthropic: 1.4%, DeepMind: 1.1%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.983 | 0.736 | 26% | 25% | 29% | 20% |
| 2 | Anthropic | 0.979 | 0.774 | 29% | 25% | 21% | 25% |
| 3 | OpenAI | 0.967 | 0.829 | 23% | 25% | 27% | 25% |
| 4 | DeepMind | 0.933 | 0.777 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.847 | 0.632 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| Anthropic | 0.968 | 1.000 | 1.000 | 0.953 |
| OpenAI | 1.000 | 1.000 | 0.901 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.861 | 0.946 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.785 |

### Score Changes
- **OpenAI**: 0.933 -> 0.967 (+0.034)
- **Anthropic**: 0.979 -> 0.979 (+0.000)
- **NovaMind**: 0.838 -> 0.847 (+0.009)
- **DeepMind**: 0.924 -> 0.933 (+0.008)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,906,081 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- OpenAI takes #1 on question_answering
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.827
- Switching Rate: 2.1%
- Market Shares: OpenAI: 95.7%, Anthropic: 3.1%, DeepMind: 1.0%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.835 | 24% | 25% | 26% | 25% |
| 2 | Meta_AI | 0.983 | 0.741 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.979 | 0.780 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.933 | 0.781 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.847 | 0.637 | 20% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| Anthropic | 0.968 | 1.000 | 1.000 | 0.953 |
| DeepMind | 0.982 | 1.000 | 0.861 | 0.946 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.785 |

### Score Changes
- **OpenAI**: 0.967 -> 0.999 (+0.032)
- **Anthropic**: 0.979 -> 0.979 (+0.000)
- **NovaMind**: 0.847 -> 0.847 (+0.000)
- **DeepMind**: 0.933 -> 0.933 (+0.000)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### Events
- **OpenAI** moved up from #3 to #1
- **Meta_AI** moved down from #1 to #2
- **Anthropic** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,906,081 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes the lead from Meta_AI
- Benchmark reasoning validity concerns (validity=0.49)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.833
- Switching Rate: 1.1%
- Market Shares: OpenAI: 96.8%, Anthropic: 2.1%, DeepMind: 0.9%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.840 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.984 | 0.785 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.983 | 0.745 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.933 | 0.785 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.847 | 0.641 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 |
| DeepMind | 0.982 | 1.000 | 0.861 | 0.946 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.785 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.979 -> 0.984 (+0.005)
- **NovaMind**: 0.847 -> 0.847 (+0.000)
- **DeepMind**: 0.933 -> 0.933 (+0.000)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### Events
- **Anthropic** moved up from #3 to #2
- **Meta_AI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,043,867 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.839
- Switching Rate: 0.7%
- Market Shares: OpenAI: 97.5%, Anthropic: 1.6%, DeepMind: 0.7%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.846 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.984 | 0.790 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.983 | 0.749 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.970 | 0.790 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.847 | 0.645 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 | 0.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 0.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 0.000 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.785 | 0.000 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.984 -> 0.984 (+0.000)
- **NovaMind**: 0.847 -> 0.847 (+0.000)
- **DeepMind**: 0.933 -> 0.970 (+0.037)
- **Meta_AI**: 0.983 -> 0.983 (+0.000)

### New Benchmark Introduced
- **factual_recall** introduced (validity=0.40, exploitability=0.50)
  - Trigger: periodic_introduction:round_21

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,043,867 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- New benchmark introduced: factual_recall
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.844
- Switching Rate: 0.5%
- Market Shares: OpenAI: 98.0%, Anthropic: 1.2%, DeepMind: 0.6%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.851 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.977 | 0.794 | 23% | 25% | 32% | 20% |
| 3 | Meta_AI | 0.976 | 0.754 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.944 | 0.794 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.853 | 0.650 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 0.956 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 0.822 |
| NovaMind | 0.884 | 0.867 | 0.880 | 0.785 | 0.870 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.984 -> 0.944 (-0.041)
- **NovaMind**: 0.847 -> 0.853 (+0.006)
- **DeepMind**: 0.970 -> 0.977 (+0.008)
- **Meta_AI**: 0.983 -> 0.976 (-0.007)

### Events
- **DeepMind** moved up from #4 to #2
- **Anthropic** moved down from #2 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,982,308 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.850
- Switching Rate: 0.3%
- Market Shares: OpenAI: 98.3%, Anthropic: 1.0%, DeepMind: 0.6%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.857 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.987 | 0.758 | 24% | 25% | 31% | 20% |
| 3 | DeepMind | 0.977 | 0.799 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.954 | 0.798 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.877 | 0.654 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 0.862 |
| NovaMind | 0.995 | 0.953 | 0.880 | 0.785 | 0.870 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.944 -> 0.954 (+0.010)
- **NovaMind**: 0.853 -> 0.877 (+0.024)
- **DeepMind**: 0.977 -> 0.977 (+0.000)
- **Meta_AI**: 0.976 -> 0.987 (+0.011)

### Events
- **Meta_AI** moved up from #3 to #2
- **DeepMind** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,982,308 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.856
- Switching Rate: 0.2%
- Market Shares: OpenAI: 98.6%, Anthropic: 0.8%, DeepMind: 0.5%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.862 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.987 | 0.762 | 24% | 25% | 31% | 20% |
| 3 | DeepMind | 0.977 | 0.804 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.954 | 0.803 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.911 | 0.658 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.997 | 1.000 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 0.862 |
| NovaMind | 0.995 | 0.953 | 0.880 | 0.830 | 0.959 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.954 -> 0.954 (+0.000)
- **NovaMind**: 0.877 -> 0.911 (+0.033)
- **DeepMind**: 0.977 -> 0.977 (+0.000)
- **Meta_AI**: 0.987 -> 0.987 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,958,880 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.861
- Switching Rate: 0.2%
- Market Shares: OpenAI: 98.7%, Anthropic: 0.7%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.867 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.988 | 0.807 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.987 | 0.766 | 24% | 25% | 30% | 20% |
| 4 | DeepMind | 0.977 | 0.808 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.914 | 0.664 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 1.000 |
| NovaMind | 0.995 | 0.953 | 0.896 | 0.830 | 0.959 |

### Score Changes
- **OpenAI**: 0.999 -> 1.000 (+0.001)
- **Anthropic**: 0.954 -> 0.988 (+0.034)
- **NovaMind**: 0.911 -> 0.914 (+0.004)
- **DeepMind**: 0.977 -> 0.977 (+0.000)
- **Meta_AI**: 0.987 -> 0.987 (+0.000)

### Events
- **Anthropic** moved up from #4 to #2
- **Meta_AI** moved down from #2 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,958,880 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- OpenAI takes #1 on reasoning
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.867
- Switching Rate: 0.1%
- Market Shares: OpenAI: 98.9%, Anthropic: 0.6%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.873 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.988 | 0.811 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.987 | 0.770 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.977 | 0.812 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.914 | 0.669 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.953 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 1.000 |
| DeepMind | 0.982 | 1.000 | 0.963 | 0.954 | 1.000 |
| NovaMind | 0.995 | 0.953 | 0.896 | 0.830 | 0.959 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.988 -> 0.988 (+0.000)
- **NovaMind**: 0.914 -> 0.914 (+0.000)
- **DeepMind**: 0.977 -> 0.977 (+0.000)
- **Meta_AI**: 0.987 -> 0.987 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,937,202 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.872
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.0%, Anthropic: 0.5%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.878 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 1.000 | 0.816 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.987 | 0.774 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.979 | 0.816 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.918 | 0.674 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.948 | 1.000 |
| DeepMind | 1.000 | 1.000 | 0.963 | 0.954 | 1.000 |
| NovaMind | 0.995 | 0.953 | 0.910 | 0.830 | 0.959 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 0.988 -> 1.000 (+0.012)
- **NovaMind**: 0.914 -> 0.918 (+0.004)
- **DeepMind**: 0.977 -> 0.979 (+0.002)
- **Meta_AI**: 0.987 -> 0.987 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,937,202 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.877
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.1%, Anthropic: 0.5%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.883 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 1.000 | 0.822 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.992 | 0.779 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.979 | 0.820 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.918 | 0.678 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.967 | 1.000 | 0.000 |
| DeepMind | 1.000 | 1.000 | 0.963 | 0.954 | 1.000 | 0.000 |
| NovaMind | 0.995 | 0.953 | 0.910 | 0.830 | 0.959 | 0.000 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 1.000 -> 1.000 (+0.000)
- **NovaMind**: 0.918 -> 0.918 (+0.000)
- **DeepMind**: 0.979 -> 0.979 (+0.000)
- **Meta_AI**: 0.987 -> 0.992 (+0.005)

### New Benchmark Introduced
- **accounting** introduced (validity=0.70, exploitability=0.25)
  - Trigger: validity_decay:factual_recall=0.40

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,947,150 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- New benchmark introduced: accounting
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.882
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.2%, Anthropic: 0.4%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.888 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.980 | 0.827 | 30% | 25% | 20% | 25% |
| 3 | DeepMind | 0.928 | 0.823 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.926 | 0.783 | 25% | 25% | 30% | 20% |
| 5 | NovaMind | 0.916 | 0.682 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.897 |
| DeepMind | 1.000 | 1.000 | 0.963 | 0.977 | 1.000 | 0.698 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.967 | 1.000 | 0.665 |
| NovaMind | 0.995 | 1.000 | 0.910 | 0.879 | 0.959 | 0.835 |

### Score Changes
- **OpenAI**: 1.000 -> 1.000 (+0.000)
- **Anthropic**: 1.000 -> 0.980 (-0.020)
- **NovaMind**: 0.918 -> 0.916 (-0.002)
- **DeepMind**: 0.979 -> 0.928 (-0.052)
- **Meta_AI**: 0.992 -> 0.926 (-0.065)

### Events
- **DeepMind** moved up from #4 to #3
- **Meta_AI** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,947,150 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.48)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.888
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.2%, Anthropic: 0.4%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 1.000 | +0.168 | 24% | 26% |
| 2 | Anthropic | 0.980 | +0.147 | 29% | 21% |
| 3 | DeepMind | 0.928 | +0.123 | 24% | 31% |
| 4 | Meta_AI | 0.926 | +0.133 | 23% | 32% |
| 5 | NovaMind | 0.916 | +0.132 | 20% | 35% |

### Event Summary
- **Rank changes:** 46
- **Strategy shifts:** 2
- **Regulatory actions:** 2
- **Consumer movement events:** 7

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
