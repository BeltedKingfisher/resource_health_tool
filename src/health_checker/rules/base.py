from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

@dataclass
class RuleResult:    
    reason: str
    severity: float
    applicable: bool = True

class Rule(ABC):
    name: str
    weight: float    

    @abstractmethod
    def evaluate(self, entry) -> RuleResult:
        ...
