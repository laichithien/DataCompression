import math
import time
class LZ77(object):
    MAX_WINDOW_SIZE = 400
	
    def __init__(self, window_size=16,lookahead_buffer_size=8):
        self.window_size = min(window_size, self.MAX_WINDOW_SIZE)
        self.lookahead_buffer_size = lookahead_buffer_size
        self.search_buffer_size = self.window_size- self.lookahead_buffer_size
        
    
    def encode(self,text):
        output = '<0,0,' + text[0]+'>'
        i = 1
        while i< len(text):
            offset, length, symbol = 0,0, text[i]
            for j in range(1,min(self.search_buffer_size+1,i)):  
                if (text[i]==text[i-j]):
                    k = 0
                    while (text[i+k]==text[i-j + k] and i+k < len(text)-1):
                        k += 1
                    if length < k:
                        offset, length, symbol = j,k, text[i+k]
            output = output +"<"+str(offset)+','+str(length)+','+symbol+'>'
            if length!=0:
                i = i+k+1
            else: i+=1
            #print(i,':',output)
        return output        

    def decode(self,text):
        start = time.time()
        text = text[1:-1]
        pairs = text.split('><')   
        decoded_str = ""
        for i in range(len(pairs)):
            p = pairs[i].split(',')
            if len(p) == 3:
                offset, length, symbol = pairs[i].split(',')
            elif len(p) == 2: 
                offset, length = pairs[i].split(',')
                symbol = ''
            else:
                offset, length = pairs[i].split(',')[0:2]
                symbol = ','
            offset, length = int(offset), int(length)
            if  length != 0:
                if offset >= length: decoded_str +=  decoded_str[len( decoded_str)-offset:len( decoded_str)-offset+length]
                else: 
                    while (offset < length):
                        decoded_str += decoded_str[len( decoded_str)-offset:len(decoded_str)]
                        length-=offset
                    decoded_str += decoded_str[len( decoded_str)-offset:len( decoded_str)-offset+length]
            decoded_str += symbol
        end = time.time()

        return decoded_str

#encodeLZ('input.txt', 'AAAA.txt')
    def Metric(self,FileIn):
        with open(FileIn, encoding="utf8") as f:
            lines = f.readlines()
        print('LZ77:')
        output = []
        encode = []
        start = time.time()
        for x in lines:
            output.append(self.encode(x))
        end = time.time()
        
        time_encode = end-start
        print('     Encode:',end-start)
        start = time.time()
        for x in output:
            encode.append(self.decode(x))
        end = time.time()
        time_decode = end-start

        print('     Decode:',end-start)
        count = 0
        for x in output:
            count += len(x[1:-1].split('><'))
        with open(FileIn, encoding="utf8") as f:
            text = f.read()
        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count*22) # 3 + 3 + 16
                
        return
        text_from_file = input_file.read()
        output = self.encode(text_from_file)
        encoded_file.writelines(output)
        input_file.close()
        encoded_file.close()
    
    def decodefile(self,FileIn, FileOut):
        input_file = open(FileIn, 'r')
        text_from_file = input_file.read()
        output = self.decode(text_from_file)
        with open(FileOut, mode='w', encoding='UTF-8', errors='strict', buffering=1) as fo:
            fo.writelines(output)
        input_file.close()
        fo.close()
# lz77 = LZ77()
# lz77.Metric('Data.txt')