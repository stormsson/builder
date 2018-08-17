#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from random import randint
import random
import sys
import string


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

        str = string.replace(str, "#", substrings)
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
