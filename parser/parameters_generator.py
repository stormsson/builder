#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import yaml
import random
from random import randint


class Parameters_Generator():
    def __init__(self, parameters_path, symbols_rules, seed=None):

        self.allowed_parameters = {}
        self._load_parameters(parameters_path)
        self.symbols_rules = symbols_rules
        self.set_seed(seed)

    def set_seed(self, seed=None):
        if not seed:
            seed = random.randrange(sys.maxsize)

        self.seed = seed
        random.seed(self.seed)

    def _load_parameters(self, folder):
        for filename in os.listdir(folder):
            if ".yml" in filename:
                with open(folder+"/"+filename) as configuration_file:
                    data = yaml.safe_load(configuration_file)

                    for parameter in data:
                        self.allowed_parameters[parameter] = data[parameter]

    def _apply_parameters_to_node(self, node, depth, index):
        # if the node doesn't have the parameters container create it
        try:
            p = node.parameters
        except Exception as e:
            node.parameters = [ ]

        # if the node does not allow parameters, simply return
        try:
            node_allowed_parameters = self.symbols_rules.allowed_symbols[node.symbol]["allowed_parameters"]
        except KeyError as e:
            #symbol does not have allowed_parameters
            return


        for parameter in node_allowed_parameters:
            try:
                possible_values = self.allowed_parameters[parameter]
            except KeyError as e:
                print("Parameter %s not found. Requested by node %s at depth %d, index %d" % (parameter, node.name, depth, index))
                raise e

            random_index = randint(0, len(possible_values))
            # for each possible parameter, we need to add a probability that the parameter
            # is not applied.
            # this is checked by creating a random number between 0 - len(parameters). note there is NOT the -1
            # if the generated number is == len(parameters) it would be out of range, therefore i consider this
            # specific value as a further element of the array, without having to modify it

            if random_index == len(possible_values):
                # print("skip for node %s/%s/%s, parameter %s " % (node.symbol, depth, index, parameter))
                # skip this parameter
                continue
            else:
                node.parameters.append(possible_values[random_index])



    def apply_parameters(self, root_node, depth=0, index=0):

        self._apply_parameters_to_node(root_node, depth, index)

        child_index = 0
        for c in root_node.children:
            self.apply_parameters(c, depth+1, child_index)
            child_index+= 1

        return root_node

