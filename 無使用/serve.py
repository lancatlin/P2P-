import socket        #匯入套件

s = socket.socket()  #創造一個socket物件
host =  "192.168.1.41"  #設定目標ip(我的桌機)
print(host)          #顯示出來
port=12345           #設定目標port
s.bind((host,port))  #綁定ip,port

s.listen(5)          #等待使用者連接，(5)是指最多連接5個
while True:
	c ,addr = s.accept()    #accept是等待連接，會給你連接者資料,c用來存取連接者
	print (addr)            #顯示連接者
	c.send('we got it'.encode('UTF-8')) #傳給連接者'we got it'，encode是用來編碼
	c.close()               #關閉連接者