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

    def _parse_ranged_production(self, production):
        regexp_qty_pattern="(?P<symbol>.*?)\[(?P<from>\d+)\-(?P<to>\d+)\]"
        match = re.search(regexp_qty_pattern, production)

        repetitions = 1
        if match:
            symbol = match.group("symbol")
            range_from = int(match.group("from"))
            range_to = int(match.group("to"))

            random_amount = randint(range_from, range_to)
            print(symbol)

            production = [ symbol ] * random_amount

            return " ".join(production)
        else:
            return production



    def generate_tree(self, symbol):
        # symbol, amount = self._parse_ranged_production(symbol)

        replaced = False
        for rule in self.rules:
            if symbol == rule["symbol"]:

                root = Node(symbol)
                random_index = randint(0, len(rule["production"])-1)
                selected_item = rule["production"][random_index]

                selected_item = self._parse_ranged_production(selected_item)
                for sub_grammar in selected_item.split(" "):
                    child = self.generate_tree(sub_grammar)
                    child.parent = root
                replaced = True

        if not replaced:
            root = Node(symbol)

        return root



    # def generate_tree(self, grammar):


    #     for symbol in grammar:
    #         symbol, amount = self._parse_ranged_production(symbol)


    #         replaced = False
    #         # print("%s" % symbol)
    #         for rule in self.rules:
    #             if symbol == rule["symbol"]:

    #                 root = Node(symbol)
    #                 random_index = randint(0, len(rule["production"])-1)
    #                 selected_item = rule["production"][random_index]

    #                 for sub_grammar in selected_item.split(" "):
    #                     child = self.generate_tree([sub_grammar])
    #                     child.parent = root
    #                 replaced = True

    #         if not replaced:
    #             root = Node(symbol)

    #     return root
