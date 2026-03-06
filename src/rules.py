from typing import List, Optional


class Rule(object):
    def __init__(
        self, 
        premise: str, 
        pos: float, 
        axis: str, 
        symbs: List[str],
        label: Optional[str] = None
    ) -> None:
        
        self.premise = premise
        self.pos = pos
        self.axis = axis
        self.symbs = symbs

        self.label = label


    def __str__(self):
        return self.label

        
class SplitRule(Rule):
    def __init__(
        self, 
        premise: str, 
        pos: float, 
        axis: str, 
        symbs: List[str]
    ) -> None:
        
        super().__init__(premise, pos, axis, symbs)
        self.label = f"split$_{{{self.axis}, {self.pos}}}$({', '.join(symbs)})"