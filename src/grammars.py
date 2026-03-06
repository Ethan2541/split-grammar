from .parsers import Parser
from .rules import Rule
from .shapes import Polygon2D

from anytree import Node
from typing import List, Optional, Tuple

import numpy as np


class SplitGrammar(object):
    def __init__(self, dir: str, seed: int = 0, filename: str = "rules.txt") -> None:
        # RNG used to precompute p_r -> should be reset for each building (Wonka et al., 2003)
        self.seed = seed
        self.reset_rng()
        
        self.parser = Parser(dir, filename)
        
        self.terminals = self.parser.parse_terminals()
        self.init_rules()


    def reset_rng(self) -> None:
        self.rng = np.random.default_rng(seed=self.seed)


    def init_rules(self) -> List[Tuple[Rule, float]]:
        # Precompute a random number for each rule to ensure coherence during 
        # rule selection and score matching
        # TODO: determine appropriate lower and upper bounds for p_r
        rules = self.parser.parse_rules()
        self.rules = [(rule, self.rng.random()) for rule in rules]


    def match_rule(self, symbol: str) -> Optional[Rule]:
        actionable_rules = self.get_actionable_rules(symbol)
        chosen_rule = self.stochastic_selection(actionable_rules)
        return chosen_rule
        
    
    def get_actionable_rules(self, symbol: str) -> List[Rule]:
        return [(rule, p_r) for rule, p_r in self.rules if rule.premise == symbol]
    
    
    def stochastic_selection(self, rules: Optional[Rule]) -> Rule:
        # TODO: for now, there is no attribute, so the selection is based on p_r only
        if len(rules) == 0:
            return None
        # return sorted(rules, key=lambda x: x[1], reverse=False)[0]
        random_idx = self.rng.choice(len(rules))
        return rules[random_idx][0]


    def derivate(self, initial_shape: Polygon2D) -> Node: 
        root = Node(name=initial_shape.label, shape=initial_shape, children=[])
        remaining_nodes = [root]

        n_iter = 0
        while len(remaining_nodes) > 0:
            current_node = remaining_nodes.pop(0)
            current_shape = current_node.shape
            n_iter += 1

            if current_shape.label in self.terminals:
                current_node.name = f"{n_iter} - {current_shape.label}"
                continue

            rule = self.match_rule(current_shape.label)

            if rule:
                children = current_shape.split(rule.r1, rule.r2, rule.symbs)
                if len(children) == 1:
                    continue
                
                children_nodes = [Node(name=child.label, shape=child, parent=current_node, children=[]) 
                                  for child in children]
                
                current_node.name = f"{n_iter} - {rule.label}"
                current_node.children = children_nodes

                # Nodes traversal (BFS in this case) should be deterministic (Wonka et al., 2003)
                remaining_nodes.extend(children_nodes)

        return root