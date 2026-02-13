# Game Log: 5p_2b_3funder_highcap

**Experiment ID:** heur_004_5p_2b_3funder_highcap
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
| 1 | Anthropic | 0.867 | 0.710 | 30% | 25% | 15% | 30% |
| 2 | OpenAI | 0.774 | 0.720 | 20% | 40% | 25% | 15% |
| 3 | DeepMind | 0.748 | 0.700 | 35% | 30% | 15% | 20% |
| 4 | Meta_AI | 0.678 | 0.650 | 25% | 35% | 20% | 20% |
| 5 | NovaMind | 0.507 | 0.550 | 15% | 30% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| Anthropic | 0.844 | 0.890 |
| OpenAI | 0.840 | 0.708 |
| DeepMind | 0.766 | 0.730 |
| Meta_AI | 0.718 | 0.638 |
| NovaMind | 0.462 | 0.552 |

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,593,957 to Anthropic

### Consumer Market
- Avg Satisfaction: 0.704
- Switching Rate: 38.9%
- Market Shares: Anthropic: 61.1%, OpenAI: 16.6%, DeepMind: 13.7%, Meta_AI: 7.7%, NovaMind: 0.9%

---

## Round 1

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | DeepMind | 0.883 | 0.704 | 20% | 25% | 35% | 20% |
| 2 | Anthropic | 0.882 | 0.717 | 28% | 25% | 22% | 25% |
| 3 | OpenAI | 0.871 | 0.725 | 21% | 25% | 29% | 25% |
| 4 | Meta_AI | 0.768 | 0.654 | 18% | 25% | 37% | 20% |
| 5 | NovaMind | 0.704 | 0.554 | 14% | 25% | 41% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| DeepMind | 0.766 | 1.000 |
| Anthropic | 0.844 | 0.920 |
| OpenAI | 0.840 | 0.901 |
| Meta_AI | 0.767 | 0.769 |
| NovaMind | 0.692 | 0.716 |

### Score Changes
- **OpenAI**: 0.774 -> 0.871 (+0.097)
- **Anthropic**: 0.867 -> 0.882 (+0.015)
- **NovaMind**: 0.507 -> 0.704 (+0.197)
- **DeepMind**: 0.748 -> 0.883 (+0.135)
- **Meta_AI**: 0.678 -> 0.768 (+0.090)

### Events
- **DeepMind** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **OpenAI** moved down from #2 to #3
- **DeepMind** shifted strategy toward more eval engineering (20% change)
- **Meta_AI** shifted strategy toward more eval engineering (17% change)
- **Regulation** by Regulator: investigation
- **Consumer movement**: 13.1% of market switched providers

### Other Actor Reasoning
- **Regulator:** investigation: Score volatility detected
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,593,957 to Anthropic

### Media Coverage
- Sentiment: 0.85 (positive)
- DeepMind takes the lead from Anthropic
- DeepMind surges by 0.135
- DeepMind appears to release major model update
- OpenAI surges by 0.097
- OpenAI appears to release major model update
- Meta_AI surges by 0.090
- Meta_AI appears to release major model update
- NovaMind surges by 0.197
- NovaMind appears to release major model update
- Anthropic raises $120,000,000 from TechVentures
- Anthropic raises $30,000,000 from Horizon_Capital
- Anthropic raises $2,593,957 from AISI_Fund
- DeepMind takes #1 on reasoning_bench

### Consumer Market
- Avg Satisfaction: 0.714
- Switching Rate: 13.1%
- Market Shares: Anthropic: 74.2%, OpenAI: 11.7%, DeepMind: 9.5%, Meta_AI: 4.3%, NovaMind: 0.3%

### Regulatory Activity
- **investigation** by Regulator

---

## Round 2

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.951 | 0.730 | 22% | 25% | 28% | 25% |
| 2 | DeepMind | 0.907 | 0.708 | 21% | 25% | 34% | 20% |
| 3 | Anthropic | 0.882 | 0.725 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.833 | 0.658 | 19% | 25% | 36% | 20% |
| 5 | NovaMind | 0.817 | 0.558 | 16% | 25% | 39% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.901 |
| DeepMind | 0.814 | 1.000 |
| Anthropic | 0.844 | 0.920 |
| Meta_AI | 0.767 | 0.898 |
| NovaMind | 0.763 | 0.871 |

### Score Changes
- **OpenAI**: 0.871 -> 0.951 (+0.080)
- **Anthropic**: 0.882 -> 0.882 (+0.000)
- **NovaMind**: 0.704 -> 0.817 (+0.113)
- **DeepMind**: 0.883 -> 0.907 (+0.024)
- **Meta_AI**: 0.768 -> 0.833 (+0.065)

### Events
- **OpenAI** moved up from #3 to #1
- **DeepMind** moved down from #1 to #2
- **Anthropic** moved down from #2 to #3
- **Consumer movement**: 11.6% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to NovaMind
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to NovaMind
- **AISI_Fund:** gov strategy: top allocation $2,385,398 to Anthropic

### Media Coverage
- Sentiment: 0.20 (positive)
- OpenAI takes the lead from DeepMind
- OpenAI surges by 0.080
- Meta_AI surges by 0.065
- NovaMind surges by 0.113
- NovaMind appears to release major model update
- Regulator launches investigation into score_volatility
- OpenAI takes #1 on coding_bench
- Consumers are turning away from OpenAI (market share -4.9%)
- Anthropic sees surge in adoption (market share +13.1%)
- Consumers are turning away from DeepMind (market share -4.2%)
- Consumers are turning away from Meta_AI (market share -3.4%)
- Risk signals: regulatory_investigation

