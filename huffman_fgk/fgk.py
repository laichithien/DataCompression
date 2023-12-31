import sys
import getopt
import time
from huffman_fgk.node import Node

class FGK(object):
    def __init__(self):
        super(FGK, self).__init__()
        self.NYT = Node(symbol="NYT")
        self.root = self.NYT
        self.nodes = []
        self.seen = [None] * 256

    def draw_tree(self, node, level=0):
        if node is None:
            return
        
        print('  ' * level, end='')
        if node.symbol:
            print(f'{node.symbol}:{node.weight}')
        else:
            print(f'[{node.weight}]')
            
        self.draw_tree(node.left, level+1)
        self.draw_tree(node.right, level+1)

    def get_code(self, s, node, code=''):
        if node.left is None and node.right is None:
            return code if node.symbol == s else ''
        else:
            temp = ''
            if node.left is not None:
                temp = self.get_code(s, node.left, code+'0')
            if not temp and node.right is not None:
                temp = self.get_code(s, node.right, code+'1')
            return temp

    def find_node_with_weight(self, weight):
        for n in reversed(self.nodes):
            if n.weight == weight:
                return n

    def swap_node(self, n1, n2):
        i1, i2 = self.nodes.index(n1), self.nodes.index(n2)
        self.nodes[i1], self.nodes[i2] = self.nodes[i2], self.nodes[i1]

        tmp_parent = n1.parent
        n1.parent = n2.parent
        n2.parent = tmp_parent

        if n1.parent.left is n2:
            n1.parent.left = n1
        else:
            n1.parent.right = n1

        if n2.parent.left is n1:
            n2.parent.left = n2
        else:
            n2.parent.right = n2

    def insert(self, s):
        
        
        node = self.seen[ord(s)]

        if node is None:
            spawn = Node(symbol=s, weight=1)
            internal = Node(symbol='', weight=1, parent=self.NYT.parent,
                left=self.NYT, right=spawn)
            spawn.parent = internal
            self.NYT.parent = internal

            if internal.parent is not None:
                internal.parent.left = internal
            else:
                self.root = internal

            self.nodes.insert(0, internal)
            self.nodes.insert(0, spawn)

            self.seen[ord(s)] = spawn
            node = internal.parent

        while node is not None:
            equal = self.find_node_with_weight(node.weight)

            if (node is not equal and node is not equal.parent and
                equal is not node.parent):
                self.swap_node(node, equal)

            node.weight = node.weight + 1
            node = node.parent

    def encode(self, text):
        result = ''

        for s in text:
            # print('-'*20)
            # print(f'Read character: {s}')
            if self.seen[ord(s)]:
                result += self.get_code(s, self.root)
                # print(f'Seen, code: {self.get_code(s, self.root)}')
            else:
                result += self.get_code('NYT', self.root)
                result += bin(ord(s))[2:].zfill(8)
                # print(f"Haven't seen, Zero node: {self.get_code('NYT', self.root)}, character code: {bin(ord(s))[2:].zfill(8)}")
            # print(f'Length: {len(result)}')
            # print(f'New result: {result}')

            
            self.insert(s)
            # print('Current tree:')
            # self.draw_tree(self.root)
            # print('-'*20)

        return result

    def get_symbol_by_ascii(self, bin_str):
        return chr(int(bin_str, 2))

    def decode(self, text):
        result = ''

        symbol = self.get_symbol_by_ascii(text[:8])
        result += symbol
        self.insert(symbol)
        node = self.root

        i = 8
        while i < len(text):
            node = node.left if text[i] == '0' else node.right
            symbol = node.symbol

            if symbol:
                if symbol == 'NYT':
                    symbol = self.get_symbol_by_ascii(text[i+1:i+9])
                    i += 8

                result += symbol
                self.insert(symbol)
                node = self.root

            i += 1

        return result

    def Metric(self, FileIn):
        with open(FileIn, encoding='utf-8') as f:
            lines = f.readlines()
        print('Huffman FGK:')
        output_code = []
        encode = []
        start = time.time()
        for x in lines:
            code = self.encode(x)
            output_code.append(code)
        end = time.time()
        print('     Encode:',end-start)

        start = time.time()
        for code in output_code:
            encode.append(self.decode(code))
        end = time.time()

        print('     Decode:',end-start)

        count = 0
        for code in output_code:
            count += len(code)
        
        with open(FileIn, encoding='utf-8') as f:
            text = f.read()

        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count) # 3 + 3 + 16
        
