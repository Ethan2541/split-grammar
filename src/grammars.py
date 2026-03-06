from .parsers import Parser

from anytree import Node

import numpy as np


class SplitGrammar(object):
    def __init__(self, dir, seed=0, filename="rules.txt"):
        # RNG used to precompute p_r -> should be reset for each building (Wonka et al., 2003)
        self.seed = seed
        self.reset_rng()
        
        self.parser = Parser(dir, filename)
        
        self.terminals = self.parser.parse_terminals()
        self.init_rules()


    def reset_rng(self):
        self.rng = np.random.default_rng(seed=self.seed)


    def init_rules(self):
        # Precompute a random number for each rule to ensure coherence during 
        # rule selection and score matching
        # TODO: determine appropriate lower and upper bounds for p_r
        rules = self.parser.parse_rules()
        self.rules = [(rule, self.rng.random()) for rule in rules]


    def match_rule(self, symbol):
        actionable_rules = self.get_actionable_rules(symbol)
        chosen_rule = self.stochastic_selection(actionable_rules)
        return chosen_rule
        
    
    def get_actionable_rules(self, symbol):
        return [(rule, p_r) for rule, p_r in self.rules if rule.premise == symbol]
    
    
    def stochastic_selection(self, rules):
        # For now, there is no attribute, so the selection is based on p_r only
        if len(rules) == 0:
            return None
        # return sorted(rules, key=lambda x: x[1], reverse=False)[0]
        random_idx = self.rng.choice(len(rules))
        return rules[random_idx][0]


    def derivate(self, initial_shape):
        # TODO: until no rules can be applied instead of max iterations
        
        root = Node(name=initial_shape.label, shape=initial_shape, children=[])
        remaining_nodes = [root]

        for i in range(10):
            current_node = remaining_nodes.pop(0)
            
            current_shape = current_node.shape
            if current_shape.label in self.terminals:
                continue

            rule = self.match_rule(current_shape.label)

            if rule:
                children = current_shape.split(rule.pos, rule.axis, rule.symbs)
                children_nodes = [Node(name=child.label, shape=child, parent=current_node, children=[]) 
                                  for child in children]
                
                current_node.name = f"{i+1} - {rule.label}"
                current_node.children = children_nodes

                remaining_nodes.extend(children_nodes)

        return root