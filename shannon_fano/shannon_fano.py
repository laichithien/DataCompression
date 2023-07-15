import pandas as pd
from shannon_fano.node import Node
from io import StringIO
import os
import struct
import pickle
import time

class ShannonFano:

    def __init__(self) -> None:
        
        pass

    def sortByProbability(self):
        temp=Node()
        for j in range(1,self.distinctCount) :
            for i in range(self.distinctCount - 1) :
                if ((self.tree[i].pro) > (self.tree[i + 1].pro)) :
                    temp.pro = self.tree[i].pro
                    temp.sym = self.tree[i].sym
    
                    self.tree[i].pro = self.tree[i + 1].pro
                    self.tree[i].sym = self.tree[i + 1].sym
    
                    self.tree[i + 1].pro = temp.pro
                    self.tree[i + 1].sym = temp.sym
    
    def shannon(self, l, h):
        pack1 = 0; pack2 = 0; diff1 = 0; diff2 = 0
        # Check if low reach high 
        if ((l + 1) == h or l == h or l > h) :
            if (l == h or l > h):
                return
            # If low reach high
            
            self.tree[h].top+=1
            self.tree[h].arr[(self.tree[h].top)] = 0
            self.tree[l].top+=1
            self.tree[l].arr[(self.tree[l].top)] = 1
            
            return
        
        else :
            for i in range(l,h):
                pack1 = pack1 + self.tree[i].pro
            pack2 = pack2 + self.tree[h].pro
            diff1 = abs(pack1 - pack2)
            j = 2
            while (j != h - l + 1) :
                k = h - j
                pack1 = pack2 = 0
                for i in range(l, k+1):
                    pack1 = pack1 + self.tree[i].pro
                for i in range(h,k,-1):
                    pack2 = pack2 + self.tree[i].pro
                diff2 = abs(pack1 - pack2)
                if (diff2 >= diff1):
                    break
                diff1 = diff2
                j+=1
            
            k+=1
            for i in range(l,k+1):
                
                self.tree[i].top+=1
                self.tree[i].arr[(self.tree[i].top)] = 1
                
            for i in range(k + 1,h+1):
                self.tree[i].top+=1
                self.tree[i].arr[(self.tree[i].top)] = 0
                
    
            self.shannon(l, k)
            self.shannon(k + 1, h)

    def preprocessing(self, string):
        n = len(string)
        total = 0
        charProb = {}

        for char in string:
            # print(char)
            if char in charProb:
                charProb[char] += 1
            else:
                charProb[char] = 1
        for char in charProb:
            charProb[char] = round(charProb[char]/ n, 3)
        self.distinctCount = len(set(string))
        self.tree = [Node() for _ in range(self.distinctCount+1)]

        for e, (key, value) in enumerate(charProb.items()):
            self.tree[e].sym = key
            self.tree[e].pro = value
            total = total + value
        
        self.tree[self.distinctCount] = 1 - total
        
        self.sortByProbability()
        for i in range(self.distinctCount):
            self.tree[i].top = -1

    def display(self):
        print("\n\n\n\tSymbol\tProbability\tCode",end='')
        for i in range(self.distinctCount - 1,-1,-1):
            print("\n\t", self.tree[i].sym, "\t\t", self.tree[i].pro,"\t",end='')
            for j in range(self.tree[i].top+1):
                print(self.tree[i].arr[j],end='')

    def encode(self, string):
        start = time.time()
        self.preprocessing(string)
        self.shannon(0, self.distinctCount - 1)
        self.metadata = pd.DataFrame(columns=['Character', 'Probability', 'Code'])
        row = 0
        for i in range(self.distinctCount - 1, -1, -1):
            self.metadata.loc[row, 'Character'] = self.tree[i].sym
            self.metadata.loc[row, 'Probability'] = self.tree[i].pro
            code = ''
            for j in range(self.tree[i].top+1):
                code += str(self.tree[i].arr[j])
            self.metadata.loc[row, 'Code'] = code
            row += 1
        # print(self.metadata)
        encoded = ''
        for char in string:
            # encoded += '<'
            c = self.metadata.loc[self.metadata['Character'] == char, 'Code'].iloc[0]
            encoded += c
            # encoded += '>'

        end = time.time()
        # print(f'Shannon Fano encode: {end - start}')
        return encoded, self.metadata
    
    def decode(self, string, table):
        start = time.time()
        table = table.sort_values(by='Code', key=lambda x: x.str.len(), ascending=False)
        result = ""
        while len(string) > 0:
            for index, row in table.iterrows():
                code = row["Code"]
                if string.startswith(code):
                    char = row["Character"]
                    result += char
                    string = string[len(code):]
                    break
        end = time.time()
        # print(f'Shannon Fano decode: {end-start}')
        return result
        
    def encode_from_file(self, fi, fo):
        with open(fi, 'r') as f:
            string = f.read()

        encoded, meta = self.encode(string)

        meta = self.metadata.to_csv(index=False, sep='|', lineterminator='\n')
        
        result = encoded + '\n\n' + meta
        print(encoded)
        # output_filename = os.path.splitext(os.path.basename(path))[0]+'_encoded_shannon_fano.txt'
        # folder = os.path.dirname(path)
        with open(fo, 'w') as f:
            f.write(result)
        return True
        
    def decode_from_file(self, fi, fo):
        with open(fi, 'r') as f:
            compressed = f.read()
        
        string, table = compressed.split('\n\n')
        
        table = pd.read_csv(StringIO(table), lineterminator='\n', sep='|', dtype=str)
        # table['Code'] = table['Code'].astype(str)

        result = self.decode(string, table)

        with open(fo, 'w') as f:
            f.write(result)
        return True
        
    def encode_from_file_1(self, path):
        with open(path, 'r') as f:
            string = f.read()
        
        encoded, meta = self.encode(string)
        encoded_bin = bytearray(int(encoded[i:i+8], 2) for i in range(0, len(encoded), 8))
        output_filename = os.path.splitext(os.path.basename(path))[0]+'_encoded_shannon_fano.bin'
        folder = os.path.dirname(path)
        with open(folder+'/'+output_filename, 'wb') as f:
            f.write(struct.pack('I', len(encoded_bin)))
            f.write(encoded_bin)

        
        # Convert the encoded message to binary format

        # binary_encoded = ''.join(str(bit) for bit in encodeds)
        # binary_encoded = binary_encoded.encode('utf-8')


        # # Serialize the metadata to binary format
        # binary_meta = pickle.dumps(self.metadata)

        # # Write the binary-encoded message to a file
        # output_filename = os.path.splitext(os.path.basename(path))[0]+'_encoded_shannon_fano.bin'
        # folder = os.path.dirname(path)
        # with open(folder+'/'+output_filename, 'wb') as f:
        #     f.write(struct.pack('I', len(binary_encoded)))
        #     f.write(binary_encoded)

        # # Write the serialized metadata to a separate file
        # meta_filename = os.path.splitext(os.path.basename(path))[0]+'_metadata_shannon_fano.bin'
        # with open(folder+'/'+meta_filename, 'wb') as f:
        #     f.write(binary_meta)

        return True
    
    def decode_from_file_1(self, path):
        # Read the binary-encoded message from the file
        # with open(path, 'rb') as f:
        #     length = struct.unpack('I', f.read(4))[0]
        #     binary_encoded = f.read(length)
        with open(path, 'rb') as f:
            length_bytes = f.read(4)
            length = struct.unpack('I', length_bytes)[0]
        with open(path, 'rb') as f:
            f.seek(4)
            binary_data = f.read(length)
        # Convert the binary-encoded message back to a string of bits
        encoded = ''.join(format(byte, '08b') for byte in binary_data)


        # Read the serialized metadata from a separate file and deserialize it
        
        meta_filename = os.path.splitext(os.path.basename(path))[0]
        meta_filename = meta_filename.split('_')[0]
        meta_filename += '_metadata_shannon_fano.bin'
        folder = os.path.dirname(path)
        with open(folder+'/'+meta_filename, 'rb') as f:
            binary_meta = f.read()
        table = pickle.loads(binary_meta)

        # Decode the message using the metadata
        result = self.decode(encoded, table)

        output_filename = os.path.splitext(os.path.basename(path))[0]+'_decoded_shannon_fano.txt'
        with open(folder+'/'+output_filename, 'w') as f:
            f.write(result)

        return True
    
    def Metric(self, FileIn):
        with open(FileIn, encoding='utf-8') as f:
            lines = f.readlines()
        print('Shannon-Fano:')
        output_code = []
        output_table = []
        encode = []
        start = time.time()
        for x in lines:
            code, table = self.encode(x)
            output_code.append(code)
            output_table.append(table)
        end = time.time()
        print('     Encode:',end-start)

        start = time.time()
        for code, table in zip(output_code, output_table):
            encode.append(self.decode(code, table))
        end = time.time()

        print('     Decode:',end-start)

        count = 0
        for code, table in zip(output_code, output_table):
            count += len(code)
            sum_table = 0
            for row in table.iterrows():
                sum_table += 8 + int(len(row[1]['Code'])) 
            count += sum_table
        
        with open(FileIn, encoding='utf-8') as f:
            text = f.read()

        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count) # 3 + 3 + 16
        