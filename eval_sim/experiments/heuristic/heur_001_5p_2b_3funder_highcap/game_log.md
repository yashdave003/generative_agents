# Game Log: 5p_2b_3funder_highcap

**Experiment ID:** heur_001_5p_2b_3funder_highcap
**Mode:** Heuristic
**Total Rounds:** 30

**Benchmarks (2):**
- **coding_bench**: validity=0.85, exploitability=0.25, weight=0.5
- **reasoning_bench**: validity=0.7, exploitability=0.45, weight=0.5

---

## Round 0

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.821 | 0.680 | 30% | 25% | 15% | 30% |
| 2 | OpenAI | 0.759 | 0.720 | 20% | 40% | 25% | 15% |
| 3 | DeepMind | 0.739 | 0.700 | 35% | 30% | 15% | 20% |
| 4 | Meta_AI | 0.668 | 0.650 | 25% | 35% | 20% | 20% |
| 5 | NovaMind | 0.510 | 0.550 | 15% | 30% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| Anthropic | 0.783 | 0.860 |
| OpenAI | 0.809 | 0.708 |
| DeepMind | 0.749 | 0.730 |
| Meta_AI | 0.699 | 0.638 |
| NovaMind | 0.468 | 0.552 |

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,448,929 to Anthropic

### Consumer Market
- Avg Satisfaction: 0.688
- Switching Rate: 34.1%
- Market Shares: Anthropic: 51.7%, OpenAI: 22.9%, DeepMind: 15.4%, Meta_AI: 8.9%, NovaMind: 1.1%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | DeepMind | 0.874 | 0.704 | 21% | 25% | 34% | 20% |
| 2 | OpenAI | 0.853 | 0.725 | 22% | 25% | 28% | 25% |
| 3 | Anthropic | 0.837 | 0.688 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.747 | 0.654 | 19% | 25% | 36% | 20% |
| 5 | NovaMind | 0.680 | 0.554 | 15% | 25% | 40% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| DeepMind | 0.749 | 1.000 |
| OpenAI | 0.809 | 0.896 |
| Anthropic | 0.783 | 0.890 |
| Meta_AI | 0.730 | 0.763 |
| NovaMind | 0.649 | 0.710 |

### Score Changes
- **OpenAI**: 0.759 -> 0.853 (+0.094)
- **Anthropic**: 0.821 -> 0.837 (+0.015)
- **NovaMind**: 0.510 -> 0.680 (+0.170)
- **DeepMind**: 0.739 -> 0.874 (+0.135)
- **Meta_AI**: 0.668 -> 0.747 (+0.078)

### Events
- **DeepMind** moved up from #3 to #1
- **Anthropic** moved down from #1 to #3
- **DeepMind** shifted strategy toward more eval engineering (19% change)
- **Meta_AI** shifted strategy toward more eval engineering (16% change)
- **Regulation** by Regulator: investigation
- **Consumer movement**: 19.5% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Score volatility detected
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,448,929 to Anthropic

### Media Coverage
- Sentiment: 0.85 (positive)
- DeepMind takes the lead from Anthropic
- DeepMind surges by 0.135
- DeepMind appears to release major model update
- OpenAI surges by 0.094
- OpenAI appears to release major model update
- Meta_AI surges by 0.078
- NovaMind surges by 0.170
- NovaMind appears to release major model update
- Anthropic raises $120,000,000 from TechVentures
- Anthropic raises $30,000,000 from Horizon_Capital
- Anthropic raises $2,448,929 from AISI_Fund
- DeepMind takes #1 on reasoning_bench

### Consumer Market
- Avg Satisfaction: 0.700
- Switching Rate: 19.5%
- Market Shares: Anthropic: 48.2%, OpenAI: 34.8%, DeepMind: 11.2%, Meta_AI: 5.3%, NovaMind: 0.4%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.940 | 0.730 | 23% | 25% | 27% | 25% |
| 2 | DeepMind | 0.890 | 0.709 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.837 | 0.695 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.812 | 0.658 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.787 | 0.558 | 17% | 25% | 38% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 0.985 | 0.896 |
| DeepMind | 0.780 | 1.000 |
| Anthropic | 0.783 | 0.890 |
| Meta_AI | 0.730 | 0.894 |
| NovaMind | 0.708 | 0.866 |

### Score Changes
- **OpenAI**: 0.853 -> 0.940 (+0.088)
- **Anthropic**: 0.837 -> 0.837 (+0.000)
- **NovaMind**: 0.680 -> 0.787 (+0.107)
- **DeepMind**: 0.874 -> 0.890 (+0.016)
- **Meta_AI**: 0.747 -> 0.812 (+0.065)

