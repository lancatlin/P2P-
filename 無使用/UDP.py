#傳輸測試1.py
import socket,_thread,time #匯入模組:thread用來分頭執行、time用來等待時間

def server(s):                          #函數server
    HOST,PORT = socket.gethostname(),1  #設定接收ip,port(是自己的)
    HOST = socket.gethostbyname(HOST)
    print(HOST)
    s.bind((HOST,PORT))                 #綁定位址
    while True:                         #重複執行的迴圈
        data,addr = s.recvfrom(1024)    #儲存接收到的 訊息,來源
        print (str(addr)+': '+data.decode('UTF-8')) #印出訊息
    s.close
def user(s):
    host,port = input('輸入對方ip:'),1  #使用者輸入對方ip,port預設1
    print(host,port)                    #顯示
    while True:                         #重複迴圈
        data=input()                    #讓使用者輸入要傳給對方的訊息
        if data == 'end':               #如果輸入的是"end"
            break                       #就結束循環。用來離開重複循環
        data=data.encode('UTF-8')       #把訊息編碼成可以發送的格式
        s.sendto(data,(host,port))      #發送給對方
    s.close
    
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)     #建立物件
#這次設定比較多，第一個設定使用ipv4，第二個設定使用UDP
ser=_thread.start_new_thread(server,(s,))   #開啟一個新的線程來執行server函數
time.sleep(1)                           #等待一下，確保已經開啟Server
user(s)                                 #執行User程式