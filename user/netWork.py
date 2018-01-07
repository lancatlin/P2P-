import socket
import time
from random import randint
import queue
import select


class network:
    def __init__(self, info):
        self.room, self.name = info['room'], info['name']
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.to_print = queue.Queue()
        self.port_range = [x for x in range(50000, 50100)]

        self.lan = self.get_LAN()
        self.port = randint(50000, 50100)
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


class Server(network):
    def __init__(self, info):
        super().__init__(info)
        print('I am server')
        self.inputs = []
        self.output = []
        self.msg = {}
        self.socket.listen(5)

    def start(self):
        timeout = 1
        self.to_print.put('創建聊天室')
        self.inputs.append(self.socket)
        while True:
            read, write, error = select.select(self.inputs, self.output, self.inputs, timeout)
            if not (read or write or error):
                continue
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
                        else:
                            print(msg)
                        self.send(msg, mode=2, one=s)
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
        super().close()

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        for i in self.msg.keys():
            if i is not one:
                self.msg[i].put(data)
                self.output.append(i)


class Client(network):
    def start(self):
        print('it is client')
        self.socket.settimeout(1)
        for p in self.port_range:
            target = self.room, p
            print(target)
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                self.receive()
            except socket.timeout:
                print('連接過時')
            except ConnectionRefusedError:
                pass
            except ConnectionAbortedError as e:
                print(e)
        print('找不到伺服器，結束程式')
        self.close()

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
        try:
            self.socket.send(data)
        except OSError:
            print('發送錯誤：套接字無連線')
            self.socket.close()


def begin(info):
    print(info)
    if info['isS'] is True:
        return Server(info)
    else:
        return Client(info)
