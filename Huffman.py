from queue import PriorityQueue
from collections import Counter


class HuffmanNode:
    def __init__(self, symbol=None, frequency=0, left=None, right=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.frequency < other.frequency

class Huffman:
    def __init__(self):
        return
    
    def build_huffman_tree(self, data):
        frequency_counter = Counter(data)
        priority_queue = PriorityQueue()

        # Create a leaf node for each symbol and add it to the priority queue
        for symbol, frequency in frequency_counter.items():
            priority_queue.put(HuffmanNode(symbol, frequency))

        # Build the Huffman tree by combining the nodes
        while priority_queue.qsize() > 1:
            left = priority_queue.get()
            right = priority_queue.get()
            parent = HuffmanNode(frequency=left.frequency + right.frequency, left=left, right=right)
            priority_queue.put(parent)

        # Return the root of the Huffman tree
        return priority_queue.get()


    def build_huffman_dictionary(self,huffman_tree, prefix='', dictionary={}):
        if huffman_tree is None:
            return

        if huffman_tree.symbol is not None:
            dictionary[huffman_tree.symbol] = prefix

        self.build_huffman_dictionary(huffman_tree.right, prefix + '0', dictionary)
        self.build_huffman_dictionary(huffman_tree.left, prefix + '1', dictionary)

        return dictionary


    def huffman_encode(self,data):
        huffman_tree = self.build_huffman_tree(data)
        huffman_dictionary = self.build_huffman_dictionary(huffman_tree)
        encoded_data = ''.join(huffman_dictionary[symbol] for symbol in data)

        return encoded_data, huffman_tree

    def huffman_decode(self,encoded_data, huffman_tree):
        decoded_data = ''
        current_node = huffman_tree

        for bit in encoded_data:
            if bit == '0':
                current_node = current_node.right
            elif bit == '1':
                current_node = current_node.left

            if current_node.symbol is not None:
                decoded_data += current_node.symbol
                current_node = huffman_tree

        return decoded_data
    def build_encoding_table(self,huffman_tree):
        encoding_table = {}

        def traverse_tree(node, code=''):
            if node.symbol is not None:
                encoding_table[node.symbol] = code
            else:
                traverse_tree(node.right, code + '0')
                traverse_tree(node.left, code + '1')

        traverse_tree(huffman_tree)
        return encoding_table