### Events
- **OpenAI** moved up from #2 to #1
- **DeepMind** moved down from #1 to #2
- **Consumer movement**: 14.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,631,603 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes the lead from DeepMind
- OpenAI surges by 0.088
- OpenAI appears to release major model update
- Meta_AI surges by 0.065
- NovaMind surges by 0.107
- NovaMind appears to release major model update
- Regulator launches investigation into score_volatility
- OpenAI sees surge in adoption (market share +11.9%)
- Consumers are turning away from Anthropic (market share -3.4%)
- Consumers are turning away from DeepMind (market share -4.2%)
- Consumers are turning away from Meta_AI (market share -3.6%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.711
- Switching Rate: 14.7%
- Market Shares: OpenAI: 44.0%, Anthropic: 40.3%, DeepMind: 12.0%, Meta_AI: 3.5%, NovaMind: 0.2%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.940 | 0.737 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.899 | 0.713 | 23% | 25% | 32% | 20% |
| 3 | Meta_AI | 0.849 | 0.663 | 21% | 25% | 34% | 20% |
| 4 | Anthropic | 0.844 | 0.700 | 28% | 25% | 22% | 25% |
| 5 | NovaMind | 0.787 | 0.564 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 0.985 | 0.896 |
| DeepMind | 0.799 | 1.000 |
| Meta_AI | 0.804 | 0.894 |
| Anthropic | 0.783 | 0.906 |
| NovaMind | 0.708 | 0.866 |

### Score Changes
- **OpenAI**: 0.940 -> 0.940 (+0.000)
- **Anthropic**: 0.837 -> 0.844 (+0.008)
- **NovaMind**: 0.787 -> 0.787 (+0.000)
- **DeepMind**: 0.890 -> 0.899 (+0.009)
- **Meta_AI**: 0.812 -> 0.849 (+0.037)

### Events
- **Meta_AI** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4
- **Consumer movement**: 14.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,631,603 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- OpenAI raises $2,631,603 from AISI_Fund
- OpenAI sees surge in adoption (market share +9.2%)
- Consumers are turning away from Anthropic (market share -8.0%)

### Consumer Market
- Avg Satisfaction: 0.720
- Switching Rate: 14.8%
- Market Shares: OpenAI: 49.9%, Anthropic: 28.9%, DeepMind: 18.7%, Meta_AI: 2.4%, NovaMind: 0.1%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.981 | 0.743 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.931 | 0.717 | 22% | 25% | 33% | 20% |
| 3 | Meta_AI | 0.849 | 0.667 | 20% | 25% | 35% | 20% |
| 4 | Anthropic | 0.844 | 0.705 | 26% | 25% | 24% | 25% |
| 5 | NovaMind | 0.787 | 0.569 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 0.985 | 0.978 |
| DeepMind | 0.861 | 1.000 |
| Meta_AI | 0.804 | 0.894 |
| Anthropic | 0.783 | 0.906 |
| NovaMind | 0.708 | 0.866 |

### Score Changes
- **OpenAI**: 0.940 -> 0.981 (+0.041)
- **Anthropic**: 0.844 -> 0.844 (+0.000)
- **NovaMind**: 0.787 -> 0.787 (+0.000)
- **DeepMind**: 0.899 -> 0.931 (+0.031)
- **Meta_AI**: 0.849 -> 0.849 (+0.000)

### Events
- **Consumer movement**: 11.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,833,185 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- OpenAI sees surge in adoption (market share +5.9%)
- Consumers are turning away from Anthropic (market share -11.4%)
- DeepMind sees surge in adoption (market share +6.6%)

### Consumer Market
- Avg Satisfaction: 0.729
- Switching Rate: 11.8%
- Market Shares: OpenAI: 57.8%, Anthropic: 20.3%, DeepMind: 20.1%, Meta_AI: 1.7%, NovaMind: 0.1%

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.981 | 0.750 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.931 | 0.722 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.868 | 0.709 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.849 | 0.671 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.787 | 0.574 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 0.985 | 0.978 |
| DeepMind | 0.861 | 1.000 |
| Anthropic | 0.831 | 0.906 |
| Meta_AI | 0.804 | 0.894 |
| NovaMind | 0.708 | 0.866 |

### Score Changes
- **OpenAI**: 0.981 -> 0.981 (+0.000)
- **Anthropic**: 0.844 -> 0.868 (+0.024)
- **NovaMind**: 0.787 -> 0.787 (+0.000)
- **DeepMind**: 0.931 -> 0.931 (+0.000)
- **Meta_AI**: 0.849 -> 0.849 (+0.000)

### Events
- **Anthropic** moved up from #4 to #3
- **Meta_AI** moved down from #3 to #4
- **Consumer movement**: 10.1% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,833,185 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +7.9%)
- Consumers are turning away from Anthropic (market share -8.6%)

### Consumer Market
- Avg Satisfaction: 0.738
- Switching Rate: 10.1%
- Market Shares: OpenAI: 66.8%, DeepMind: 17.6%, Anthropic: 14.3%, Meta_AI: 1.2%, NovaMind: 0.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.981 | 0.756 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.931 | 0.728 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.869 | 0.714 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.849 | 0.675 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.787 | 0.578 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 0.985 | 0.978 |
| DeepMind | 0.861 | 1.000 |
| Anthropic | 0.833 | 0.906 |
| Meta_AI | 0.804 | 0.894 |
| NovaMind | 0.708 | 0.866 |

