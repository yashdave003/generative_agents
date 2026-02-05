"""
Actors for Evaluation Ecosystem Simulation

This module exports all actor types:
- ModelProvider: AI model provider competing on benchmarks
- Evaluator: Benchmark organization that scores models
- Consumer: End user who subscribes to models
- Policymaker: Regulator who can issue requirements
- Funder: Capital allocator who influences provider development

Each actor has:
- PublicState: Visible to all actors
- PrivateState: Visible only to self (and logger)
- GroundTruth: Held externally by simulation (invisible to actors)
"""

from .model_provider import ModelProvider, ModelProviderScratch
from .evaluator import Evaluator, Benchmark, Regulation
from .consumer import Consumer
from .policymaker import Policymaker
from .funder import Funder, get_default_funder_configs, get_multi_funder_configs

__all__ = [
    # Core actors
    "ModelProvider",
    "ModelProviderScratch",
    "Evaluator",
    "Benchmark",
    "Regulation",
    # New actors
    "Consumer",
    "Policymaker",
    "Funder",
    # Funder configs
    "get_default_funder_configs",
    "get_multi_funder_configs",
]
