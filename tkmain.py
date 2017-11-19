import socket,threading,time,sys

class net:
    def __init__(self,ip,window):
        self.window = window
        #暫時測試用
        self.port = 40000
        self.addr =  (self.get_LAN(), self.port)
        self.mode = True
        self.message = (window.nameentry.get()+',' + str(self.addr[0]) + ',' + str(self.addr[1])).encode('UTF-8')
        time.sleep(0.5)
        self.target = (ip,self.port)
        ser = threading.Thread(target=self.server)
        ser.setDaemon(True)
        ser.start()
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
        self.s.sendto(self.message,self.target)
        while True:
            data,addr = self.s.recvfrom(1024)
            data = data.decode('UTF-8')
            self.window.add_new(data)
            time.sleep(0.5)
    def user(self,string):
        now = time.strftime("[%H-%M]")
        data=now+string
        self.window.add_new('<You>'+data)
        if data == 'end':
            sys.exit()
        data = '<'+self.window.nameentry.get()+'>'+data
        data=data.encode('UTF-8')
        self.s.sendto(data,self.target)
    def test(self):
        if self.mode:
            print('準備連接'+str(self.target))
            x = 0
            while self.mode and x <= 500:
                self.s.sendto(self.message,self.target)
                time.sleep(5)
                x+=1
            if self.mode:
                self._print('連線失敗')
                sys.exit()
            else:
                self._print('已連接')
    def _print(self,s):
        string = str(s)
        self.window._print_(string)
    def get_LAN(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        return s.getsockname()[0]
