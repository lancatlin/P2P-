import socket,server

class network:
    def __init__(self,room,name,window):
        self.room = room
        self.name = name
        self.window = window
        self.data = server.GetIP()
        addr = self.data.search(room)
        if addr == None:
            self.server()
        else:
            self.client()
        self.place = socket.gethostname()
    def client(self):
        pass
    def server(self):
        self.data.set_IP()
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        return s.getsockname()[0]