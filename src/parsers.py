from .rules import Rule, SplitRule

from typing import List, Set

import os
import re


class Parser(object):
    def __init__(self, dir: str, filename: str) -> None:
        self.dir = dir
        self.filename = filename
        self.path = os.path.join(self.dir, self.filename)

        self.IMPLY = "::-"
        self.AND = " "
        self.OR = "|"

        assert self.check_rules_integrity(), "Invalid rule syntax"


    def check_rules_integrity(self):
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file if line.strip()]

        for line in stripped_lines:
            if self.IMPLY not in line:
                return False
            
            premise, _ = line.split(self.IMPLY) # Raise an error if several "::-" symbols

            # The premise should contain a single nonterminal symbol
            if premise.strip().islower() or len(premise.split()) > 1:
                return False
            
        return True
            

    def parse_terminals(self) -> Set[str]:
        # TODO: support AND operator in symbols splitting
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file if line.strip()]

        terminals = set()
        for line in stripped_lines:
            _, conclusion = line.split(self.IMPLY)  # Terminals do not appear in premises
            symbols = conclusion.split()
            print(symbols)
            terminals.update([s.strip() for s in symbols if s.strip().islower()])

        return terminals

    
    def parse_rules(self) -> List[Rule]:
        # TODO: should p_r be common for duplicated rules (with "|")?
        # TODO: determine whether conversion or split rule
        # TODO: support for AND symbol in syntax

        expanded_rules = self.rule_expansion()
        rules = []
        for rule in expanded_rules:
            premise, conclusion = rule.split(self.IMPLY)

            pattern = r"\((\d+\.?\d*),\s*(\d+\.?\d*)\)\s*\((\d+\.?\d*),\s*(\d+\.?\d*)\)\s*(\w+)\s*(\w+)"
            match = re.search(pattern, conclusion)
            if match:
                r1 = (float(match.group(1)), float(match.group(2)))
                r2 = (float(match.group(3)), float(match.group(4)))
                symbols = [match.group(5), match.group(6)]

            new_rule = SplitRule(premise.strip(), r1, r2, [s.strip() for s in symbols])
            rules.append(new_rule)

        return rules
    

    def rule_expansion(self) -> List[str]:
        with open(self.path, "r") as file:
            stripped_lines = [line.rstrip("\n") for line in file if line.strip()]

        rules = []
        for line in stripped_lines:
            if self.OR in line:
                premise, conclusion = line.split(self.IMPLY)
                or_terms = conclusion.split(self.OR)
                rules.extend(f"{premise.strip()} {self.IMPLY} {symbs.strip()}" for symbs in or_terms)

            else:
                rules.append(line)
            
        return rules