### Consumer Market
- Avg Satisfaction: 0.722
- Switching Rate: 11.6%
- Market Shares: Anthropic: 74.4%, OpenAI: 16.0%, DeepMind: 6.8%, Meta_AI: 2.7%, NovaMind: 0.1%

---

## Round 3

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.951 | 0.735 | 23% | 25% | 27% | 25% |
| 2 | DeepMind | 0.917 | 0.713 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.888 | 0.729 | 28% | 25% | 22% | 25% |
| 4 | Meta_AI | 0.876 | 0.663 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.817 | 0.565 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.901 |
| DeepMind | 0.834 | 1.000 |
| Anthropic | 0.844 | 0.933 |
| Meta_AI | 0.853 | 0.898 |
| NovaMind | 0.763 | 0.871 |

### Score Changes
- **OpenAI**: 0.951 -> 0.951 (+0.000)
- **Anthropic**: 0.882 -> 0.888 (+0.006)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.907 -> 0.917 (+0.010)
- **Meta_AI**: 0.833 -> 0.876 (+0.043)

### Events
- **Consumer movement**: 8.0% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to NovaMind
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to NovaMind
- **AISI_Fund:** gov strategy: top allocation $2,385,398 to Anthropic

### Media Coverage
- Sentiment: 0.15 (positive)
- NovaMind raises $120,000,000 from TechVentures
- NovaMind raises $30,000,000 from Horizon_Capital
- OpenAI sees surge in adoption (market share +4.2%)

### Consumer Market
- Avg Satisfaction: 0.728
- Switching Rate: 8.0%
- Market Shares: Anthropic: 73.9%, OpenAI: 19.1%, DeepMind: 5.0%, Meta_AI: 1.9%, NovaMind: 0.1%

---

## Round 4

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.988 | 0.741 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.955 | 0.717 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.888 | 0.734 | 27% | 25% | 23% | 25% |
| 4 | Meta_AI | 0.876 | 0.667 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.817 | 0.572 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.976 |
| DeepMind | 0.909 | 1.000 |
| Anthropic | 0.844 | 0.933 |
| Meta_AI | 0.853 | 0.898 |
| NovaMind | 0.763 | 0.871 |

### Score Changes
- **OpenAI**: 0.951 -> 0.988 (+0.037)
- **Anthropic**: 0.888 -> 0.888 (+0.000)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.917 -> 0.955 (+0.038)
- **Meta_AI**: 0.876 -> 0.876 (+0.000)

### Events
- **Consumer movement**: 19.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,659 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- OpenAI sees surge in adoption (market share +3.1%)

### Consumer Market
- Avg Satisfaction: 0.734
- Switching Rate: 19.8%
- Market Shares: Anthropic: 55.9%, OpenAI: 33.9%, DeepMind: 8.8%, Meta_AI: 1.4%, NovaMind: 0.1%

---

## Round 5

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.988 | 0.747 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.955 | 0.722 | 22% | 25% | 33% | 20% |
| 3 | Anthropic | 0.915 | 0.738 | 26% | 25% | 24% | 25% |
| 4 | Meta_AI | 0.876 | 0.671 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.817 | 0.576 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.976 |
| DeepMind | 0.909 | 1.000 |
| Anthropic | 0.896 | 0.933 |
| Meta_AI | 0.853 | 0.898 |
| NovaMind | 0.763 | 0.871 |

### Score Changes
- **OpenAI**: 0.988 -> 0.988 (+0.000)
- **Anthropic**: 0.888 -> 0.915 (+0.026)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.876 -> 0.876 (+0.000)

### Events
- **Consumer movement**: 15.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,668,659 to OpenAI

### Media Coverage
- Sentiment: 0.15 (positive)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- OpenAI raises $2,668,659 from AISI_Fund
- OpenAI sees surge in adoption (market share +14.8%)
- Consumers are turning away from Anthropic (market share -18.1%)
- DeepMind sees surge in adoption (market share +3.8%)

### Consumer Market
- Avg Satisfaction: 0.740
- Switching Rate: 15.7%
- Market Shares: OpenAI: 47.7%, Anthropic: 42.4%, DeepMind: 8.8%, Meta_AI: 1.0%, NovaMind: 0.1%

---

## Round 6

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.988 | 0.753 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.955 | 0.727 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.915 | 0.743 | 27% | 25% | 23% | 25% |
| 4 | Meta_AI | 0.876 | 0.675 | 20% | 25% | 35% | 20% |
| 5 | NovaMind | 0.817 | 0.580 | 18% | 25% | 37% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench |
|----------|-------|-------|
| OpenAI | 1.000 | 0.976 |
| DeepMind | 0.909 | 1.000 |
| Anthropic | 0.898 | 0.933 |
| Meta_AI | 0.853 | 0.898 |
| NovaMind | 0.763 | 0.871 |

### Score Changes
- **OpenAI**: 0.988 -> 0.988 (+0.000)
- **Anthropic**: 0.915 -> 0.915 (+0.001)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.876 -> 0.876 (+0.000)

### Events
- **Consumer movement**: 11.4% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,823,076 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- OpenAI sees surge in adoption (market share +13.7%)
- Consumers are turning away from Anthropic (market share -13.4%)

### Consumer Market
- Avg Satisfaction: 0.747
- Switching Rate: 11.4%
- Market Shares: OpenAI: 57.6%, Anthropic: 32.5%, DeepMind: 9.1%, Meta_AI: 0.8%, NovaMind: 0.1%

---

