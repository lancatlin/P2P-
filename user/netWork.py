import socket
import time
import ipgetter
import connect
from multiprocessing import Process
import threading
from random import randint
import queue

class network:
    def __init__(self, info, c):
        self.room,self.name = info[0],info[1]
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.to_print = queue.Queue()
        self.data = c
        self.lan = self.get_LAN()
        self.port = randint(50000,60000)
        self.wan = ipgetter.myip()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.lan,self.port))

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
            self.to_print.put('<'+self.name+'>'+data)
            data = '@'+self.name+'>'+data
        elif mode == 1:
            data='@'+s
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

    def receive(self,sock):
        try:
            data = sock.recv(1024)
            data = data.decode()
            if data in ['exit','']:
                print('結束連線' + str(sock))
                sock.close()
                return 'close'
            elif data[0] == '@':
                return data
            else:
                print(data)
        except socket.timeout:
            sock.close()
            print('因超時而結束連線'+str(sock))
            return 'close'
        except OSError:
            sock.close()
            print('套接字以斷開連線'+str(sock))
class Server(network):
    def __init__(self, info, c):
        super().__init__(info, c)
        self.target = []
        self.data.set(self.room, self.wan, self.lan, self.port)
        Process(target=self.data.wait_connect).start()
        self.socket.listen(5)

    def start(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind((self.lan, self.port))
        self.socket.settimeout(10)
        self.to_print.put('創建聊天室')
        while True:
            try:
                new, addr = self.socket.accept()
                print(str(addr)+'已連接')
                thread = threading.Thread(target=self.receive,args=(new,))
                thread.start()
                self.target.append(new)
            except socket.timeout:
                try:
                    addr = self.data.info.get(False)
                    addr = self.get_target(addr)
                    udp.sendto(self.massege, addr)
                except queue.Empty:
                    print('尚未有新連線')

    def receive(self,target):
        self.socket.settimeout(10)
        self.send(self.name+'加入聊天室',1)
        while True:
            mode = super().receive(target)
            if not mode:
                self.target.remove(target)
                break
            elif mode is not None:
                self.to_print.put(mode)
                self.send(mode, 2, target)

    def close(self):
        self.send('聊天室關閉',1)
        self.send('exit', 2)
        for i in self.target:
            i.close()
        super().close()

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        for i in self.target:
            if i != one:
                try:
                    i.send(data)
                except OSError:
                    print('套接字無連接')


class Client(network):
    def start(self):
        print('it is client')
        self.socket.settimeout(10)
        while True:
            target = self.get_target(self.data.search(self.room))
            print(target)
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                break
            except socket.timeout:
                self.data.connect(self.room, self.wan, self.lan, self.port)
                print('嘗試連接到', target)
        self.receive(self.socket)

    def close(self):
        self.send(self.name + '離開聊天室', 1)
        self.send('exit', 2)
        self.socket.close()
        super().close()

    def receive(self,sock):
        sock.settimeout(60)
        while True:
            result = super().receive(sock)
            if result == 'close':
                print('break')
                break
            elif result is not None:
                self.to_print.put(result)

    def send(self, s, mode=0, one=None):
        data = super().send(s,mode)
        try:
            self.socket.send(data)
        except OSError:
            print('發送錯誤：套接字無連線')
            self.socket.close()


def begin(info):
    c = connect.Connect()
    mode = c.search(info[0])
    if mode is None:
        return Server(info, c)
    else:
        return Client(info, c)