### Score Changes
- **OpenAI**: 0.981 -> 0.981 (+0.000)
- **Anthropic**: 0.868 -> 0.869 (+0.001)
- **NovaMind**: 0.787 -> 0.787 (+0.000)
- **DeepMind**: 0.931 -> 0.931 (+0.000)
- **Meta_AI**: 0.849 -> 0.849 (+0.000)

### Events
- **Consumer movement**: 9.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,071,100 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +9.0%)
- Consumers are turning away from Anthropic (market share -6.0%)

### Consumer Market
- Avg Satisfaction: 0.748
- Switching Rate: 9.3%
- Market Shares: OpenAI: 76.1%, DeepMind: 12.8%, Anthropic: 10.1%, Meta_AI: 0.9%, NovaMind: 0.1%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.981 | 0.763 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.931 | 0.732 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.869 | 0.718 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.849 | 0.681 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.787 | 0.582 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 0.985 | 0.978 | 0.000 |
| DeepMind | 0.861 | 1.000 | 0.000 |
| Anthropic | 0.833 | 0.906 | 0.000 |
| Meta_AI | 0.804 | 0.894 | 0.000 |
| NovaMind | 0.708 | 0.866 | 0.000 |

### Score Changes
- **OpenAI**: 0.981 -> 0.981 (+0.000)
- **Anthropic**: 0.869 -> 0.869 (+0.000)
- **NovaMind**: 0.787 -> 0.787 (+0.000)
- **DeepMind**: 0.931 -> 0.931 (+0.000)
- **Meta_AI**: 0.849 -> 0.849 (+0.000)

### Events
- **Consumer movement**: 6.4% of market switched providers

### New Benchmark Introduced
- **reasoning** introduced (validity=0.85, exploitability=0.15)
  - Trigger: periodic_introduction:round_7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,071,100 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- New benchmark introduced: reasoning
- OpenAI sees surge in adoption (market share +9.3%)
- Consumers are turning away from Anthropic (market share -4.1%)
- Consumers are turning away from DeepMind (market share -4.9%)

### Consumer Market
- Avg Satisfaction: 0.756
- Switching Rate: 6.4%
- Market Shares: OpenAI: 82.5%, DeepMind: 9.4%, Anthropic: 7.3%, Meta_AI: 0.7%, NovaMind: 0.1%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.873 | 0.723 | 26% | 25% | 24% | 25% |
| 2 | OpenAI | 0.849 | 0.769 | 26% | 25% | 24% | 25% |
| 3 | Meta_AI | 0.821 | 0.686 | 20% | 25% | 35% | 20% |
| 4 | DeepMind | 0.817 | 0.736 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.789 | 0.587 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.833 | 0.906 | 0.877 |
| OpenAI | 0.985 | 0.978 | 0.717 |
| Meta_AI | 0.804 | 0.894 | 0.793 |
| DeepMind | 0.861 | 1.000 | 0.704 |
| NovaMind | 0.753 | 0.866 | 0.769 |

### Score Changes
- **OpenAI**: 0.981 -> 0.849 (-0.132)
- **Anthropic**: 0.869 -> 0.873 (+0.004)
- **NovaMind**: 0.787 -> 0.789 (+0.002)
- **DeepMind**: 0.931 -> 0.817 (-0.113)
- **Meta_AI**: 0.849 -> 0.821 (-0.028)

### Events
- **Anthropic** moved up from #3 to #1
- **OpenAI** moved down from #1 to #2
- **Meta_AI** moved up from #4 to #3
- **DeepMind** moved down from #2 to #4
- **Regulation** by Regulator: public_warning

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.30
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,240,500 to OpenAI

### Media Coverage
- Sentiment: 0.15 (positive)
- Anthropic takes the lead from OpenAI
- OpenAI sees surge in adoption (market share +6.4%)
- Consumers are turning away from DeepMind (market share -3.4%)

### Consumer Market
- Avg Satisfaction: 0.764
- Switching Rate: 3.7%
- Market Shares: OpenAI: 86.3%, DeepMind: 7.4%, Anthropic: 5.7%, Meta_AI: 0.5%, NovaMind: 0.1%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.924 | 0.776 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.873 | 0.728 | 28% | 25% | 22% | 25% |
| 3 | DeepMind | 0.866 | 0.740 | 23% | 25% | 32% | 20% |
| 4 | Meta_AI | 0.821 | 0.690 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.789 | 0.591 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.848 |
| Anthropic | 0.833 | 0.906 | 0.877 |
| DeepMind | 0.861 | 1.000 | 0.801 |
| Meta_AI | 0.804 | 0.894 | 0.793 |
| NovaMind | 0.753 | 0.866 | 0.769 |

### Score Changes
- **OpenAI**: 0.849 -> 0.924 (+0.075)
- **Anthropic**: 0.873 -> 0.873 (+0.000)
- **NovaMind**: 0.789 -> 0.789 (+0.000)
- **DeepMind**: 0.817 -> 0.866 (+0.049)
- **Meta_AI**: 0.821 -> 0.821 (+0.000)

