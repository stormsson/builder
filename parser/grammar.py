#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import random
import string
from anytree import Node
import re

class Grammar:

    @staticmethod
    def generate_string(tree):
        str = "%s(#)" % tree.name

        if not tree.is_leaf:
            substrings = []
            for child in tree.children:
                substrings.append(Grammar.generate_string(child))

            try:
                substrings = " + ".join(substrings)
            except Exception as e:
                print(substrings)
                raise e
        else:
            substrings =""
        str = string.replace(str, "#", substrings)
        return str




    def __init__(self):
        self.result = ""
        self.rules = []
        self.raw_rules = []

        return

    def set_seed(self, seed=None):
        random.seed(seed)

    def reset_seed(self):
        random.seed(None)

    """
    loads a grammar rules file
    """
    def load_grammar(self, path):
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
    transforms a production defined in the rules as S[min-max] to
    a concatenated OR production without range
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


    """
    after a rule for a production is found,
    this function randomly decides which production to apply, if
    more than 1 is available.
    Ex:
    from this possible production : C | C C | C C C
    the function returns only C or C C or C C C

    @return array of symbols
    """
    def _select_production(self, rule_production):

        random_index = randint(0, len(rule_production)-1)
        selected_item = rule_production[random_index]

        selected_item = self._parse_ranged_production(selected_item)

        selected_item = selected_item.split(" ")
        return selected_item

    """
    given a symbol, generate the subtree corresponding to it.
    index/depth are used to allow custom constraints per level/position
    """
    def generate_tree(self, symbol, index=0, depth=0):
        # symbol, amount = self._parse_ranged_production(symbol)

        replaced = False
        for rule in self.rules:
            if symbol == rule["symbol"]:

                root = Node(symbol, index=index, type=symbol, depth=depth)

                # random_index = randint(0, len(rule["production"])-1)
                # selected_item = rule["production"][random_index]

                # selected_item = self._parse_ranged_production(selected_item)
                selected_production = self._select_production(rule["production"])
                child_index = 0
                for sub_grammar in selected_production:
                    child = self.generate_tree(sub_grammar, index=child_index, depth=depth+1)
                    child.parent = root
                    child_index+=1

                replaced = True

        if not replaced:
            root = Node(symbol, index=index, type=symbol)

        return root