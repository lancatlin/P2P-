import socket,server,ipgetter
from random import randint

class network:
    def __init__(self,window):
        self.room = window.roomentry.get()
        self.name = window.nameentry.get()
        self.window = window
        self.data = server.GetIP()
        self.lan_addr = self.get_LAN()
        addr = self.data.search(self.room)
        self.wan = ipgetter.myip()
        if addr == None:
            self.mode = True
            self.start = lambda :self.server()
        else:
            self.mode = False
            self.start = lambda :self.client()
        self.place = socket.gethostname()
    def client(self):
        print('it is client')
    def server(self):
        self.data.set_IP(self.room,self.wan,self.lan_addr[1])
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.socket.bind(self.lan_addr)
        print(self.socket.recvfrom(1024))
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",30000))
        return s.getsockname()[0],randint(50000,60000)
    def close(self):
        if self.mode:
            self.data.clear(self.room)
            self.window.destroy()