### Events
- **OpenAI** moved up from #2 to #1
- **Anthropic** moved down from #1 to #2
- **DeepMind** moved up from #4 to #3
- **Meta_AI** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,240,500 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- OpenAI takes the lead from Anthropic
- OpenAI surges by 0.075
- Regulator issues public warning about AI safety concerns
- OpenAI takes #1 on reasoning_bench
- OpenAI sees surge in adoption (market share +3.7%)
- Risk signals: regulatory_public_warning

### Consumer Market
- Avg Satisfaction: 0.771
- Switching Rate: 2.7%
- Market Shares: OpenAI: 89.0%, DeepMind: 6.0%, Anthropic: 4.5%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.924 | 0.782 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.911 | 0.734 | 28% | 25% | 22% | 25% |
| 3 | DeepMind | 0.877 | 0.744 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.821 | 0.695 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.789 | 0.596 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.848 |
| Anthropic | 0.833 | 0.906 | 0.952 |
| DeepMind | 0.906 | 1.000 | 0.801 |
| Meta_AI | 0.804 | 0.894 | 0.793 |
| NovaMind | 0.753 | 0.866 | 0.769 |

### Score Changes
- **OpenAI**: 0.924 -> 0.924 (+0.000)
- **Anthropic**: 0.873 -> 0.911 (+0.038)
- **NovaMind**: 0.789 -> 0.789 (+0.000)
- **DeepMind**: 0.866 -> 0.877 (+0.011)
- **Meta_AI**: 0.821 -> 0.821 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,985,909 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.778
- Switching Rate: 2.1%
- Market Shares: OpenAI: 91.1%, DeepMind: 4.8%, Anthropic: 3.7%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.929 | 0.740 | 29% | 25% | 21% | 25% |
| 2 | OpenAI | 0.925 | 0.789 | 26% | 25% | 24% | 25% |
| 3 | Meta_AI | 0.878 | 0.699 | 23% | 25% | 32% | 20% |
| 4 | DeepMind | 0.877 | 0.749 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.805 | 0.601 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.908 | 0.906 | 0.952 |
| OpenAI | 1.000 | 1.000 | 0.850 |
| Meta_AI | 0.926 | 1.000 | 0.793 |
| DeepMind | 0.906 | 1.000 | 0.801 |
| NovaMind | 0.783 | 0.866 | 0.785 |

### Score Changes
- **OpenAI**: 0.924 -> 0.925 (+0.001)
- **Anthropic**: 0.911 -> 0.929 (+0.019)
- **NovaMind**: 0.789 -> 0.805 (+0.016)
- **DeepMind**: 0.877 -> 0.877 (+0.000)
- **Meta_AI**: 0.821 -> 0.878 (+0.057)

### Events
- **Anthropic** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2
- **Meta_AI** moved up from #4 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,985,909 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- Anthropic takes the lead from OpenAI
- Meta_AI surges by 0.057

### Consumer Market
- Avg Satisfaction: 0.785
- Switching Rate: 1.6%
- Market Shares: OpenAI: 92.7%, DeepMind: 3.9%, Anthropic: 3.1%, Meta_AI: 0.3%, NovaMind: 0.1%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.929 | 0.746 | 29% | 25% | 21% | 25% |
| 2 | OpenAI | 0.925 | 0.795 | 26% | 25% | 24% | 25% |
| 3 | Meta_AI | 0.898 | 0.703 | 22% | 25% | 33% | 20% |
| 4 | DeepMind | 0.877 | 0.753 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.805 | 0.605 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.908 | 0.906 | 0.952 |
| OpenAI | 1.000 | 1.000 | 0.850 |
| Meta_AI | 0.926 | 1.000 | 0.832 |
| DeepMind | 0.906 | 1.000 | 0.801 |
| NovaMind | 0.783 | 0.866 | 0.785 |

### Score Changes
- **OpenAI**: 0.925 -> 0.925 (+0.000)
- **Anthropic**: 0.929 -> 0.929 (+0.000)
- **NovaMind**: 0.805 -> 0.805 (+0.000)
- **DeepMind**: 0.877 -> 0.877 (+0.000)
- **Meta_AI**: 0.878 -> 0.898 (+0.019)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,949,485 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.792
- Switching Rate: 1.2%
- Market Shares: OpenAI: 93.9%, DeepMind: 3.2%, Anthropic: 2.6%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.943 | 0.801 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.933 | 0.751 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.916 | 0.709 | 23% | 25% | 32% | 20% |
| 4 | DeepMind | 0.889 | 0.757 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.805 | 0.610 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.886 |
| Anthropic | 0.921 | 0.906 | 0.952 |
| Meta_AI | 1.000 | 1.000 | 0.832 |
| DeepMind | 0.906 | 1.000 | 0.825 |
| NovaMind | 0.783 | 0.866 | 0.785 |

### Score Changes
- **OpenAI**: 0.925 -> 0.943 (+0.018)
- **Anthropic**: 0.929 -> 0.933 (+0.003)
- **NovaMind**: 0.805 -> 0.805 (+0.000)
- **DeepMind**: 0.877 -> 0.889 (+0.012)
- **Meta_AI**: 0.898 -> 0.916 (+0.019)

