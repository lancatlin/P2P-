import socket,server,ipgetter,time
from random import randint

class network:
    def __init__(self,window):
        self.massege = ('my name is' + socket.gethostname()).encode()
        self.room = window.roomentry.get()
        self.name = window.nameentry.get()
        self.window = window
        self.data = server.GetIP('IP')
        self.client_data = server.GetIP('client')
        self.lan_addr = self.get_LAN(),randint(50000,60000)
        addr = self.data.search(self.room)
        self.wan = ipgetter.myip()
        self.target = []
        if addr == None:
            self.mode = True
            self.start = lambda :self.server()
        else:
            self.mode = False
            self.start = lambda :self.client()
    def client(self):
        print('it is client')
        addr = self.data.search(self.name)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(self.lan_addr)
        self.client_data.set_IP(self.room,self.lan_addr[0],self.lan_addr[1])
        self.socket.sendto(self.massege,addr)
        data,host = self.socket.recvfrom(1024)
        print(host,data)
        self.client_data.clear(self.name)
        self.receive()
    def server(self):
        self.data.set_IP(self.room,self.wan,self.lan_addr[1])
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(self.lan_addr)

        self.receive()
    def receive(self):
        self.socket.settimeout(5)
        while True:
            try:
                data,host = self.socket.recvfrom(1024)
                if host not in self.target:
                    self.target.append(host)
                    self.socket.sendto(self.massege,host)
                else:
                    data = data.decode()
                    self.window.add_new(data)
            except socket.timeout:
                if self.mode:
                    target = self.client_data.get_all()
                    for i in target:
                        self.socket.sendto(self.massege,(i[1],i[2]))
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",30000))
        return s.getsockname()[0]
    def close(self):
        if self.mode:
            self.data.clear(self.room)
            self.send('聊天室關閉')
        self.window.destroy()
    def send(self,s,mode=True):
        if mode:
            now = time.strftime("[%H-%M]")
            data = now + s
            self.window.add_new('<You>' + data)
            data = '<' + self.window.nameentry.get() + '>' + data
        else:
            data=s
        data = data.encode('UTF-8')
        for i in self.target:
            self.socket.sendto(data,i)