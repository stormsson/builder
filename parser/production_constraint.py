#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class Production_Constraint():
    DEFAULT_INDEX = [ "*" ]

    # def __init__(self, production, symbol="*", depth="*", index="*"):
    #     if symbol == depth == index == "*":
    #         raise ValueError('Symbol, depth and index are all set to "*". At least one parameter must be defined')


    #     self.symbol = symbol.upper()
    #     self.depth = depth
    #     self.index = index
    #     self.production = production

    """
    index is an array of integer.
    Each element describes the position of the node at the i-th level
    ex 1:
        [0] is the first node of depth 0 ( the root )
        [0, 0] is the first node at depth 1
        [0, 1] is the second node at depth 1

    ex 2:
        Node('/T', depth=0, index=[0], symbol='T')
        ├── Node('/T/C', depth=1, index=[0, 0], symbol='C')
        │   └── Node('/T/C/Sc', depth=2, index=[0, 0, 0], symbol='Sc')
        │       └── Node('/T/C/Sc/0', depth=3, index=[0, 0, 0, 0], symbol='0')
        └── Node('/T/C', depth=1, index=[0, 1],  symbol='C')
            ├── Node('/T/C/Sc', depth=2, index=[0, 1, 0],  symbol='Sc')
            │   └── Node('/T/C/Sc/0', depth=3, index=[0, 1, 0, 0], symbol='0')
            ├── Node('/T/C/Sc', depth=2, index=[0, 1, 1],  symbol='Sc')
            │   └── Node('/T/C/Sc/L', depth=3, index=[0, 1, 1, 0],  symbol='L')
            ├── Node('/T/C/Sc', depth=2, index=[0, 1, 2],  symbol='Sc')
            │   └── Node('/T/C/Sc/Img', depth=3, index=[0, 1, 2, 0], symbol='Img')
            └── Node('/T/C/Sc', depth=2, index=[0, 1, 3],  symbol='Sc')
                └── Node('/T/C/Sc/0', depth=3, index=[0, 1, 3, 0], symbol='0')
    """
    def __init__(self, production, symbol="*", index=None):

        if not index:
            index = self.DEFAULT_INDEX

        if symbol == index == "*":
            raise ValueError('Symbol and index are all set to "*". At least one parameter must be defined')

        if index == ["*"]:
            self.depth = "*"
        else:
            self.depth = len(index) -1

        self.symbol = symbol.upper()
        self.index = index
        self.production = production

    def __str__(self):
        txt = {
            "symbol": self.symbol,
            "production": self.production,
            "index": self.index,
            "depth": self.depth,
        }

        return str(txt)

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
            if self.index == ["*"]:
                return True
            return False

        return True

    def match(self, symbol="*",  index=["*"]):
        if symbol == index == "*":
            raise ValueError('Symbol and index are all set to "*". At least one parameter must be defined')

        depth = len(index) -1
        print(symbol, index)
        print("match symbol %s: %s" % ( self.symbol , self._match_symbol(symbol)))
        print("match depth: %s: %s" % (self.depth, self._match_depth(depth)))
        symbol = symbol.upper()
        return self._match_symbol(symbol) and self._match_depth(depth) and self._match_index(index)