### Events
- **OpenAI** moved up from #2 to #1
- **Anthropic** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,949,485 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- OpenAI takes the lead from Anthropic

### Consumer Market
- Avg Satisfaction: 0.798
- Switching Rate: 1.0%
- Market Shares: OpenAI: 94.9%, DeepMind: 2.6%, Anthropic: 2.2%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 1.000 | 0.714 | 23% | 25% | 32% | 20% |
| 2 | OpenAI | 0.943 | 0.807 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.933 | 0.755 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.889 | 0.761 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.805 | 0.614 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.000 |
| OpenAI | 1.000 | 1.000 | 0.886 | 0.000 |
| Anthropic | 0.921 | 0.906 | 0.952 | 0.000 |
| DeepMind | 0.906 | 1.000 | 0.825 | 0.000 |
| NovaMind | 0.783 | 0.866 | 0.785 | 0.000 |

### Score Changes
- **OpenAI**: 0.943 -> 0.943 (+0.000)
- **Anthropic**: 0.933 -> 0.933 (+0.000)
- **NovaMind**: 0.805 -> 0.805 (+0.000)
- **DeepMind**: 0.889 -> 0.889 (+0.000)
- **Meta_AI**: 0.916 -> 1.000 (+0.084)

### Events
- **Meta_AI** moved up from #3 to #1
- **OpenAI** moved down from #1 to #2
- **Anthropic** moved down from #2 to #3

### New Benchmark Introduced
- **question_answering** introduced (validity=0.85, exploitability=0.15)
  - Trigger: periodic_introduction:round_14

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,969,663 to OpenAI

### Media Coverage
- Sentiment: 0.50 (positive)
- Meta_AI takes the lead from OpenAI
- Meta_AI surges by 0.084
- Meta_AI appears to release major model update
- New benchmark introduced: question_answering
- Meta_AI takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.805
- Switching Rate: 0.8%
- Market Shares: OpenAI: 95.7%, DeepMind: 2.1%, Anthropic: 1.9%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.982 | 0.720 | 24% | 25% | 31% | 20% |
| 2 | OpenAI | 0.902 | 0.813 | 25% | 25% | 25% | 25% |
| 3 | Anthropic | 0.878 | 0.760 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.863 | 0.765 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.789 | 0.619 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| OpenAI | 1.000 | 1.000 | 0.889 | 0.818 |
| Anthropic | 0.921 | 0.906 | 0.952 | 0.768 |
| DeepMind | 0.906 | 1.000 | 0.825 | 0.812 |
| NovaMind | 0.783 | 0.866 | 0.785 | 0.758 |

### Score Changes
- **OpenAI**: 0.943 -> 0.902 (-0.040)
- **Anthropic**: 0.933 -> 0.878 (-0.055)
- **NovaMind**: 0.805 -> 0.789 (-0.016)
- **DeepMind**: 0.889 -> 0.863 (-0.025)
- **Meta_AI**: 1.000 -> 0.982 (-0.018)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,969,663 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.811
- Switching Rate: 0.7%
- Market Shares: OpenAI: 96.4%, DeepMind: 1.8%, Anthropic: 1.7%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.982 | 0.725 | 25% | 25% | 30% | 20% |
| 2 | OpenAI | 0.930 | 0.819 | 24% | 25% | 26% | 25% |
| 3 | DeepMind | 0.910 | 0.769 | 22% | 25% | 33% | 20% |
| 4 | Anthropic | 0.890 | 0.764 | 28% | 25% | 22% | 25% |
| 5 | NovaMind | 0.789 | 0.623 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| OpenAI | 1.000 | 1.000 | 0.889 | 0.900 |
| DeepMind | 0.906 | 1.000 | 0.832 | 0.946 |
| Anthropic | 0.921 | 0.979 | 0.952 | 0.768 |
| NovaMind | 0.783 | 0.866 | 0.785 | 0.758 |

### Score Changes
- **OpenAI**: 0.902 -> 0.930 (+0.027)
- **Anthropic**: 0.878 -> 0.890 (+0.012)
- **NovaMind**: 0.789 -> 0.789 (+0.000)
- **DeepMind**: 0.863 -> 0.910 (+0.047)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### Events
- **DeepMind** moved up from #4 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,978,238 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.817
- Switching Rate: 0.5%
- Market Shares: OpenAI: 96.9%, DeepMind: 1.5%, Anthropic: 1.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.982 | 0.731 | 26% | 25% | 29% | 20% |
| 2 | Anthropic | 0.955 | 0.769 | 27% | 25% | 23% | 25% |
| 3 | OpenAI | 0.930 | 0.824 | 23% | 25% | 27% | 25% |
| 4 | DeepMind | 0.915 | 0.773 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.812 | 0.627 | 19% | 25% | 36% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| Anthropic | 0.921 | 1.000 | 0.952 | 0.954 |
| OpenAI | 1.000 | 1.000 | 0.889 | 0.900 |
| DeepMind | 0.932 | 1.000 | 0.832 | 0.946 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.758 |

