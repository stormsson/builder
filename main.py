#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from parser.grammar import Grammar
from parser.production_constraint import Production_Constraint
from symbols.rules import Symbols_Rules

g = Grammar()
g.load_grammar("rules.txt")

c = Production_Constraint("Img", symbol="T", depth=0)

g.add_production_constraint(c)
tree = g.generate_tree("T")

r = Symbols_Rules()
# print(g.generate(["T"]))

from anytree import RenderTree, ContStyle
print(RenderTree(tree, style=ContStyle()))

print Grammar.generate_string(tree)

r.load_symbols_configurations("config/symbols")