import socket,threading,time,sys

class net:
    def __init__(self,ip,window):
        self.window = window
        #暫時測試用
        self.port = 40000
        HOST, PORT = socket.gethostname(), self.port
        HOST = socket.gethostbyname(HOST)
        self.addr =  (self.window.ip, self.port)
        self.mode = True
        self.data = (window.nameentry.get()+',' + str(self.addr[0]) + ',' + str(self.addr[1])).encode('UTF-8')
        time.sleep(0.5)
        self.target = (ip,self.port)
        threading.Thread(target=self.server,args=()).start()
    def server(self):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.s.bind(self.addr)
        print(self.addr)
        #addr = ip,self.window.portentry.get()
        threading.Thread(target=self.test,args=()).start()
        data , self.target = self.s.recvfrom(1024)
        self.mode = False
        self._print('已連接')
        print(data)
        self.s.sendto(self.data,self.target)
        while True:
            data,addr = self.s.recvfrom(1024)
            data = data.decode('UTF-8')
            self.window.add_new(data)
            time.sleep(0.5)
    def user(self,string):
        now = time.strftime("[%H-%M]")
        data=now+string
        self.window.add_new('<You>'+data)
        if self.data == 'end':
            sys.exit()
        data = '<'+self.window.nameentry.get()+'>'+data
        data=data.encode('UTF-8')
        self.s.sendto(data,self.target)
    def test(self):
        if self.mode:
            print('準備連接'+str(self.target))
            x = 0
            while self.mode and x <= 500:
                self.s.sendto(self.data,self.target)
                time.sleep(2)
                x+=1
            if self.mode:
                self._print('連線失敗')
                sys.exit()
            else:
                self._print('已連接')
    def _print(self,s):
        string = str(s)
        self.window._print_(string)