import os
class code:
    @staticmethod
    def encode(text,mode=False,password=0):
        #mode 為解密，not mode為加密
        if not mode:
            long = len(text)
        else:
            long = ''
            for i in range(len(text)):
                if text[i] == '!':
                    text = text.strip(long + '!')
                    break
                else:
                    long += text[i]
            long = int(long)
        # 計算
        password %= long
        while len(text) % password != 0 and not mode:
            text += ' '
        xword = len(text) // password
        result = []
        k = 0
        if mode:
            p = password
            x = xword
        else:
            p = xword
            x = password
        for i in range(p):
            result.append('')
            for j in range(x):
                result[-1] += text[k]
                k += 1
        if not mode:
            string = str(long) + '!'
        else:
            string = ''
        for i in range(x):
            for j in result:
                string += j[i]
        return string
class key:
    def read(self):
        with open('encode_key.txt','r') as file:
            with open('key.json','w') as key_file:
                decode = code.encode(text=file.read(),mode=True,password=17)
                key_file.write(decode)
    def remove(self):
        os.remove('key.json')
    def set(self):
        with open('P2P talking-1246da9b2e36.json','r') as file:
            self.key = code.encode(text=file.read(),mode=False,password=17)
            print(self.key)
            print(code.encode(text=self.key,mode=True,password=17))
        with open('encode_key.txt','w') as key_file:
            key_file.write(self.key)