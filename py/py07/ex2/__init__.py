from .battleStrategy import BattleStrategy as strategy
from .normalStrategy import NormalStrategy as normal
from .aggressiveStrategy import AggressiveStrategy as aggressive
from .defensiveStrategy import DefensiveStrategy as defensive


__all__ = [
    "strategy",
    "normal",
    "aggressive",
    "defensive"
]
