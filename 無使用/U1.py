import _thread
import socket
import sys
import time


def main():
	def server(ADDR,ip):
		global mode,data
		s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		s.bind(ADDR)
		print(ADDR)
		addr = ip,4
		_thread.start_new_thread(test,(s ,addr,ADDR))
		data , addr = s.recvfrom(1024)
		mode = False
		print(data)
		s.sendto('ok'.encode('UTF-8'),addr)
		s.sendto(data,(addr[0],4))
		_thread.start_new_thread(user,(s ,addr))
		while True:
			data,addr = s.recvfrom(1024)
			print (str(addr)+data.decode('UTF-8')) 
		s.close
	def user(s,addr):
		while True:
			data=input()
			if data == 'end':
				break
			data=data.encode('UTF-8')
			s.sendto(data,addr)
		s.close
		sys.exit()
	def test(s,addr,ADDR):
		global mode
		global data
		if mode:
			print('準備連接'+str(addr))
			x = 0
			while mode and x <= 1000:
				s.sendto(data,addr)
				time.sleep(0.1)
				x+=1
			if mode:
				print('連線失敗')
				sys.exit()
			else:
				print('已連接')
	HOST,PORT = socket.gethostname(),4
	HOST = socket.gethostbyname(HOST)
	ADDR = (HOST,PORT)
	mode = True
	data = ('test,'+'lancat,'+str(ADDR[0])+','+str(ADDR[1])).encode()
	time.sleep(0.5)
	ip = input('輸入ip:')
	f.close()
	server(ADDR,ip)
if __name__ == '__main__':
	main()