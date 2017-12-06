import socket,server,ipgetter
from random import randint

class network:
    def __init__(self,window):
        self.massege = ('my name is' + socket.gethostname()).encode()
        self.room = window.roomentry.get()
        self.name = window.nameentry.get()
        self.window = window
        self.data = server.GetIP()
        self.lan_addr = self.get_LAN(),randint(50000,60000)
        addr = self.data.search(self.room)
        self.wan = self.get_LAN()
        if addr == None:
            self.mode = True
            self.start = lambda :self.server()
        else:
            self.mode = False
            self.start = lambda :self.client()
    def client(self):
        print('it is client')
        addr = self.data.search(self.room)
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(self.lan_addr)
        self.socket.sendto(self.massege,addr)
        print(self.socket.recvfrom(1024))
    def server(self):
        self.data.set_IP(self.room,self.wan,self.lan_addr[1])
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(self.lan_addr)
        data,host = self.socket.recvfrom(1024).decode()
        print(host+':'+data)
        self.socket.sendto(self.massege,host)
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",30000))
        return s.getsockname()[0]
    def close(self):
        if self.mode:
            self.data.clear(self.room)
            self.window.destroy()