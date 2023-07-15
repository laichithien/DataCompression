import time
class LZ78(object):
    def __init__(self):
        return
    
    def encode(self,text):
        dict_of_codes = {text[0]: '1'}
        combination = ''
        output = '<0' + text[0]+'>'
        code = 2
        text = text[1:]
        for char in text:
            combination += char
            if combination not in dict_of_codes:
                dict_of_codes[combination] = str(code)
                if len(combination) == 1:
                    output = output + '<0' + combination+'>'
                    #encoded_file.write('0' + combination)
                else:
                    output = output + '<'+dict_of_codes[combination[0:-1]] + combination[-1]+'>'
                    #encoded_file.write(dict_of_codes[combination[0:-1]] + combination[-1])
                code += 1
                combination = ''
        return output        

    def decode(self,text):
        text = text[1:-1]
        pairs = text.split('><')    
        dict_of_codes = {'0': '', '1': pairs[0][-1]}
        output = dict_of_codes['1']
        text = text[2:]
        combination = ''
        code = 2
        for i in range(1,len(pairs)):
            char =  pairs[i][-1]
            combination = pairs[i][:-1]
            dict_of_codes[str(i+1)] = dict_of_codes[combination] + char
            output = output + dict_of_codes[combination] + char
        '''
              for char in text:
            if char in '1234567890':
                combination += char
                
            else:
                dict_of_codes[str(code)] = dict_of_codes[combination] + char
                output = output + dict_of_codes[combination] + char
                #decoded_file.write(dict_of_codes[combination] + char)
                combination = ''
                code += 1

        '''
  
        return output
    
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
    def Metric(self,FileIn):
        with open(FileIn, encoding="utf8") as f:
            lines = f.readlines()
        print('LZ78:')
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
                combination = j[:-1]
                mi = max(int(combination),mi)
        print('     max:',mi)
        with open(FileIn, encoding="utf8") as f:
            text = f.read()
        
        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count*16)
        

# lz78 = LZ78()
# lz78.Metric('demo.txt')

#encodeLZ('input.txt', 'AAAA.txt')