import time
class RLE:
    def __init__(self) -> None:
        pass

    def encode(self, string):
        n = len(string)
        i = 0
        code = ""
        while i < n:
    
            # Count occurrences of
            # current character
            count = 1
            while (i < n - 1 and
                string[i] == string[i + 1]):
                count += 1
                i += 1
            i += 1
            code += "<"
            code += string[i-1]+str(count)
            code +='>'
        return code
    
    def decode(self, string):
        string = string[1:-1]
        pairs = string.split('><')   
        decoded_str = ""
        i = 0
        for i in range(len(pairs)):
            char = pairs[i][0]
            count = int(pairs[i][1:])
            decoded_str += char * count
            i += 2
        return decoded_str
    
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
        print('RLE:')
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
                combination = j[1:]
                mi = max(int(combination),mi)
        print('     max:',mi)
        with open(FileIn, encoding="utf8") as f:
            text = f.read()
        
        print('     Kích thước đầu:',(len(text)-499)*16)
        print('     Kích thước nén:',count*19) # 16 + 


                