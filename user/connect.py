import socket
import re
import queue
import json


class Connect:
    def __init__(self):
        setting = json.load(open('/home/lancat/文件/P2P-/setting.json', 'r'))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((setting['ip'], setting['port']))
        self.info = queue.Queue()

    def search(self, room):
        self.socket.send(('room:'+room).encode())
        data = self.socket.recv(1024)
        data = data.decode()
        print(data)
        if data != 'None':
            return self.dict(data)
        else:
            print('room is None')
            return None

    def set(self, room, wan, lan, port):
        msg = 'set:'+','.join([room, wan, lan, str(port)])
        print(msg)
        self.socket.send(msg.encode())
        print(self.socket.recv(1024))

    def wait_connect(self):
        while True:
            data = self.socket.recv(1024)
            info = self.dict(data)
            self.info.put(info)

    def connect(self, room, wan, lan, port):
        msg = 'connect:'+','.join([room, wan, lan, str(port)])
        self.socket.send(msg.encode())
        print(self.socket.recv(1024))
    def dict(self, string):
        info = re.match(
            '(?P<mode>[^:,]+):(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)', string).groupdict()
        print(info)
        return info

    def remove(self, room):
        msg = 'del:%s' % room
        self.socket.send(msg.encode())
