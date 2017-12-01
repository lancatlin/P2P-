import socket

s = socket.socket() #創造socket物件
host = "192.168.1.9"#設定目標ip
port = 12345        #目標port

s.connect((host,port))  #連接伺服器
print (s.recv(1024))    #顯示收到的訊息，1024為最大資料長度
s.close()           #關掉socket