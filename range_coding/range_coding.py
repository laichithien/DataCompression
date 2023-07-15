from typing import List, Tuple
from collections import Counter
import pandas as pd
import os
from io import StringIO
import time 
# from decimal import *


class RangeCoding:
    def __init__(self) -> None:
        pass

    def encode(self, string):
        start = time.time()
        freq = dict(Counter(string))
        total_characters = sum(freq.values())

        prob_table = [(char, freq[char]/total_characters) for char in freq]
        prob_table.sort(key=lambda x: x[1], reverse=True)

        ordered_prob_table = []
        low = 0.0
        for char, prob in prob_table:
            high = low + prob
            ordered_prob_table.append((char, low, high))
            low = high
        low = 0.0
        high = 1.0

        for char in string: 
            for char_, low_range, high_range in ordered_prob_table:
                if char_ == char:
                    break
            range_width = high - low 
            high = low + range_width * high_range
            low = low + range_width * low_range 

        code = low
        length = len(string)
        end = time.time()
        print('Range encode:',end - start)

        return code, pd.DataFrame(ordered_prob_table, columns=['Character', 'Low', 'High']), length
    
    def decode(self, code, ordered_prob_table, length):
        start = time.time()
        string = ''
        low = 0.0
        high = 1.0
        # char = ''
        widthRange = abs(high - low)
        currentTable = ordered_prob_table.copy()

        while len(string) < length:
            
            # Scale the original to fit current range
            for index, row in currentTable.iterrows():
                char = row['Character']
                low_range = row['Low']
                high_range = row['High']

                # currentTable.loc[index, 'Low'] = float(low_range) * range + low
                # currentTable.loc[index, 'High'] = float(high_range) * range + low
                
                low_range = row['Low'] = float(low_range) * widthRange + low
                high_range = row['High'] = float(high_range) * widthRange + low

                if low_range <= code < high_range:
                    string+=char
                    sHigh = high_range
                    sLow = low_range
                    # print(f'Original length: {length}')
                    # print(f'Encoded length: {len(string)}')

            low = sLow
            high = sHigh
            widthRange = abs(sHigh-sLow)
        end = time.time()
        print('Range decode:',end - start)
        return string

    def encode_from_file(self, fi, fo):
        with open(fi, 'r') as f:
            string = f.read()

        encoded, table, length = self.encode(string)
        # encoded = format(encoded, '.100f')
        # print(x_str)
        # print(f'Encoded: {encoded}')
        # encoded = encoded*100000000000000
        

        table = table.to_csv(index=False, sep='|', lineterminator='\n')
        result = str(encoded) + '\n\n' + table + '\n\n' + str(length)
        # output_filename = os.path.splitext(os.path.basename(path))[0]+'_encoded_range_coding.txt'
        # folder = os.path.dirname(path)
        with open(fo, 'w') as f:
            f.write(result)
        # print(encoded)
        return True
    
    def decode_from_file(self, fi, fo):
        with open(fi, 'r') as f:
            compressed = f.read()
        
        code, table, length = compressed.split('\n\n')
        
        
        table = pd.read_csv(StringIO(table), lineterminator='\n', sep='|')
        code = float(code)
        result = self.decode(code, table, float(length))

        # output_filename = os.path.splitext(os.path.basename(path))[0]+'_decoded_range_coding.txt'
        # folder = os.path.dirname(path)
        with open(fo, 'w') as f:
            f.write(result)
        return True


