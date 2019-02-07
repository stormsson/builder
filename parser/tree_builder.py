#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import random
import sys


from anytree import Node

class Tree_Builder():
    @staticmethod
    def generate_string(tree):
        str = "%s(#)" % tree.name

        if not tree.is_leaf:
            substrings = []
            for child in tree.children:
                substrings.append(Tree_Builder.generate_string(child))

            try:
                substrings = " + ".join(substrings)
            except Exception as e:
                raise e
        else:
            substrings =""

        str = str.replace( "#", substrings)
        return str

    def __init__(self, seed=None):
        self.seed = None
        self.set_seed(seed)
        self.rules = None

    def set_seed(self, seed=None):
        if not seed:
            seed = random.randrange(sys.maxsize)

        self.seed = seed
        random.seed(self.seed)

    def get_seed(self):
        return self.seed

    def reset_seed(self):
        self.set_seed()


    def generate_tree(self, grammar, starting_symbol):
        self.grammar = grammar

        self.production_constraints = self.grammar.production_constraints
        return self._build_tree(starting_symbol)


    """
    given a symbol, generate the subtree corresponding to it.
    index/depth are used to allow custom constraints per level/position
    """
    def _build_tree(self, symbol, index=[0]):

        depth = len(index) -1

        replaced = False
        for rule in self.grammar.rules:
            if symbol == rule["symbol"]:

                root = Node(symbol, symbol=symbol, depth=len(index)-1, index=index)

                # random_index = randint(0, len(rule["production"])-1)
                # selected_item = rule["production"][random_index]

                # selected_item = self._parse_ranged_production(selected_item)
                selected_production = self._apply_constraints_to_production(rule["production"], symbol, index)
                selected_production = self._select_production(selected_production)
                child_index = 0
                for sub_grammar in selected_production:
                    child = self._build_tree(sub_grammar,  index = index + [child_index])
                    child.parent = root
                    child_index+=1

                replaced = True

        if not replaced:
            root = Node(symbol, symbol=symbol, depth=len(index)-1, index=index)

        return root

    """
    when a rule is found, this function applies the constraints to the production.
    """
    # def _apply_constraints_to_production(self, production, symbol, depth, index):
    def _apply_constraints_to_production(self, production, symbol, index):
        if len(self.grammar.production_constraints):
            for c in self.grammar.production_constraints:
                # if c.match(symbol, depth, index):
                if c.match(symbol, index):
                    production = [ c.production ]
                    break

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

        selected_item = self.grammar._parse_ranged_production(selected_item)

        selected_item = selected_item.split(" ")
        return selected_item
