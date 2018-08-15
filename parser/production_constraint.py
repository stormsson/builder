#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Production_Constraint():
    def __init__(self, production, symbol="*", depth="*", index="*"):
        if symbol == depth == index == "*":
            raise ValueError('Symbol, depth and index are all set to "*". At least one parameter must be defined')

        self.symbol = symbol.upper()
        self.depth = depth
        self.index = index
        self.production = production


    def _match_symbol(self, symbol):
        if symbol != self.symbol:
            if self.symbol == "*":
                return True
            return False

        return True

    def _match_depth(self, depth):
        if depth != self.depth:
            if self.depth == "*":
                return True
            return False
        return True

    def _match_index(self, index):
        if index != self.index:
            if self.index == "*":
                return True
            return False

        return True

    def match(self, symbol="*", depth="*", index="*"):
        if symbol == depth == index == "*":
            raise ValueError('Symbol, depth and index are all set to "*". At least one parameter must be defined')

        symbol = symbol.upper()
        return self._match_symbol(symbol) and self._match_depth(depth) and self._match_index(index)