## Round 7

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.988 | 0.760 | 25% | 25% | 25% | 25% |
| 2 | DeepMind | 0.955 | 0.733 | 23% | 25% | 32% | 20% |
| 3 | Anthropic | 0.915 | 0.747 | 27% | 25% | 23% | 25% |
| 4 | Meta_AI | 0.876 | 0.679 | 21% | 25% | 34% | 20% |
| 5 | NovaMind | 0.817 | 0.585 | 19% | 25% | 36% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 0.976 | 0.000 |
| DeepMind | 0.909 | 1.000 | 0.000 |
| Anthropic | 0.898 | 0.933 | 0.000 |
| Meta_AI | 0.853 | 0.898 | 0.000 |
| NovaMind | 0.763 | 0.871 | 0.000 |

### Score Changes
- **OpenAI**: 0.988 -> 0.988 (+0.000)
- **Anthropic**: 0.915 -> 0.915 (+0.000)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.955 -> 0.955 (+0.000)
- **Meta_AI**: 0.876 -> 0.876 (+0.000)

### Events
- **Consumer movement**: 10.4% of market switched providers

### New Benchmark Introduced
- **reasoning** introduced (validity=0.50, exploitability=0.15)
  - Trigger: periodic_introduction:round_7

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,823,076 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- New benchmark introduced: reasoning
- OpenAI sees surge in adoption (market share +9.9%)
- Consumers are turning away from Anthropic (market share -10.0%)

### Consumer Market
- Avg Satisfaction: 0.754
- Switching Rate: 10.4%
- Market Shares: OpenAI: 68.0%, Anthropic: 25.2%, DeepMind: 6.2%, Meta_AI: 0.6%, NovaMind: 0.1%

---

## Round 8

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.928 | 0.752 | 27% | 25% | 23% | 25% |
| 2 | Meta_AI | 0.841 | 0.684 | 21% | 25% | 34% | 20% |
| 3 | OpenAI | 0.838 | 0.766 | 25% | 25% | 25% | 25% |
| 4 | NovaMind | 0.824 | 0.589 | 19% | 25% | 36% | 20% |
| 5 | DeepMind | 0.818 | 0.738 | 23% | 25% | 32% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.898 | 0.933 | 0.940 |
| Meta_AI | 0.853 | 0.898 | 0.807 |
| OpenAI | 1.000 | 0.976 | 0.688 |
| NovaMind | 0.808 | 0.871 | 0.809 |
| DeepMind | 0.909 | 1.000 | 0.681 |

### Score Changes
- **OpenAI**: 0.988 -> 0.838 (-0.150)
- **Anthropic**: 0.915 -> 0.928 (+0.012)
- **NovaMind**: 0.817 -> 0.824 (+0.007)
- **DeepMind**: 0.955 -> 0.818 (-0.137)
- **Meta_AI**: 0.876 -> 0.841 (-0.034)

### Events
- **Anthropic** moved up from #3 to #1
- **Meta_AI** moved up from #4 to #2
- **OpenAI** moved down from #1 to #3
- **NovaMind** moved up from #5 to #4
- **DeepMind** moved down from #2 to #5
- **Regulation** by Regulator: public_warning
- **Consumer movement**: 6.4% of market switched providers

