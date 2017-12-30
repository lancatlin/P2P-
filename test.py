from user import connect
import socket
from Server import network
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


t = Test()
t.test_server()
