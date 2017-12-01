import socket,_thread           #匯入套件

def server(s,host,port):        #server的程式
	s.bind((host,port))         #綁定ip
	s.listen(1)                 #接受一個人的連接，()內數字代表人數
	user , addr = s.accept()    #取得連接者的資料
	print(addr)                 #顯示連接者地址
	sent(user,'get')            #傳給連接者"get"
	_thread.start_new_thread(sender,(user,))    #開啟一個新線程來跟對方聊天
	listener(user)              #開啟收訊息函數
def sent(s,string):             #發送訊息函數，用來簡化操作過程
	s.send(string.encode('UTF-8'))  #將傳入的數編碼後發出去
def _listen(s):                 #簡化收訊息函數
	data = s.recv(1024)         #等待接收訊息
	return data.decode('UTF-8') #回傳訊息內容
def user(s,port):               #User的程式
	addr = (input('目的ip:'),port)    #詢問對方ip
	s.connect(addr)             #連接對方
	print(_listen(s))           #印出收到的訊息
	_thread.start_new_thread(sender,(s,))   #開啟一個新線程來跟對方聊天
	listener(s)                 #開啟收訊息函數
def sender(a):                  #跟對方聊天的程式
	while True:                 #重複迴圈
		data = input()          #取得輸入
		sent(a,data)            #寄送給對方
def listener(b):                #收訊息函數
	while True:                 #重複迴圈
		data = _listen(b)       #接收訊息
		print(data)             #顯示訊息
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)  #建立socket物件，這次是TCP
host = socket.gethostname()     #取得自己的ip
port = 1
mode = input('server or user?') #設定模式，Server或User
if mode == 'server':            #判斷模式
	server(s,host,port)
elif mode == 'user':
	user(s,port)