from .rules import SplitRule

from typing import List, Set

import os


class Parser(object):
    def __init__(
        self, 
        dir: str, 
        filename: str
    ) -> None:
        
        self.dir = dir
        self.filename = filename
        self.path = os.path.join(self.dir, self.filename)

        self.IMPLY = "::-"
        self.AND = ","
        self.OR = "|"


    def check_rules_integrity(self):
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file]

        for line in stripped_lines:
            if self.IMPLY not in line:
                return False
            
            premise, _ = line.split(self.IMPLY) # Raise an error if several "::-" symbols

            # The premise should contain a single nonterminal symbol
            if premise.strip().islower() or len(premise.split()) > 1:
                return False
            
        return True
            

    def parse_terminals(self) -> Set[str]:
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file]

        terminals = set()
        for line in stripped_lines:
            _, conclusion = line.split(self.IMPLY)  # Terminals do not appear in premises
            symbols = conclusion.split(self.AND)
            terminals.update([s.strip() for s in symbols if s.strip().islower()])

        return terminals

    
    def parse_rules(self) -> List[Rule]:
        # TODO: initial symbol?
        # TODO: should p_r be common for duplicated rules (with "|")?
        # TODO: determine whether conversion or split rule
        # TODO: support for AND symbol in syntax

        expanded_rules = self.rule_expansion()
        rules = []
        for rule in expanded_rules:
            premise, conclusion = rule.split(self.IMPLY)

            predicate, *symbols = conclusion.split()
            position, axis = float(predicate.strip()[:-1]), predicate.strip()[-1]

            new_rule = SplitRule(premise.strip(), position, axis, [s.strip() for s in symbols])
            rules.append(new_rule)

        return rules
    

    def rule_expansion(self) -> List[str]:
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file]

        rules = []
        for line in stripped_lines:
            if self.OR in line:
                premise, conclusion = line.split(self.IMPLY)
                or_terms = conclusion.split(self.OR)
                rules.extend(f"{premise.strip()} {self.IMPLY} {symbs.strip()}" for symbs in or_terms)

            else:
                rules.append(line)
            
        return rules