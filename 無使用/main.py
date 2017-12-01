import socket,_thread,time

def server(s):
	global mode
	HOST,PORT = socket.gethostname(),2
	HOST = socket.gethostbyname(HOST)
	s.bind((HOST,PORT))
	s.listen(1)
	use,addr = s.accept()
	use.send('get'.encode('UTF-8'))
	if mode != 'user':
		mode = 'server'
		_thread.start_new_thread(_send,(s,use))
		_thread.start_new_thread(_listen,(s,))
def _send(s,use = None):
	while True:
		data=input()
		if data == 'end':
			break
		data=data.encode('UTF-8')
		if use == None:
			s.send(data)
		else:
			use.send(data)
def _listen(s):
	while True:
		data = s.recv(1024)
		print (str(addr)+': '+data.decode('UTF-8'))
def user(s):
	global mode
	while mode == None:
		host,port = input('輸入對方ip:'),2
		s.connect((host,port))
		if s.recv(1024).decode('UTF-8') == 'get':
			mode = 'user'
	_thread.start_new_thread(_send,(s))
	_thread.start_new_thread(_listen,(s,))
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mode = None
ser=_thread.start_new_thread(server,(s,))
time.sleep(1)
user(s)
s.close()