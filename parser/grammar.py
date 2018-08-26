#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import random
from anytree import Node
import re

from parser.tree_builder import Tree_Builder

class Grammar:

    def __init__(self, grammar_path, seed=None):
        self.result = ""

        # TODO: improve this
        self.production_constraints = []
        self.rules = []
        self.raw_rules = []

        self._load_grammar(grammar_path)

        self.tree_builder = Tree_Builder(seed)

    def set_production_constraints(self, production_constraints):
        self.production_constraints = production_constraints

    def reset_production_constraints(self):
        self.production_constraints = []


    def add_production_constraint(self, production_constraint):
        self.production_constraints.append(production_constraint)


    """
    loads a grammar rules file
    """
    def _load_grammar(self, path):
        with open(path, "r") as grammar_file:
            for line in grammar_file:
                self.raw_rules.append(line)
                elems = line.split("=")
                symbol = elems[0].strip()
                value = elems[1]
                production = [ x.strip() for x in value.split("|") ]
                self.rules.append({"symbol": symbol, "production": production })
        return

    """
    transforms a production defined in the rules as Symbol[min-max] to
    a concatenated OR production without the range syntax
    Ex:
    C[1-3] is transformed to: C | C C | C C C
    """
    def _parse_ranged_production(self, production):
        regexp_qty_pattern="(?P<symbol>.*?)\[(?P<from>\d+)\-(?P<to>\d+)\]"
        match = re.search(regexp_qty_pattern, production)

        repetitions = 1
        if match:
            symbol = match.group("symbol")
            range_from = int(match.group("from"))
            range_to = int(match.group("to"))

            random_amount = randint(range_from, range_to)
            production = [ symbol ] * random_amount

            return " ".join(production)
        else:
            return production