### Score Changes
- **OpenAI**: 0.930 -> 0.930 (+0.000)
- **Anthropic**: 0.890 -> 0.955 (+0.066)
- **NovaMind**: 0.789 -> 0.812 (+0.023)
- **DeepMind**: 0.910 -> 0.915 (+0.004)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### Events
- **Anthropic** moved up from #4 to #2
- **OpenAI** moved down from #2 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,978,238 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- Anthropic surges by 0.065
- Anthropic takes #1 on question_answering

### Consumer Market
- Avg Satisfaction: 0.821
- Switching Rate: 2.2%
- Market Shares: OpenAI: 95.5%, Meta_AI: 2.0%, Anthropic: 1.3%, DeepMind: 1.3%, NovaMind: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.982 | 0.736 | 26% | 25% | 29% | 20% |
| 2 | OpenAI | 0.963 | 0.830 | 23% | 25% | 27% | 25% |
| 3 | Anthropic | 0.955 | 0.773 | 28% | 25% | 22% | 25% |
| 4 | DeepMind | 0.922 | 0.777 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.822 | 0.632 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| OpenAI | 1.000 | 1.000 | 0.889 | 1.000 |
| Anthropic | 0.921 | 1.000 | 0.952 | 0.954 |
| DeepMind | 0.932 | 1.000 | 0.854 | 0.946 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.786 |

### Score Changes
- **OpenAI**: 0.930 -> 0.963 (+0.033)
- **Anthropic**: 0.955 -> 0.955 (+0.000)
- **NovaMind**: 0.812 -> 0.822 (+0.009)
- **DeepMind**: 0.915 -> 0.922 (+0.007)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### Events
- **OpenAI** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,854,550 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes #1 on question_answering

### Consumer Market
- Avg Satisfaction: 0.824
- Switching Rate: 3.6%
- Market Shares: OpenAI: 92.4%, Meta_AI: 5.3%, Anthropic: 1.1%, DeepMind: 1.1%, NovaMind: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.990 | 0.835 | 24% | 25% | 26% | 25% |
| 2 | Meta_AI | 0.982 | 0.742 | 26% | 25% | 29% | 20% |
| 3 | Anthropic | 0.955 | 0.778 | 28% | 25% | 22% | 25% |
| 4 | DeepMind | 0.922 | 0.781 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.822 | 0.636 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| Anthropic | 0.921 | 1.000 | 0.952 | 0.954 |
| DeepMind | 0.932 | 1.000 | 0.854 | 0.946 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.786 |

### Score Changes
- **OpenAI**: 0.963 -> 0.990 (+0.027)
- **Anthropic**: 0.955 -> 0.955 (+0.000)
- **NovaMind**: 0.822 -> 0.822 (+0.000)
- **DeepMind**: 0.922 -> 0.922 (+0.000)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### Events
- **OpenAI** moved up from #2 to #1
- **Meta_AI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,854,550 to OpenAI

### Media Coverage
- Sentiment: 0.15 (positive)
- OpenAI takes the lead from Meta_AI
- Consumers are turning away from OpenAI (market share -3.0%)
- Meta_AI sees surge in adoption (market share +3.4%)

### Consumer Market
- Avg Satisfaction: 0.832
- Switching Rate: 3.0%
- Market Shares: OpenAI: 95.5%, Meta_AI: 2.6%, Anthropic: 1.0%, DeepMind: 0.9%, NovaMind: 0.1%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.990 | 0.841 | 24% | 25% | 26% | 25% |
| 2 | Meta_AI | 0.982 | 0.747 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.961 | 0.782 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.922 | 0.785 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.822 | 0.640 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 |
| Anthropic | 0.953 | 1.000 | 0.952 | 0.954 |
| DeepMind | 0.932 | 1.000 | 0.854 | 0.946 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.786 |

### Score Changes
- **OpenAI**: 0.990 -> 0.990 (+0.000)
- **Anthropic**: 0.955 -> 0.961 (+0.005)
- **NovaMind**: 0.822 -> 0.822 (+0.000)
- **DeepMind**: 0.922 -> 0.922 (+0.000)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,065,165 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +3.0%)

### Consumer Market
- Avg Satisfaction: 0.839
- Switching Rate: 1.5%
- Market Shares: OpenAI: 97.0%, Meta_AI: 1.3%, Anthropic: 0.9%, DeepMind: 0.8%, NovaMind: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.990 | 0.847 | 24% | 25% | 26% | 25% |
| 2 | Meta_AI | 0.982 | 0.752 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.961 | 0.788 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.951 | 0.789 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.822 | 0.645 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.000 |
| Anthropic | 0.953 | 1.000 | 0.952 | 0.954 | 0.000 |
| DeepMind | 0.932 | 1.000 | 0.934 | 0.953 | 0.000 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.786 | 0.000 |

### Score Changes
- **OpenAI**: 0.990 -> 0.990 (+0.000)
- **Anthropic**: 0.961 -> 0.961 (+0.000)
- **NovaMind**: 0.822 -> 0.822 (+0.000)
- **DeepMind**: 0.922 -> 0.951 (+0.029)
- **Meta_AI**: 0.982 -> 0.982 (+0.000)