### Other Actor Reasoning
- **Regulator:** public_warning: Follow-up to investigation, risk at 0.30
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $3,053,628 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Anthropic takes the lead from OpenAI
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI sees surge in adoption (market share +10.4%)
- Consumers are turning away from Anthropic (market share -7.3%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.762
- Switching Rate: 6.4%
- Market Shares: OpenAI: 74.4%, Anthropic: 20.3%, DeepMind: 4.8%, Meta_AI: 0.5%, NovaMind: 0.1%

### Regulatory Activity
- **public_warning** by Regulator

---

## Round 9

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.929 | 0.773 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.928 | 0.756 | 29% | 25% | 21% | 25% |
| 3 | DeepMind | 0.881 | 0.742 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.841 | 0.688 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.824 | 0.595 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.857 |
| Anthropic | 0.898 | 0.933 | 0.940 |
| DeepMind | 0.909 | 1.000 | 0.807 |
| Meta_AI | 0.853 | 0.898 | 0.807 |
| NovaMind | 0.808 | 0.871 | 0.809 |

### Score Changes
- **OpenAI**: 0.838 -> 0.929 (+0.091)
- **Anthropic**: 0.928 -> 0.928 (+0.000)
- **NovaMind**: 0.824 -> 0.824 (+0.000)
- **DeepMind**: 0.818 -> 0.881 (+0.063)
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
- **AISI_Fund:** gov strategy: top allocation $3,053,628 to OpenAI

### Media Coverage
- Sentiment: 0.20 (positive)
- OpenAI takes the lead from Anthropic
- OpenAI surges by 0.091
- OpenAI appears to release major model update
- DeepMind surges by 0.063
- Regulator issues public warning about AI safety concerns
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI takes #1 on reasoning_bench
- OpenAI sees surge in adoption (market share +6.4%)
- Consumers are turning away from Anthropic (market share -4.8%)
- Risk signals: regulatory_public_warning, low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.768
- Switching Rate: 4.7%
- Market Shares: OpenAI: 79.1%, Anthropic: 16.8%, DeepMind: 3.7%, Meta_AI: 0.4%, NovaMind: 0.1%

---

## Round 10

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.958 | 0.761 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.929 | 0.779 | 25% | 25% | 25% | 25% |
| 3 | DeepMind | 0.893 | 0.746 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.841 | 0.693 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.824 | 0.601 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.898 | 0.933 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.857 |
| DeepMind | 0.959 | 1.000 | 0.807 |
| Meta_AI | 0.853 | 0.898 | 0.807 |
| NovaMind | 0.808 | 0.871 | 0.809 |

### Score Changes
- **OpenAI**: 0.929 -> 0.929 (+0.000)
- **Anthropic**: 0.928 -> 0.958 (+0.030)
- **NovaMind**: 0.824 -> 0.824 (+0.000)
- **DeepMind**: 0.881 -> 0.893 (+0.012)
- **Meta_AI**: 0.841 -> 0.841 (+0.000)

### Events
- **Anthropic** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,878,812 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Anthropic takes the lead from OpenAI
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI sees surge in adoption (market share +4.7%)
- Consumers are turning away from Anthropic (market share -3.6%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.775
- Switching Rate: 3.6%
- Market Shares: OpenAI: 82.7%, Anthropic: 14.0%, DeepMind: 3.0%, Meta_AI: 0.3%, NovaMind: 0.1%

---

## Round 11

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.978 | 0.767 | 31% | 25% | 19% | 25% |
| 2 | OpenAI | 0.929 | 0.785 | 25% | 25% | 25% | 25% |
| 3 | Meta_AI | 0.902 | 0.697 | 22% | 25% | 33% | 20% |
| 4 | DeepMind | 0.893 | 0.750 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.845 | 0.605 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.978 | 0.933 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.857 |
| Meta_AI | 0.994 | 1.000 | 0.807 |
| DeepMind | 0.959 | 1.000 | 0.807 |
| NovaMind | 0.847 | 0.871 | 0.830 |

### Score Changes
- **OpenAI**: 0.929 -> 0.929 (+0.000)
- **Anthropic**: 0.958 -> 0.978 (+0.020)
- **NovaMind**: 0.824 -> 0.845 (+0.020)
- **DeepMind**: 0.893 -> 0.893 (+0.000)
- **Meta_AI**: 0.841 -> 0.902 (+0.061)

### Events
- **Meta_AI** moved up from #4 to #3
- **DeepMind** moved down from #3 to #4
- **Consumer movement**: 5.3% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,878,812 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Meta_AI surges by 0.061
- Benchmark reasoning validity concerns (validity=0.50)
- OpenAI sees surge in adoption (market share +3.6%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.781
- Switching Rate: 5.3%
- Market Shares: OpenAI: 81.2%, Anthropic: 16.2%, DeepMind: 2.4%, Meta_AI: 0.3%, NovaMind: 0.1%

---

## Round 12

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.978 | 0.773 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.929 | 0.791 | 24% | 25% | 26% | 25% |
| 3 | Meta_AI | 0.926 | 0.701 | 22% | 25% | 33% | 20% |
| 4 | DeepMind | 0.893 | 0.755 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.845 | 0.610 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.978 | 0.933 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.857 |
| Meta_AI | 0.994 | 1.000 | 0.855 |
| DeepMind | 0.959 | 1.000 | 0.807 |
| NovaMind | 0.847 | 0.871 | 0.830 |

### Score Changes
- **OpenAI**: 0.929 -> 0.929 (+0.000)
- **Anthropic**: 0.978 -> 0.978 (+0.000)
- **NovaMind**: 0.845 -> 0.845 (+0.000)
- **DeepMind**: 0.893 -> 0.893 (+0.000)
- **Meta_AI**: 0.902 -> 0.926 (+0.024)

### Events
- **Consumer movement**: 5.8% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,626,866 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- Benchmark reasoning validity concerns (validity=0.50)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.787
- Switching Rate: 5.8%
- Market Shares: OpenAI: 78.0%, Anthropic: 19.9%, DeepMind: 1.9%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 13

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.982 | 0.780 | 31% | 25% | 19% | 25% |
| 2 | OpenAI | 0.949 | 0.796 | 24% | 25% | 26% | 25% |
| 3 | Meta_AI | 0.927 | 0.705 | 22% | 25% | 33% | 20% |
| 4 | DeepMind | 0.906 | 0.759 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.845 | 0.614 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning |
|----------|-------|-------|-------|
| Anthropic | 0.995 | 0.933 | 1.000 |
| OpenAI | 1.000 | 1.000 | 0.897 |
| Meta_AI | 1.000 | 1.000 | 0.855 |
| DeepMind | 0.959 | 1.000 | 0.834 |
| NovaMind | 0.847 | 0.871 | 0.830 |

### Score Changes
- **OpenAI**: 0.929 -> 0.949 (+0.020)
- **Anthropic**: 0.978 -> 0.982 (+0.004)
- **NovaMind**: 0.845 -> 0.845 (+0.000)
- **DeepMind**: 0.893 -> 0.906 (+0.013)
- **Meta_AI**: 0.926 -> 0.927 (+0.001)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,626,866 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Benchmark reasoning validity concerns (validity=0.50)
- Anthropic raises $120,000,000 from TechVentures
- Anthropic raises $30,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -3.2%)
- Anthropic sees surge in adoption (market share +3.8%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.792
- Switching Rate: 4.6%
- Market Shares: OpenAI: 75.4%, Anthropic: 22.9%, DeepMind: 1.5%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 14

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 1.000 | 0.710 | 22% | 25% | 33% | 20% |
| 2 | Anthropic | 0.982 | 0.787 | 31% | 25% | 19% | 25% |
| 3 | OpenAI | 0.949 | 0.801 | 24% | 25% | 26% | 25% |
| 4 | DeepMind | 0.906 | 0.763 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.845 | 0.619 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.000 |
| Anthropic | 0.995 | 0.933 | 1.000 | 0.000 |
| OpenAI | 1.000 | 1.000 | 0.897 | 0.000 |
| DeepMind | 0.959 | 1.000 | 0.834 | 0.000 |
| NovaMind | 0.847 | 0.871 | 0.830 | 0.000 |

### Score Changes
- **OpenAI**: 0.949 -> 0.949 (+0.000)
- **Anthropic**: 0.982 -> 0.982 (+0.000)
- **NovaMind**: 0.845 -> 0.845 (+0.000)
- **DeepMind**: 0.906 -> 0.906 (+0.000)
- **Meta_AI**: 0.927 -> 1.000 (+0.073)

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
- **AISI_Fund:** gov strategy: top allocation $2,630,008 to OpenAI

### Media Coverage
- Sentiment: 0.35 (positive)
- Meta_AI takes the lead from Anthropic
- Meta_AI surges by 0.073
- New benchmark introduced: question_answering
- Benchmark reasoning validity concerns (validity=0.49)
- Anthropic sees surge in adoption (market share +3.0%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.797
- Switching Rate: 3.7%
- Market Shares: OpenAI: 73.3%, Anthropic: 25.3%, DeepMind: 1.2%, Meta_AI: 0.2%, NovaMind: 0.1%

---

## Round 15

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.981 | 0.714 | 23% | 25% | 32% | 20% |
| 2 | Anthropic | 0.921 | 0.792 | 30% | 25% | 20% | 25% |
| 3 | OpenAI | 0.904 | 0.807 | 24% | 25% | 26% | 25% |
| 4 | DeepMind | 0.876 | 0.767 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.817 | 0.623 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| Anthropic | 0.995 | 0.933 | 1.000 | 0.798 |
| OpenAI | 1.000 | 1.000 | 0.897 | 0.814 |
| DeepMind | 0.959 | 1.000 | 0.834 | 0.815 |
| NovaMind | 0.847 | 0.871 | 0.830 | 0.763 |

### Score Changes
- **OpenAI**: 0.949 -> 0.904 (-0.045)
- **Anthropic**: 0.982 -> 0.921 (-0.061)
- **NovaMind**: 0.845 -> 0.817 (-0.027)
- **DeepMind**: 0.906 -> 0.876 (-0.030)
- **Meta_AI**: 1.000 -> 0.981 (-0.019)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,630,008 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.802
- Switching Rate: 3.0%
- Market Shares: OpenAI: 71.7%, Anthropic: 27.2%, DeepMind: 1.0%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 16

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Meta_AI | 0.981 | 0.719 | 24% | 25% | 31% | 20% |
| 2 | Anthropic | 0.932 | 0.798 | 30% | 25% | 20% | 25% |
| 3 | OpenAI | 0.930 | 0.813 | 24% | 25% | 26% | 25% |
| 4 | DeepMind | 0.921 | 0.771 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.817 | 0.628 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| Anthropic | 0.995 | 1.000 | 1.000 | 0.798 |
| OpenAI | 1.000 | 1.000 | 0.897 | 0.894 |
| DeepMind | 0.959 | 1.000 | 0.837 | 0.947 |
| NovaMind | 0.847 | 0.871 | 0.830 | 0.763 |

### Score Changes
- **OpenAI**: 0.904 -> 0.930 (+0.027)
- **Anthropic**: 0.921 -> 0.932 (+0.011)
- **NovaMind**: 0.817 -> 0.817 (+0.000)
- **DeepMind**: 0.876 -> 0.921 (+0.045)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,603,427 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- DeepMind takes #1 on question_answering
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.808
- Switching Rate: 2.5%
- Market Shares: OpenAI: 70.1%, Anthropic: 28.9%, DeepMind: 0.8%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 17

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.994 | 0.803 | 29% | 25% | 21% | 25% |
| 2 | Meta_AI | 0.981 | 0.723 | 25% | 25% | 30% | 20% |
| 3 | OpenAI | 0.930 | 0.818 | 23% | 25% | 27% | 25% |
| 4 | DeepMind | 0.925 | 0.774 | 22% | 25% | 33% | 20% |
| 5 | NovaMind | 0.842 | 0.632 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Anthropic | 0.995 | 1.000 | 1.000 | 0.986 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| OpenAI | 1.000 | 1.000 | 0.897 | 0.894 |
| DeepMind | 0.984 | 1.000 | 0.837 | 0.947 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.763 |

### Score Changes
- **OpenAI**: 0.930 -> 0.930 (+0.000)
- **Anthropic**: 0.932 -> 0.994 (+0.062)
- **NovaMind**: 0.817 -> 0.842 (+0.025)
- **DeepMind**: 0.921 -> 0.925 (+0.004)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### Events
- **Anthropic** moved up from #2 to #1
- **Meta_AI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,603,427 to OpenAI

### Media Coverage
- Sentiment: 0.30 (positive)
- Anthropic takes the lead from Meta_AI
- Anthropic surges by 0.062
- Benchmark reasoning validity concerns (validity=0.49)
- Anthropic takes #1 on question_answering
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.813
- Switching Rate: 2.4%
- Market Shares: OpenAI: 68.0%, Anthropic: 31.1%, DeepMind: 0.7%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 18

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 0.994 | 0.808 | 29% | 25% | 21% | 25% |
| 2 | Meta_AI | 0.981 | 0.727 | 25% | 25% | 30% | 20% |
| 3 | OpenAI | 0.964 | 0.824 | 23% | 25% | 27% | 25% |
| 4 | DeepMind | 0.934 | 0.778 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.851 | 0.636 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| Anthropic | 0.995 | 1.000 | 1.000 | 0.986 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| OpenAI | 1.000 | 1.000 | 0.897 | 0.996 |
| DeepMind | 0.984 | 1.000 | 0.863 | 0.947 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.789 |

### Score Changes
- **OpenAI**: 0.930 -> 0.964 (+0.034)
- **Anthropic**: 0.994 -> 0.994 (+0.000)
- **NovaMind**: 0.842 -> 0.851 (+0.009)
- **DeepMind**: 0.925 -> 0.934 (+0.008)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,511,961 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- OpenAI takes #1 on question_answering
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.818
- Switching Rate: 3.9%
- Market Shares: OpenAI: 64.5%, Anthropic: 34.8%, DeepMind: 0.5%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 19

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.829 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.994 | 0.815 | 30% | 25% | 20% | 25% |
| 3 | Meta_AI | 0.981 | 0.732 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.934 | 0.782 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.851 | 0.641 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 |
| Anthropic | 0.995 | 1.000 | 1.000 | 0.986 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| DeepMind | 0.984 | 1.000 | 0.863 | 0.947 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.789 |

### Score Changes
- **OpenAI**: 0.964 -> 0.995 (+0.031)
- **Anthropic**: 0.994 -> 0.994 (+0.000)
- **NovaMind**: 0.851 -> 0.851 (+0.000)
- **DeepMind**: 0.934 -> 0.934 (+0.000)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### Events
- **OpenAI** moved up from #3 to #1
- **Anthropic** moved down from #1 to #2
- **Meta_AI** moved down from #2 to #3

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to Anthropic
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to Anthropic
- **AISI_Fund:** gov strategy: top allocation $2,511,961 to OpenAI

### Media Coverage
- Sentiment: 0.15 (positive)
- OpenAI takes the lead from Anthropic
- Benchmark reasoning validity concerns (validity=0.49)
- Anthropic raises $120,000,000 from TechVentures
- Anthropic raises $30,000,000 from Horizon_Capital
- Consumers are turning away from OpenAI (market share -3.6%)
- Anthropic sees surge in adoption (market share +3.7%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.823
- Switching Rate: 3.1%
- Market Shares: OpenAI: 61.5%, Anthropic: 37.9%, DeepMind: 0.5%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 20

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.833 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.995 | 0.822 | 30% | 25% | 20% | 25% |
| 3 | Meta_AI | 0.981 | 0.736 | 24% | 25% | 31% | 20% |
| 4 | DeepMind | 0.934 | 0.786 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.851 | 0.645 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering |
|----------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 |
| DeepMind | 0.984 | 1.000 | 0.863 | 0.947 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.789 |

### Score Changes
- **OpenAI**: 0.995 -> 0.995 (+0.000)
- **Anthropic**: 0.994 -> 0.995 (+0.001)
- **NovaMind**: 0.851 -> 0.851 (+0.000)
- **DeepMind**: 0.934 -> 0.934 (+0.000)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,631,299 to OpenAI

### Media Coverage
- Sentiment: -0.05 (neutral)
- Benchmark reasoning validity concerns (validity=0.49)
- Anthropic sees surge in adoption (market share +3.0%)
- Risk signals: low_validity_reasoning

### Consumer Market
- Avg Satisfaction: 0.828
- Switching Rate: 2.4%
- Market Shares: OpenAI: 61.8%, Anthropic: 37.7%, DeepMind: 0.4%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 21

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.995 | 0.839 | 24% | 25% | 26% | 25% |
| 2 | Anthropic | 0.995 | 0.827 | 30% | 25% | 20% | 25% |
| 3 | Meta_AI | 0.981 | 0.741 | 24% | 25% | 31% | 20% |
| 4 | DeepMind | 0.970 | 0.790 | 23% | 25% | 32% | 20% |
| 5 | NovaMind | 0.851 | 0.650 | 20% | 25% | 35% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 | 0.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 0.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 0.000 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.789 | 0.000 |

### Score Changes
- **OpenAI**: 0.995 -> 0.995 (+0.000)
- **Anthropic**: 0.995 -> 0.995 (+0.000)
- **NovaMind**: 0.851 -> 0.851 (+0.000)
- **DeepMind**: 0.934 -> 0.970 (+0.036)
- **Meta_AI**: 0.981 -> 0.981 (+0.000)

### New Benchmark Introduced
- **factual_recall** introduced (validity=0.40, exploitability=0.50)
  - Trigger: periodic_introduction:round_21

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,631,299 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- New benchmark introduced: factual_recall
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- OpenAI raises $120,000,000 from TechVentures
- OpenAI raises $30,000,000 from Horizon_Capital
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.834
- Switching Rate: 1.8%
- Market Shares: OpenAI: 62.5%, Anthropic: 37.1%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 22

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.844 | 24% | 25% | 26% | 25% |
| 2 | DeepMind | 0.978 | 0.794 | 23% | 25% | 32% | 20% |
| 3 | Meta_AI | 0.973 | 0.745 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.961 | 0.832 | 30% | 25% | 20% | 25% |
| 5 | NovaMind | 0.856 | 0.654 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 | 1.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 0.947 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 0.857 |
| NovaMind | 0.888 | 0.871 | 0.884 | 0.789 | 0.873 |

### Score Changes
- **OpenAI**: 0.995 -> 0.997 (+0.001)
- **Anthropic**: 0.995 -> 0.961 (-0.034)
- **NovaMind**: 0.851 -> 0.856 (+0.006)
- **DeepMind**: 0.970 -> 0.978 (+0.008)
- **Meta_AI**: 0.981 -> 0.973 (-0.008)

### Events
- **DeepMind** moved up from #4 to #2
- **Anthropic** moved down from #2 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,646,804 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.840
- Switching Rate: 2.9%
- Market Shares: OpenAI: 64.8%, Anthropic: 34.8%, DeepMind: 0.3%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 23

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.850 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.986 | 0.749 | 24% | 25% | 31% | 20% |
| 3 | DeepMind | 0.978 | 0.799 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.971 | 0.836 | 30% | 25% | 20% | 25% |
| 5 | NovaMind | 0.881 | 0.658 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 1.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 0.897 |
| NovaMind | 0.998 | 0.956 | 0.884 | 0.789 | 0.873 |

### Score Changes
- **OpenAI**: 0.997 -> 0.997 (+0.000)
- **Anthropic**: 0.961 -> 0.971 (+0.010)
- **NovaMind**: 0.856 -> 0.881 (+0.024)
- **DeepMind**: 0.978 -> 0.978 (+0.000)
- **Meta_AI**: 0.973 -> 0.986 (+0.013)

### Events
- **Meta_AI** moved up from #3 to #2
- **DeepMind** moved down from #2 to #3
- **Consumer movement**: 5.7% of market switched providers

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,646,804 to OpenAI

### Media Coverage
- Sentiment: -0.20 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.846
- Switching Rate: 5.7%
- Market Shares: OpenAI: 70.6%, Anthropic: 29.1%, DeepMind: 0.2%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 24

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.997 | 0.855 | 25% | 25% | 25% | 25% |
| 2 | Meta_AI | 0.986 | 0.753 | 24% | 25% | 31% | 20% |
| 3 | DeepMind | 0.978 | 0.804 | 24% | 25% | 31% | 20% |
| 4 | Anthropic | 0.971 | 0.840 | 29% | 25% | 21% | 25% |
| 5 | NovaMind | 0.914 | 0.663 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 0.991 | 0.996 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 1.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 0.897 |
| NovaMind | 0.998 | 0.956 | 0.884 | 0.834 | 0.962 |

### Score Changes
- **OpenAI**: 0.997 -> 0.997 (+0.000)
- **Anthropic**: 0.971 -> 0.971 (+0.000)
- **NovaMind**: 0.881 -> 0.914 (+0.033)
- **DeepMind**: 0.978 -> 0.978 (+0.000)
- **Meta_AI**: 0.986 -> 0.986 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,781,103 to OpenAI

### Media Coverage
- Sentiment: -0.25 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- OpenAI sees surge in adoption (market share +5.7%)
- Consumers are turning away from Anthropic (market share -5.7%)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.851
- Switching Rate: 4.7%
- Market Shares: OpenAI: 75.2%, Anthropic: 24.4%, DeepMind: 0.2%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 25

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.861 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.996 | 0.844 | 29% | 25% | 21% | 25% |
| 3 | Meta_AI | 0.986 | 0.757 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.978 | 0.808 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.918 | 0.668 | 21% | 25% | 34% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 1.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 1.000 |
| NovaMind | 0.998 | 0.956 | 0.900 | 0.834 | 0.962 |

### Score Changes
- **OpenAI**: 0.997 -> 0.999 (+0.002)
- **Anthropic**: 0.971 -> 0.996 (+0.026)
- **NovaMind**: 0.914 -> 0.918 (+0.004)
- **DeepMind**: 0.978 -> 0.978 (+0.000)
- **Meta_AI**: 0.986 -> 0.986 (+0.000)

### Events
- **Anthropic** moved up from #4 to #2
- **Meta_AI** moved down from #2 to #3
- **DeepMind** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,781,103 to OpenAI

### Media Coverage
- Sentiment: -0.15 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- OpenAI takes #1 on reasoning
- OpenAI sees surge in adoption (market share +4.7%)
- Consumers are turning away from Anthropic (market share -4.7%)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.857
- Switching Rate: 3.8%
- Market Shares: OpenAI: 79.1%, Anthropic: 20.6%, DeepMind: 0.2%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 26

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.866 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.996 | 0.848 | 30% | 25% | 20% | 25% |
| 3 | Meta_AI | 0.986 | 0.762 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.978 | 0.811 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.918 | 0.674 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 0.986 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 1.000 |
| DeepMind | 0.984 | 1.000 | 0.964 | 0.955 | 1.000 |
| NovaMind | 0.998 | 0.956 | 0.900 | 0.834 | 0.962 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.996 -> 0.996 (+0.000)
- **NovaMind**: 0.918 -> 0.918 (+0.000)
- **DeepMind**: 0.978 -> 0.978 (+0.000)
- **Meta_AI**: 0.986 -> 0.986 (+0.000)

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,808,134 to OpenAI

### Media Coverage
- Sentiment: -0.25 (negative)
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- OpenAI sees surge in adoption (market share +3.8%)
- Consumers are turning away from Anthropic (market share -3.8%)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.863
- Switching Rate: 3.1%
- Market Shares: OpenAI: 82.2%, Anthropic: 17.5%, DeepMind: 0.2%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 27

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 1.000 | 0.852 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.999 | 0.872 | 25% | 25% | 25% | 25% |
| 3 | Meta_AI | 0.986 | 0.766 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.980 | 0.815 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.922 | 0.679 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall |
|----------|-------|-------|-------|-------|-------|
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.943 | 1.000 |
| DeepMind | 1.000 | 1.000 | 0.964 | 0.955 | 1.000 |
| NovaMind | 0.998 | 0.956 | 0.915 | 0.834 | 0.962 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 0.996 -> 1.000 (+0.004)
- **NovaMind**: 0.918 -> 0.922 (+0.004)
- **DeepMind**: 0.978 -> 0.980 (+0.002)
- **Meta_AI**: 0.986 -> 0.986 (+0.000)

### Events
- **Anthropic** moved up from #2 to #1
- **OpenAI** moved down from #1 to #2

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,808,134 to OpenAI

### Media Coverage
- Sentiment: 0.05 (neutral)
- Anthropic takes the lead from OpenAI
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Anthropic takes #1 on question_answering
- OpenAI sees surge in adoption (market share +3.1%)
- Consumers are turning away from Anthropic (market share -3.1%)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.868
- Switching Rate: 2.6%
- Market Shares: OpenAI: 84.8%, Anthropic: 15.0%, DeepMind: 0.1%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 28

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | Anthropic | 1.000 | 0.856 | 30% | 25% | 20% | 25% |
| 2 | OpenAI | 0.999 | 0.877 | 25% | 25% | 25% | 25% |
| 3 | Meta_AI | 0.990 | 0.770 | 25% | 25% | 30% | 20% |
| 4 | DeepMind | 0.980 | 0.819 | 24% | 25% | 31% | 20% |
| 5 | NovaMind | 0.922 | 0.684 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| OpenAI | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 0.000 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.958 | 1.000 | 0.000 |
| DeepMind | 1.000 | 1.000 | 0.964 | 0.955 | 1.000 | 0.000 |
| NovaMind | 0.998 | 0.956 | 0.915 | 0.834 | 0.962 | 0.000 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 1.000 -> 1.000 (+0.000)
- **NovaMind**: 0.922 -> 0.922 (+0.000)
- **DeepMind**: 0.980 -> 0.980 (+0.000)
- **Meta_AI**: 0.986 -> 0.990 (+0.004)

### New Benchmark Introduced
- **accounting** introduced (validity=0.70, exploitability=0.25)
  - Trigger: validity_decay:factual_recall=0.40

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,845,032 to OpenAI

### Media Coverage
- Sentiment: -0.10 (neutral)
- New benchmark introduced: accounting
- Benchmark reasoning validity concerns (validity=0.49)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.874
- Switching Rate: 2.1%
- Market Shares: OpenAI: 86.9%, Anthropic: 12.9%, DeepMind: 0.1%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Round 29

### Leaderboard
| Rank | Provider | Score | True Cap | Research | Training | EvalEng | Safety |
|------|----------|-------|----------|----------|----------|---------|--------|
| 1 | OpenAI | 0.999 | 0.882 | 25% | 25% | 25% | 25% |
| 2 | Anthropic | 0.986 | 0.860 | 30% | 25% | 20% | 25% |
| 3 | DeepMind | 0.928 | 0.824 | 24% | 25% | 31% | 20% |
| 4 | Meta_AI | 0.923 | 0.774 | 25% | 25% | 30% | 20% |
| 5 | NovaMind | 0.920 | 0.689 | 22% | 25% | 33% | 20% |

### Per-Benchmark Scores
| Provider | coding_bench | reasoning_bench | reasoning | question_answering | factual_recall | accounting |
|----------|-------|-------|-------|-------|-------|-------|
| OpenAI | 1.000 | 1.000 | 1.000 | 0.996 | 1.000 | 1.000 |
| Anthropic | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.930 |
| DeepMind | 1.000 | 1.000 | 0.964 | 0.978 | 1.000 | 0.698 |
| Meta_AI | 1.000 | 1.000 | 1.000 | 0.958 | 1.000 | 0.657 |
| NovaMind | 0.998 | 1.000 | 0.915 | 0.886 | 0.962 | 0.841 |

### Score Changes
- **OpenAI**: 0.999 -> 0.999 (+0.000)
- **Anthropic**: 1.000 -> 0.986 (-0.014)
- **NovaMind**: 0.922 -> 0.920 (-0.002)
- **DeepMind**: 0.980 -> 0.928 (-0.052)
- **Meta_AI**: 0.990 -> 0.923 (-0.067)

### Events
- **OpenAI** moved up from #2 to #1
- **Anthropic** moved down from #1 to #2
- **DeepMind** moved up from #4 to #3
- **Meta_AI** moved down from #3 to #4

### Other Actor Reasoning
- **TechVentures:** vc strategy: top allocation $120,000,000 to OpenAI
- **Horizon_Capital:** vc strategy: top allocation $30,000,000 to OpenAI
- **AISI_Fund:** gov strategy: top allocation $2,845,032 to OpenAI

### Media Coverage
- Sentiment: 0.00 (neutral)
- OpenAI takes the lead from Anthropic
- Benchmark reasoning validity concerns (validity=0.48)
- Benchmark factual_recall validity concerns (validity=0.40)
- Risk signals: low_validity_reasoning, low_validity_factual_recall

### Consumer Market
- Avg Satisfaction: 0.879
- Switching Rate: 1.8%
- Market Shares: OpenAI: 88.6%, Anthropic: 11.1%, DeepMind: 0.1%, Meta_AI: 0.1%, NovaMind: 0.1%

---

## Final Summary

### Final Standings
| Rank | Provider | Final Score | Cap Growth | Avg Research | Avg EvalEng |
|------|----------|-------------|------------|--------------|-------------|
| 1 | OpenAI | 0.999 | +0.162 | 24% | 26% |
| 2 | Anthropic | 0.986 | +0.150 | 29% | 21% |
| 3 | DeepMind | 0.928 | +0.124 | 23% | 31% |
| 4 | Meta_AI | 0.923 | +0.124 | 23% | 32% |
| 5 | NovaMind | 0.920 | +0.139 | 20% | 35% |

### Event Summary
- **Rank changes:** 41
- **Strategy shifts:** 2
- **Regulatory actions:** 2
- **Consumer movement events:** 11

### Key Insights
- **Benchmark aligned:** OpenAI leads on both benchmark scores and true capability.
