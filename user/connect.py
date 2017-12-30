import socket
import re
import queue


class Connect:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect('127.0.0.1', port)
        self.client = queue.Queue()

    def search(self,room):
        self.socket.send(('room:'+room).encode())
        data = self.socket.recv(1024)
        data = data.decode()
        if data:
            return self.dict(data)
        else:
            print('room is None')
            return None

    def set(self, room, wan, lan, port):
        msg = 'set:'+','.join([room, wan, lan, port])
        print(msg)
        self.socket.send(msg)
        print(self.socket.recv(1024))

    def wait_connect(self):
        while True:
            data = self.socket.recv(1024)
            info = self.dict(data)
            self.client.put(info)

    def dict(self, string):
        info = re.match(
            '(?P<mode>[^:,]+):(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)', string).groupdict()
        print(info)
        return info
