from user import connect
import socket
import time
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
        port = randint(40000, 50000)
        s = network.ServerNet(port)
        Process(target=s.start).start()
        time.sleep(2)
        for i in range(2):
            self.client(port)

    def client(self, port):
        server = netWork.begin(('room', str(randint(1, 10))), port)
        Process(target=server.start).start()
        print('new Process')
        time.sleep(4)


t = Test()
t.test_run()
