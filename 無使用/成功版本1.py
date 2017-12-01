import socket,_thread,time

def server(ADDR,ip):                        #伺服器程式
	global mode,data                        #讀取全域變數
	s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)#建立socket物件
	s.bind(ADDR)                            #綁定IP
	print(ADDR)
	addr = ip,4                             #設定目的位址
	_thread.start_new_thread(test,(s ,addr,ADDR))#開啟新線程不停傳送訊息到對方
	data , addr = s.recvfrom(1024)          #讀取收到的訊息
	mode = False                            #利用全域變數讓另一個線程
	print(data)
	s.sendto('ok'.encode('UTF-8'),addr)     #發送訊息"ok"給對方
	s.sendto(data,(addr[0],4))
	_thread.start_new_thread(user,(s ,addr))#開啟新線程來讀取使用者輸入並發送
	while True:
		data,addr = s.recvfrom(1024)        #等待接收訊息
		print (str(addr)+data.decode('UTF-8')) #印出訊息內容
	s.close
def user(s,addr):                           #發送訊息給對方的函數
	while True:
		data=input()                        #讀取使用者輸入
		if data == 'end':                   #如果輸入"end"就結束
			break
		data=data.encode('UTF-8')
		s.sendto(data,addr)                 #發送訊息
	s.close
def test(s,addr,ADDR):                      #不停發送信息的函數
	global mode#讀取全域變數
	global data
	if mode:
		print('準備連接'+str(addr))
		x = 0
		while mode and x <= 1000:   #重複執行直到server說停或者過了100秒
			s.sendto(data,addr)
			time.sleep(0.1)
			x+=1
		if mode:                    #判斷是否成功
			print('連線失敗')
		else:
			print('已連接')
HOST,PORT = socket.gethostname(),4  #取得自己的ip
HOST = socket.gethostbyname(HOST)
ADDR = (HOST,PORT)
mode = True
data = ('test,'+'lancat,'+str(ADDR[0])+','+str(ADDR[1])).encode()
#預設發送信息，內容無意義
time.sleep(0.5)
f=open('C:\\ip.txt','r')            #讀取對方ip
ip = f.read()
f.close()
server(ADDR,ip)                     #啟動server函數