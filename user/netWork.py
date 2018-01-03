import socket
import time
import ipgetter
import connect
from multiprocessing import Process
import threading
from random import randint
import queue
import select

class network:
    def __init__(self, info, c):
        self.room, self.name = info['room'], info['name']
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.to_print = queue.Queue()
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
            print(data)
            data = data.decode()
            if data in ['exit', '']:
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
        timeout = 10
        self.to_print.put('創建聊天室')
        while True:
            read, write, error = select.select(self.inputs, self.output, self.inputs, timeout)
            if not (read or write or error):
                try:
                    addr = self.data.info.get(False)
                    addr = self.get_target(addr)
                    udp.sendto(self.massege, addr)
                except queue.Empty:
                    print('尚未有新連線')
            for s in read:
                if s is self.socket:
                    new, addr = self.socket.accept()
                    print(str(addr) + '已連接')
                    self.inputs.append(new)
                else:
                    msg = s.recv(1024)
                    if msg: #有內容就印出
                        msg = msg.decode()
                        print(msg)
                    else:   #沒有內容，移除連線
                        self.inputs.remove(s)
                        s.close()
            for s in write:
                try:
                    msg = self.msg[s].get(False)
                    s.send(msg.encode())
                    self.output.remove(s)
                except queue.Empty:
                    print('沒東西要寄出'+str(s))
                except socket.error as e:
                    print(e)

    def close(self):
        self.send('聊天室關閉', 1)
        self.send('exit', 2)
        for i in self.inputs:
            i.close()
            self.inputs.remove(i)
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
    print('I am begin, the mode is' + str(mode))
    if mode is None:
        return Server(info, c)
    else:
        return Client(info, c)
