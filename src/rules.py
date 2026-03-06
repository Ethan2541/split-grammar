from abc import ABC
from typing import List, Optional, Tuple


class Rule(ABC):
    def __init__(self, label: Optional[str] = None, rule_type: Optional[str] = None) -> None:
        self.label = label
        self.rule_type = rule_type

    def __str__(self) -> str:
        return self.label

        
class SplitRule(Rule):
    def __init__(self, 
                 premise: str, 
                 r1: Tuple[float, float], 
                 r2: Tuple[float, float],  
                 symbs: List[str]
                 ) -> None:
        
        self.premise = premise
        self.r1 = r1
        self.r2 = r2
        self.symbs = symbs

        self.label = f"split {r1} {r2} {' '.join(symbs)})"