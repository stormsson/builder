#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import yaml

class Symbols_Rules():
    def __init__(self):
        self.allowed_symbols = {}

    def load_configurations(self, folder):

        for filename in os.listdir(folder):
            if ".yml" in filename:
                with open(folder+"/"+filename) as configuration_file:
                    data = yaml.safe_load(configuration_file)
                    self.allowed_symbols[data["symbol"]] = data
        return