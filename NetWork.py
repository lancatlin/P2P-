import socket,server,ipgetter,time
from random import randint

class network:
    def __init__(self,window,info):
        self.room,self.name = info[0],info[1]
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.window = window
        self.data = server.GetIP('IP')
        self.client_data = server.GetIP('client')
        self.lan = self.get_LAN()
        self.port = randint(50000,60000)
        addr = self.data.search(self.room)
        self.wan = ipgetter.myip()
        self.target = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.lan,self.port))
        if addr == None:
            self.mode = True
            self.start = lambda :self.server()
        else:
            self.mode = False
            self.start = lambda :self.client()
    def receive(self):
        self.socket.settimeout(5)
        print('receive')
        if self.mode:
            self.send('創建聊天室',mode=False)
            self.window.add_new('創建聊天室')
        else:
            self.send(self.name + '加入聊天室', mode=False)
            self.window.add_new(self.name+'加入聊天室')
        while True:
            try:
                data,host = self.socket.recvfrom(1024)
                if host not in self.target:
                    self.target.append(host)
                    print(self.target)
                    self.socket.sendto(self.massege,host)
                    self.window.add_new(data.decode())
                else:
                    data = data.decode()
                    self.window.add_new(data)
                    if self.mode:
                        self.send(data,mode=False,one=host)
            except socket.timeout:
                target = self.client_data.get_all()
                if self.mode and target != []:
                    for i in target:
                        if i['wan'] == self.wan:
                            print('send to ' + i['lan'])
                            self.socket.sendto(self.massege,(i['lan'],i['port']))
                        else:
                            print('send to ' + i['wan'])
                            self.socket.sendto(self.massege, (i['wan'], i['port']))
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",30000))
        return s.getsockname()[0]
    def close(self):
        self.window.destroy()
    def send(self,s,mode=True,one=None):
        if mode:
            now = time.strftime("[%H-%M]")
            data = now + s
            self.window.add_new('<'+self.name+'>'+data)
            data = '<'+self.name+'>'+data
        else:
            data=s
        data = data.encode('UTF-8')
        if self.mode:
            for i in self.target:
                if i != one:
                    i.send(data)
        else:
            self.socket.send(data)
class server(network):
    def server(self):
        self.data.set_IP(self.room,self.wan,self.lan,self.port)
        self.socket.listen(5)
        self.socket.settimeout(5)
        while True:
            try:
                new,addr = self.socket.accept()
                print(addr+'已連接')
                self.target.append(new)
            except socket.timeout:
                target = self.client_data.get_all()
                if self.mode and target != []:
                    for i in target:
                        if i['wan'] == self.wan:
                            print('send to ' + i['lan'])
                            self.socket.sendto(self.massege, (i['lan'], i['port']))
                        else:
                            print('send to ' + i['wan'])
                            self.socket.sendto(self.massege, (i['wan'], i['port']))
    def close(self):
        self.data.clear(self.room)
        self.send('聊天室關閉',False)
        super().close()
class client(network):
    def client(self):
        print('it is client')
        self.client_data.set_IP(self.name,self.wan,self.lan,self.port)
        self.socket.settimeout(10)
        while True:
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                self.client_data.clear(self.name)
                break
            except socket.timeout:
                addr = self.data.search(self.room)
                if addr['wan'] == self.wan:
                    target = (addr['lan'],addr['port'])
                else:
                    target = (addr['wan'],addr['port'])
                print('嘗試連接到', target)
    def close(self):
        self.client_data.clear(self.name)
        self.send(self.name + '離開聊天室', False)
        super().close()