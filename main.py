#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from parser.grammar import Grammar
from symbols.rules import Symbols_Rules

x = Grammar()
r = Symbols_Rules()
x.load_grammar("rules.txt")
x.set_seed()
# print(x.generate(["T"]))
tree = x.generate_tree("T")

from anytree import RenderTree, AsciiStyle
print(RenderTree(tree, style=AsciiStyle()).by_attr())

print Grammar.generate_string(tree)

r.load_configurations("symbols-config")