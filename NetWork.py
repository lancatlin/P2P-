import socket,sheet,ipgetter,time,threading
from random import randint

class network:
    def __init__(self,window,info):
        self.room,self.name = info[0],info[1]
        self.massege = ('my name is ' + self.name + ' in room:' + self.room).encode()
        self.window = window
        self.data = sheet.GetIP('IP')
        self.client_data = sheet.GetIP('client')
        self.lan = self.get_LAN()
        self.port = randint(50000,60000)
        self.wan = ipgetter.myip()
        self.target = []
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.lan,self.port))
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
        return data
    def get_target(self,sheet,one=None):
        if one != None:
            i = sheet.search(one)
            if i['wan'] == self.wan:
                return i['lan'],i['port']
            else:
                return i['wan'],i['port']
        else:
            target = sheet.get_all()
            for i in target:
                result = []
                if i['wan'] == self.wan:
                    result.append((i['lan'],i['port']))
                else:
                    result.append((i['wan'],i['port']))
class server(network):
    def start(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind((self.lan, self.port))
        self.data.set_IP(self.room,self.wan,self.lan,self.port)
        self.socket.listen(5)
        self.socket.settimeout(10)
        while True:
            try:
                new,addr = self.socket.accept()
                print(addr+'已連接')
                thread = threading.Thread(target=self.receive,args=(new,))
                thread.start()
                self.target.append({'socket':new,'addr':addr,'thread':thread})
            except socket.timeout:
                for i in self.get_target(self.client_data):
                    udp.sendto(i)
    def receive(self,target):
        self.socket.settimeout(20)
        while True:
            try:
                data,addr = target.recv(1024)
                data = data.decode()
                self.window.add_new(data)
                self.send(data, mode=False, one=target)
            except socket.timeout:
                self.target.remove(target)
                target.close()
    def close(self):
        self.data.clear(self.room)
        self.send('聊天室關閉',False)
        super().close()
    def send(self,s,mode=True,one=None):
        data = super().send(s,mode,one)
        try:
            self.socket.send(data)
            for i in self.target:
                if i != one:
                    i['socket'].send(data)
        except BrokenPipeError as e:
            print(e)
class client(network):
    def start(self):
        print('it is client')
        self.client_data.set_IP(self.name,self.wan,self.lan,self.port)
        self.socket.settimeout(10)
        target = self.get_target(self.data,self.room)
        while True:
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                self.client_data.clear(self.name)
                break
            except socket.timeout:
                target = self.get_target(self.data,self.room)
                print('嘗試連接到', target)
    def close(self):
        self.client_data.clear(self.name)
        self.send(self.name + '離開聊天室', False)
        super().close()
    def receive(self):
        self.socket.settimeout(20)
        while True:
            try:
                data, addr = self.socket.recv(1024)
                data = data.decode()
                self.window.add_new(data)
            except socket.timeout:
                print('過久沒有連線')
    def send(self,s,mode=True,one=None):
        data = super().send(s,mode,one)
        try:
            self.socket.send(data)
        except BrokenPipeError as e:
            print(e)
def begin(window,info):
    data = sheet.GetIP('IP')
    addr = data.search(info[0])
    if addr == None:
        return server(window,info)
    else:
        return client(window,info)