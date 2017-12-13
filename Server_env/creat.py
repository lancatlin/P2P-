    #creat_new window
import sys,login
def creat():
    print('即將新增新的分數表，取消請輸入exit')
    name = input('輸入舊分數表名稱(如不要請留空): ')
    if name == 'exit':
        sys.exit()
    elif name != '':
        with open('score.sc','r') as file:
            with open(name,'w') as new:
                new.write(file.read())
    print('-'*50)
    print('新分數表設定:')
    while True:
        try:
            info = int(input('新分數表長度: '))
            break
        except:
            if info == 'exit':
                sys.exit()
            print('請輸入數字')
    with open('score.sc','w') as file:
        result = ''
        for i in range(1,info+1):
            result+=str(i)+':0\n'
        file.write(result)
    input('新分數表已建立完成，請重新啟動加分程式')
def new_teen():
    print('即將新增新的組員表，取消請輸入exit')
    name = input('輸入舊組員表名稱(如不要請留空): ')
    if name == 'exit':
        sys.exit()
    elif name != '':
        with open('teen.sc', 'r') as file:
            with open(name, 'w') as new:
                new.write(file.read())
    print('-' * 50)
    print('新分數表設定:')
    result = []
    num = 0
    again = True
    while again:
        result.append([])
        p = 1
        while True:
            try:
                info = input('第{0}組 第{1}位: '.format(num+1,p))
                int(info)
                result[num].append(info)
                p += 1
            except:
                if info == 'exit':
                    again = False
                    break
                elif info == '':
                    break
                print('請輸入數字')
        num += 1
    print(result)
    with open('teen.sc', 'w') as file:
        string = ''
        for i in range(len(result)):
            string += str(i+1)+':'+(','.join(result[i]))+'\n'
        print(string)
        file.write(string)
    input('新分數表已建立完成，請重新啟動加分程式')
def new_code():
    x = 10
    print('即將改變密碼，取消請輸入exit')
    try:
        f = open('code.sc','r')
        code = f.read()
        while code != '':
            name = input('輸入舊密碼: ')
            if name == 'exit':
                sys.exit()
            elif name == login.encode(code,x):
                break
            else:
                print('密碼錯誤')
    except IOError:
        pass
    print('-' * 50)
    print('新密碼設定:')
    while True:
        try:
            info = input('輸入新密碼: ')
            if info == 'exit':
                sys.exit()
            break
        except:
            print('請輸入數字')
    with open('code.sc', 'w') as file:
        result = login.encode(info,-x)
        file.write(result)
    input('新密碼已建立完成，請重新啟動加分程式')
if __name__ == '__main__':
    mode = input('模式:(1)建立新分數表 (2)建立組員名單 (3)更改密碼:')
    if mode == '1':
        creat()
    elif mode == '2':
        new_teen()
    elif mode == '3':
        new_code()