### New Benchmark Introduced
- **factual_recall** introduced (validity=0.82, exploitability=0.20)
  - Trigger: periodic_introduction:round_21

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,065,165 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: factual_recall

### Consumer Market
- Avg Satisfaction: 0.845
- Switching Rate: 0.8%
- Market Shares: OpenAI: 97.8%, Anthropic: 0.8%, DeepMind: 0.7%, Meta_AI: 0.7%, NovaMind: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.980 | 0.852 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.954 | 0.792 | 23% | 25% | 32% | 20% |
| 3 | Meta_AI | 0.950 | 0.756 | 25% | 25% | 30% | 20% |
| 4 | Anthropic | 0.916 | 0.793 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.804 | 0.649 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 | 0.950 |
| DeepMind | 0.932 | 1.000 | 0.934 | 0.953 | 0.963 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.851 |
| Anthropic | 0.953 | 1.000 | 0.952 | 0.954 | 0.782 |
| NovaMind | 0.824 | 0.866 | 0.835 | 0.786 | 0.752 |

### Score Changes
- **OpenAI**: 0.990 -> 0.980 (-0.010)
- **Anthropic**: 0.961 -> 0.916 (-0.045)
- **NovaMind**: 0.822 -> 0.804 (-0.017)
- **DeepMind**: 0.951 -> 0.954 (+0.003)
- **Meta_AI**: 0.982 -> 0.950 (-0.033)

### Events
- **DeepMind** moved up from #4 to #2
- **Meta_AI** moved down from #2 to #3
- **Anthropic** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,020,135 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.851
- Switching Rate: 0.5%
- Market Shares: OpenAI: 98.3%, Anthropic: 0.7%, DeepMind: 0.6%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.980 | 0.857 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.978 | 0.760 | 24% | 25% | 31% | 20% |
| 3 | DeepMind | 0.955 | 0.797 | 23% | 25% | 32% | 20% |
| 4 | Anthropic | 0.923 | 0.797 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.827 | 0.653 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 | 0.950 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.964 |
| DeepMind | 0.932 | 1.000 | 0.934 | 0.953 | 0.967 |
| Anthropic | 0.953 | 1.000 | 0.952 | 0.954 | 0.811 |
| NovaMind | 0.917 | 0.955 | 0.835 | 0.786 | 0.752 |

### Score Changes
- **OpenAI**: 0.980 -> 0.980 (+0.000)
- **Anthropic**: 0.916 -> 0.923 (+0.007)
- **NovaMind**: 0.804 -> 0.827 (+0.023)
- **DeepMind**: 0.954 -> 0.955 (+0.001)
- **Meta_AI**: 0.950 -> 0.978 (+0.028)

### Events
- **Meta_AI** moved up from #3 to #2
- **DeepMind** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,020,135 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.856
- Switching Rate: 0.3%
- Market Shares: OpenAI: 98.6%, Anthropic: 0.6%, DeepMind: 0.5%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.980 | 0.863 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.978 | 0.764 | 25% | 25% | 30% | 20% |
| 3 | DeepMind | 0.963 | 0.802 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.923 | 0.802 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.854 | 0.657 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.969 | 1.000 | 0.950 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.964 |
| DeepMind | 0.932 | 1.000 | 0.934 | 0.953 | 1.000 |
| Anthropic | 0.953 | 1.000 | 0.952 | 0.954 | 0.811 |
| NovaMind | 0.917 | 0.955 | 0.835 | 0.830 | 0.817 |

### Score Changes
- **OpenAI**: 0.980 -> 0.980 (+0.000)
- **Anthropic**: 0.923 -> 0.923 (+0.000)
- **NovaMind**: 0.827 -> 0.854 (+0.027)
- **DeepMind**: 0.955 -> 0.963 (+0.008)
- **Meta_AI**: 0.978 -> 0.978 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,985,085 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.862
- Switching Rate: 0.2%
- Market Shares: OpenAI: 98.8%, Anthropic: 0.5%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.987 | 0.868 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.978 | 0.768 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.975 | 0.806 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.963 | 0.807 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.859 | 0.662 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 0.950 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.964 |
| Anthropic | 0.981 | 1.000 | 0.963 | 0.954 | 0.994 |
| DeepMind | 0.932 | 1.000 | 0.934 | 0.953 | 1.000 |
| NovaMind | 0.917 | 0.955 | 0.853 | 0.830 | 0.817 |

### Score Changes
- **OpenAI**: 0.980 -> 0.987 (+0.008)
- **Anthropic**: 0.923 -> 0.975 (+0.052)
- **NovaMind**: 0.854 -> 0.859 (+0.005)
- **DeepMind**: 0.963 -> 0.963 (+0.000)
- **Meta_AI**: 0.978 -> 0.978 (+0.000)

### Events
- **Anthropic** moved up from #4 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,985,085 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- Anthropic surges by 0.052
- OpenAI takes #1 on reasoning

