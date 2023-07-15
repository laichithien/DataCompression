import math
import  collections 
import time
class LZW(object):
    def __init__(self):
        return
    
    def encode(self,text):
        dict_of_codes = {chr(i):i for i in range(256)}
        output = ''
        index = 0
        while index < len(text):
            TempIndex, TrackingString = index+1, text[index] 
            while TempIndex < len(text) and (TrackingString + text[TempIndex]) in dict_of_codes.keys():
                TrackingString += text[TempIndex]
                TempIndex += 1
            output = output + '<'+str(dict_of_codes[TrackingString])+'>'
            if TempIndex < len(text):
                dict_of_codes[TrackingString+text[TempIndex]] = len(dict_of_codes)

            index = TempIndex
        return output       

    def decode(self,text):
        text = text[1:-1]
        code = text.split('><')
        code = [int(code[i]) for i in range (len(code))]
        dict_of_codes = {i:chr(i) for i in range(65536)}
        Document = ''
        Document += dict_of_codes[code[0]]
        TempString = dict_of_codes[code[0]]
        last_output = ''

        for index in range(1, len(code)):
            if code[index] in dict_of_codes.keys():
                last_output = dict_of_codes[code[index]]
                Document += dict_of_codes[code[index]]
                TempString += dict_of_codes[code[index]]
                TempIndex = 1
        
                while TempIndex <= len(TempString) and TempString[:TempIndex] in dict_of_codes.values():
                    TempIndex += 1

                if TempString[:TempIndex] not in dict_of_codes.values():
                    dict_of_codes[len(dict_of_codes)] = TempString[:TempIndex]
                    TempString = TempString[TempIndex-1:]
            else:
                last_output += last_output[0]
                Document += last_output
                dict_of_codes[len(dict_of_codes)] = last_output
        return Document
    def Metric(self,FileIn):
        with open(FileIn, encoding="utf8") as f:
            lines = f.readlines()
        print('LZW:')
        output = []
        encode = []
        start = time.time()
        for x in lines:
            output.append(self.encode(x))
        end = time.time()
        print('     Encode:',end-start)
        start = time.time()
        for x in output:
            encode.append(self.decode(x))
        end = time.time()
        print('     Decode:',end-start)
        count = 0
        mi = 0
        for x in output:
            count += len(x[1:-1].split('><'))
            for j in (x[1:-1].split('><')):
                mi = max(int(j),mi)
        print('     max:',mi)
        with open(FileIn, encoding="utf8") as f:
            text = f.read()
        
        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count*12) # bắt chước slide thầy???
    def encodefile(self,FileIn, FileOut):
        input_file = open(FileIn, 'r')
        encoded_file = open(FileOut, 'w')
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
# w = LZW()
# w.Metric('demo.txt')