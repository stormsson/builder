#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from flask import Flask
from flask import render_template
import flask


import random
import sys
import os

from jinja2 import Environment, BaseLoader, Template, FileSystemLoader
import jinja2


from anytree import PreOrderIter
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = current_dir[:current_dir.rfind(os.path.sep)]
sys.path.insert(0, parent_dir)



from parser.grammar import Grammar
from parser.parameters_generator import Parameters_Generator
from parser.tree_builder import Tree_Builder
from symbols.symbols_rules import Symbols_Rules

app = Flask(__name__)


SYMBOL_CONTENT_PLACEHOLDER= "<symbol-content/>"

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(['server/templates',
                             'server/templates/symbols']),
])
app.jinja_loader = my_loader

env = Environment(loader=my_loader)

@app.route('/')
def generateTreeNoParameter():
    seed = random.randrange(sys.maxsize)
    return generateTree(seed)

@app.route("/<int:seed>")
def generateTree(seed):

    g = Grammar(grammar_path="grammar.txt", seed=seed)
    symbols_rules = Symbols_Rules(symbols_configuration_folder="config/symbols")
    parameters_generator = Parameters_Generator("config/parameters", symbols_rules, g.tree_builder.get_seed())

    tree = g.generate_tree("T")
    tree = parameters_generator.apply_parameters(tree)

    tpl = generateTemplate(tree)
    treeTemplate = env.from_string(tpl)
    return treeTemplate.render(seed=seed, url_for = flask.url_for, tree_string = Tree_Builder.generate_string(tree))

def generateTemplate(tree):
    tpl =SYMBOL_CONTENT_PLACEHOLDER

    for node in PreOrderIter(tree):
        try:
            subtpl = open('server/templates/symbols/'+node.symbol+".html", 'r').read()
            children_subtpl_placeholders = " ".join([ SYMBOL_CONTENT_PLACEHOLDER ] * len(node.children) )
            subtpl = subtpl.replace(SYMBOL_CONTENT_PLACEHOLDER, children_subtpl_placeholders)
        except Exception as e:
            subtpl = "<div>template %s not found</div>" % node.symbol
            raise e

        tpl = tpl.replace(SYMBOL_CONTENT_PLACEHOLDER, subtpl, 1)
        tpl = tpl.replace("<symbol-classes/>", " ".join(node.parameters), 1)


    return tpl

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port = 3333)