#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from parser.grammar import Grammar
from parser.production_constraint import Production_Constraint
from parser.parameters_generator import Parameters_Generator
from parser.tree_builder import Tree_Builder
from symbols.symbols_rules import Symbols_Rules

# create a grammar
g = Grammar(grammar_path="grammar.txt", seed=1)

# load symbols rules
symbols_rules = Symbols_Rules(symbols_configuration_folder="config/symbols")

# create production constraint example
# c = Production_Constraint("Img", symbol="T", depth=0)
# c1 = Production_Constraint("0", symbol="C", depth=1, index=1)

# add production constraints to grammar
# g.add_production_constraint(c1)

# create parameters generator
parameters_generator = Parameters_Generator("config/parameters", symbols_rules, g.tree_builder.get_seed())

tree = g.generate_tree("T")
tree = parameters_generator.apply_parameters(tree)

print Tree_Builder.generate_string(tree)





from anytree import RenderTree, ContStyle
print(RenderTree(tree, style=ContStyle()))



