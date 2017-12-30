from user import connect
import socket
import time
import window
from Server import network
from user import netWork
from random import randint
from multiprocessing import Process


class Test:
    def test_server(self):
        port = 44445
        server = network.ServerNet(port)
        Process(target=server.start).start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        s.send('room:room'.encode())
        data = s.recv(1024)
        print(data)
        s.send('set:room,0.0.0.0,192.168.1.1,12345'.encode())
        data = s.recv(1024)
        print(data)
        s.send('room:room'.encode())
        print(s.recv(1024))
        s.close()

    def test_run(self):
        port = 55558
        s = network.ServerNet(port)
        Process(target=s.start).start()

    def client(self, port):
        server = netWork.begin(('room', str(randint(1, 10))), port)
        Process(target=server.start).start()
        print('new Process')
        time.sleep(4)

    def test_begin(self, name):
        info = 'room', name
        self.window = window.window(info)
        print('準備連接中')
        self.net = netWork.begin(info)
        self.window.setIp(self.net)
        main = Process(target=self.net.start)
        main.start()
        self.window.mainloop()


t = Test()
Process(target=t.test_run).start()
Process(target=t.test_begin, args = ('server', )).start()
t.test_begin('client')
