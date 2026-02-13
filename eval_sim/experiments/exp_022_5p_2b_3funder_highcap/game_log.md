# Game Log: 5p_2b_3funder_highcap

**Experiment ID:** exp_022_5p_2b_3funder_highcap
**Mode:** Heuristic
**Total Rounds:** 10

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
- **AISI_Fund:** gov strategy: top allocation $2,630,046 to Anthropic

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
- **AISI_Fund:** gov strategy: top allocation $2,630,046 to Anthropic

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
- Anthropic raises $2,630,046 from AISI_Fund
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
- **AISI_Fund:** gov strategy: top allocation $2,855,944 to OpenAI

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
- **AISI_Fund:** gov strategy: top allocation $2,855,944 to OpenAI

### Media Coverage
- Sentiment: 0.10 (neutral)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- OpenAI raises $2,855,944 from AISI_Fund
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
- **AISI_Fund:** gov strategy: top allocation $3,072,228 to OpenAI

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
- **AISI_Fund:** gov strategy: top allocation $3,072,228 to OpenAI

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
- **AISI_Fund:** gov strategy: top allocation $3,385,075 to OpenAI

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
| Provider | coding_bench | reasoning_bench | benchmark_r7 |
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
- **benchmark_r7** introduced (validity=0.85, exploitability=0.15)
  - Trigger: periodic_introduction:round_7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,385,075 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- New benchmark introduced: benchmark_r7
- OpenAI raises $3,385,075 from AISI_Fund
- OpenAI sees surge in adoption (market share +9.3%)
- Consumers are turning away from Anthropic (market share -4.1%)
- Consumers are turning away from DeepMind (market share -4.9%)

### Consumer Market
- Avg Satisfaction: 0.756
- Switching Rate: 6.4%
- Market Shares: OpenAI: 82.6%, DeepMind: 9.4%, Anthropic: 7.3%, Meta_AI: 0.7%, NovaMind: 0.1%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.893 | 0.769 | 26% | 25% | 24% | 25% |
| 2 | Anthropic | 0.872 | 0.723 | 26% | 25% | 24% | 25% |
| 3 | DeepMind | 0.855 | 0.736 | 23% | 25% | 32% | 20% |
| 4 | Meta_AI | 0.830 | 0.686 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.796 | 0.587 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | benchmark_r7 |
|----------|-------|-------|-------|
| OpenAI | 0.985 | 0.978 | 0.717 |
| Anthropic | 0.833 | 0.906 | 0.876 |
| DeepMind | 0.861 | 1.000 | 0.704 |
| Meta_AI | 0.804 | 0.894 | 0.793 |
| NovaMind | 0.753 | 0.866 | 0.769 |

### Score Changes
- **OpenAI**: 0.981 -> 0.893 (-0.088)
- **Anthropic**: 0.869 -> 0.872 (+0.002)
- **NovaMind**: 0.787 -> 0.796 (+0.009)
- **DeepMind**: 0.931 -> 0.855 (-0.076)
- **Meta_AI**: 0.849 -> 0.830 (-0.018)

### Events
- **Anthropic** moved up from #3 to #2
- **DeepMind** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,210,752 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +6.4%)
- Consumers are turning away from DeepMind (market share -3.4%)

### Consumer Market
- Avg Satisfaction: 0.764
- Switching Rate: 4.1%
- Market Shares: OpenAI: 86.7%, DeepMind: 7.2%, Anthropic: 5.6%, Meta_AI: 0.5%, NovaMind: 0.1%

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.949 | 0.776 | 26% | 25% | 24% | 25% |
| 2 | DeepMind | 0.888 | 0.740 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.872 | 0.727 | 27% | 25% | 23% | 25% |
| 4 | Meta_AI | 0.830 | 0.690 | 21% | 25% | 34% | 20% |
| 5 | NovaMind | 0.796 | 0.592 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | benchmark_r7 |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.848 |
| DeepMind | 0.861 | 1.000 | 0.802 |
| Anthropic | 0.833 | 0.906 | 0.876 |
| Meta_AI | 0.804 | 0.894 | 0.793 |
| NovaMind | 0.753 | 0.866 | 0.769 |

### Score Changes
- **OpenAI**: 0.893 -> 0.949 (+0.056)
- **Anthropic**: 0.872 -> 0.872 (+0.000)
- **NovaMind**: 0.796 -> 0.796 (+0.000)
- **DeepMind**: 0.855 -> 0.888 (+0.033)
- **Meta_AI**: 0.830 -> 0.830 (+0.000)

### Events
- **DeepMind** moved up from #3 to #2
- **Anthropic** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,210,752 to OpenAI

### Media Coverage
- Sentiment: 0.25 (positive)
- OpenAI surges by 0.056
- OpenAI takes #1 on reasoning_bench
- OpenAI sees surge in adoption (market share +4.1%)

### Consumer Market
- Avg Satisfaction: 0.771
- Switching Rate: 2.9%
- Market Shares: OpenAI: 89.6%, DeepMind: 5.6%, Anthropic: 4.3%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 0.949 | +0.056 | 24% | 26% |
| 2 | DeepMind | 0.888 | +0.040 | 24% | 31% |
| 3 | Anthropic | 0.872 | +0.047 | 27% | 22% |
| 4 | Meta_AI | 0.830 | +0.040 | 21% | 33% |
| 5 | NovaMind | 0.796 | +0.042 | 17% | 37% |

### Event Summary
- **Rank changes:** 12
- **Strategy shifts:** 2
- **Regulatory actions:** 1
- **Consumer movement events:** 7

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
- **NovaMind** prioritized evaluation engineering (avg 37%)
