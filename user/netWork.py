import socket
import time
import ipgetter
import connect
from multiprocessing import Process
from random import randint
import queue
import select


class network:
    def __init__(self, info, c):
        self.room, self.name = info['room'], info['name']
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.to_print = queue.Queue()

        self.to_print.put('test')

        self.data = c
        self.lan = self.get_LAN()
        self.port = randint(50000, 60000)
        self.wan = ipgetter.myip()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.lan, self.port))

    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 30000))
        return s.getsockname()[0]

    def close(self):
        pass

    def send(self, s, mode=0):
        if mode == 0:
            now = time.strftime("[%H-%M]")
            data = now + s
            self.to_print.put(self.name+'>'+data)
            data = '@'+self.name+'>'+data
        elif mode == 1:
            data = '@'+s
        else:
            data = s
        data = data.encode('UTF-8')
        return data

    def get_target(self, info):
        result = []
        if info['wan'] == self.wan:
            return info['lan'], int(info['port'])
        else:
            return info['wan'], int(info['port'])


class Server(network):
    def __init__(self, info, c):
        super().__init__(info, c)
        print('I am server')
        self.inputs = []
        self.output = []
        self.msg = {}
        self.data.set(self.room, self.wan, self.lan, self.port)
        Process(target=self.data.wait_connect).start()
        self.socket.listen(5)

    def start(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind((self.lan, self.port))
        timeout = 1
        self.to_print.put('創建聊天室')
        self.inputs.append(self.socket)
        while True:
            read, write, error = select.select(self.inputs, self.output, self.inputs, timeout)
            if not (read or write or error):
                try:
                    addr = self.data.info.get(False)
                    addr = self.get_target(addr)
                    udp.sendto(self.massege, addr)
                except queue.Empty:
                    pass
            for s in read:
                if s is self.socket:
                    new, addr = self.socket.accept()
                    print(str(addr) + '已連接')
                    self.inputs.append(new)
                    self.msg[new] = queue.Queue()
                else:
                    msg = s.recv(1024)
                    if msg: #有內容就印出
                        msg = msg.decode()
                        if msg[0] == '@':
                            self.to_print.put(msg)
                    else:   #沒有內容，移除連線
                        self.inputs.remove(s)
                        s.close()
            for s in write:
                try:
                    msg = self.msg[s].get(False)
                    s.send(msg)
                    self.output.remove(s)
                except queue.Empty:
                    print('沒東西要寄出'+str(s))
                except socket.error as e:
                    print(e)

    def close(self):
        self.data.remove(self.room)
        super().close()

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        if one:
            self.msg[one].put(data)
            self.output.append(one)
        else:
            for i in self.msg.keys():
                self.msg[i].put(data)
                self.output.append(i)


class Client(network):
    def start(self):
        print('it is client')
        self.socket.settimeout(10)
        while True:
            target = self.get_target(self.data.search(self.room))
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                break
            except socket.timeout:
                self.data.connect(self.room, self.wan, self.lan, self.port)
                print('嘗試連接到', target)
        self.receive()

    def close(self):
        self.send(self.name + '離開聊天室', 1)
        self.send('exit', 2)
        self.socket.close()
        super().close()

    def receive(self):
        self.socket.settimeout(60)
        self.socket.send(self.massege)
        while True:
            try:
                result = self.socket.recv(1024)
                result = result.decode()
                if result:
                    self.to_print.put(result)
                else:
                    self.socket.close()
            except socket.timeout:
                pass

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        print(data)
        try:
            self.socket.send(data)
        except OSError:
            print('發送錯誤：套接字無連線')
            self.socket.close()


def begin(info):
    c = connect.Connect()
    mode = c.search(info['room'])
    if mode is None:
        return Server(info, c)
    else:
        return Client(info, c)