### Consumer Market
- Avg Satisfaction: 0.867
- Switching Rate: 0.2%
- Market Shares: OpenAI: 99.0%, Anthropic: 0.5%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.874 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.978 | 0.773 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.975 | 0.810 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.965 | 0.812 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.859 | 0.666 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 0.979 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.964 |
| Anthropic | 0.981 | 1.000 | 0.963 | 0.954 | 0.994 |
| DeepMind | 0.932 | 1.000 | 0.939 | 0.953 | 1.000 |
| NovaMind | 0.917 | 0.955 | 0.853 | 0.830 | 0.817 |

### Score Changes
- **OpenAI**: 0.987 -> 0.995 (+0.007)
- **Anthropic**: 0.975 -> 0.975 (+0.000)
- **NovaMind**: 0.859 -> 0.859 (+0.000)
- **DeepMind**: 0.963 -> 0.965 (+0.001)
- **Meta_AI**: 0.978 -> 0.978 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,961,109 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.873
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.1%, Anthropic: 0.4%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.879 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.987 | 0.815 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.978 | 0.777 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.973 | 0.816 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.862 | 0.670 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 0.979 |
| Anthropic | 0.981 | 1.000 | 0.963 | 1.000 | 0.994 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.947 | 0.964 |
| DeepMind | 1.000 | 1.000 | 0.939 | 0.953 | 1.000 |
| NovaMind | 0.917 | 0.955 | 0.866 | 0.830 | 0.817 |

### Score Changes
- **OpenAI**: 0.995 -> 0.995 (+0.000)
- **Anthropic**: 0.975 -> 0.987 (+0.012)
- **NovaMind**: 0.859 -> 0.862 (+0.003)
- **DeepMind**: 0.965 -> 0.973 (+0.009)
- **Meta_AI**: 0.978 -> 0.978 (+0.000)

### Events
- **Anthropic** moved up from #3 to #2
- **Meta_AI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,961,109 to OpenAI

### Consumer Market
- Avg Satisfaction: 0.878
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.2%, Anthropic: 0.4%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.884 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.992 | 0.781 | 25% | 25% | 30% | 20% |
| 3 | Anthropic | 0.987 | 0.821 | 29% | 25% | 21% | 25% |
| 4 | DeepMind | 0.973 | 0.819 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.862 | 0.675 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 0.979 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.969 | 1.000 | 0.000 |
| Anthropic | 0.981 | 1.000 | 0.963 | 1.000 | 0.994 | 0.000 |
| DeepMind | 1.000 | 1.000 | 0.939 | 0.953 | 1.000 | 0.000 |
| NovaMind | 0.917 | 0.955 | 0.866 | 0.830 | 0.817 | 0.000 |

### Score Changes
- **OpenAI**: 0.995 -> 0.995 (+0.000)
- **Anthropic**: 0.987 -> 0.987 (+0.000)
- **NovaMind**: 0.862 -> 0.862 (+0.000)
- **DeepMind**: 0.973 -> 0.973 (+0.000)
- **Meta_AI**: 0.978 -> 0.992 (+0.014)

### Events
- **Meta_AI** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3

### New Benchmark Introduced
- **accounting** introduced (validity=0.80, exploitability=0.25)
  - Trigger: periodic_introduction:round_28

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,965,924 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- New benchmark introduced: accounting

### Consumer Market
- Avg Satisfaction: 0.883
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.3%, Anthropic: 0.3%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 1.000 | 0.889 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.969 | 0.826 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.930 | 0.785 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.926 | 0.823 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.870 | 0.679 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| Anthropic | 0.981 | 1.000 | 0.963 | 1.000 | 0.994 | 0.896 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.969 | 1.000 | 0.680 |
| DeepMind | 1.000 | 1.000 | 0.939 | 0.977 | 1.000 | 0.711 |
| NovaMind | 0.917 | 1.000 | 0.866 | 0.878 | 0.817 | 0.830 |

### Score Changes
- **OpenAI**: 0.995 -> 1.000 (+0.005)
- **Anthropic**: 0.987 -> 0.969 (-0.018)
- **NovaMind**: 0.862 -> 0.870 (+0.008)
- **DeepMind**: 0.973 -> 0.926 (-0.047)
- **Meta_AI**: 0.992 -> 0.930 (-0.062)

### Events
- **Anthropic** moved up from #3 to #2
- **Meta_AI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,965,924 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI takes #1 on factual_recall

### Consumer Market
- Avg Satisfaction: 0.888
- Switching Rate: 0.1%
- Market Shares: OpenAI: 99.3%, Anthropic: 0.3%, DeepMind: 0.2%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 1.000 | +0.169 | 25% | 25% |
| 2 | Anthropic | 0.969 | +0.146 | 28% | 22% |
| 3 | Meta_AI | 0.930 | +0.135 | 23% | 31% |
| 4 | DeepMind | 0.926 | +0.123 | 23% | 31% |
| 5 | NovaMind | 0.870 | +0.129 | 19% | 35% |

### Event Summary
- **Rank changes:** 47
- **Strategy shifts:** 2
- **Regulatory actions:** 2
- **Consumer movement events:** 7

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
- **NovaMind** prioritized evaluation engineering (avg 35%)
