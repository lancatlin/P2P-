import socket, sheet, ipgetter, time, threading
from random import randint


class network:
    def __init__(self, window, info):
        self.room, self.name = info[0], info[1]
        self.massege = ('my name is %s in %s' % (self.name, self.room)).encode()
        self.window = window
        self.data = sheet.GetIP('IP')
        self.client_data = sheet.GetIP('client')
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
        self.window.destroy()

    def send(self, s, mode=0):
        if mode == 0:
            now = time.strftime("[%H-%M]")
            data = now + s
            self.window.add_new(self.name+'>'+data)
            data = '@'+self.name+'>'+data
        elif mode == 1:
            data = '@'+s
        else:
            data = s
        data = data.encode('UTF-8')
        return data

    def get_target(self, sheet, one=None):
        if one is not None:
            i = sheet.search(one)
            if i['wan'] == self.wan:
                return i['lan'], i['port']
            else:
                return i['wan'], i['port']
        else:
            target = sheet.get_all()
            result = []
            for i in target:
                if i['wan'] == self.wan:
                    result.append((i['lan'], i['port']))
                else:
                    result.append((i['wan'], i['port']))
            return result

    def receive(self, sock):
        try:
            data = sock.recv(1024)
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


class server(network):
    def __init__(self, window, info):
        super().__init__(window, info)
        self.target = []
        self.data.set_IP(self.room, self.wan, self.lan, self.port)
        self.socket.listen(5)

    def start(self):
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        udp.bind((self.lan, self.port))
        self.socket.settimeout(10)
        self.window.add_new('創建聊天室')
        while True:
            try:
                new, addr = self.socket.accept()
                print('%s已連接' % str(addr))
                thread = threading.Thread(target=self.receive, args=(new,))
                thread.start()
                self.target.append(new)
            except socket.timeout:
                addr = self.get_target(self.client_data)
                for i in addr:
                    udp.sendto(self.massege, i)

    def receive(self, target):
        self.socket.settimeout(10)
        self.send(self.name+'加入聊天室', 1)
        while True:
            mode = super().receive(target)
            if not mode:
                self.target.remove(target)
                break
            elif mode is not None:
                self.window.add_new(mode)
                self.send(mode, 2, target)

    def close(self):
        self.data.clear(self.room)
        self.send('聊天室關閉', 1)
        self.send('exit', 2)
        for i in self.target:
            i.close()
        super().close()

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        for i in self.target:
            if i != one:
                try:
                    i.send(data)
                except OSError:
                    print('套接字無連接')


class client(network):
    def start(self):
        print('it is client')
        self.client_data.set_IP(self.name, self.wan, self.lan, self.port)
        self.socket.settimeout(10)
        target = self.get_target(self.data, self.room)
        while True:
            try:
                self.socket.connect(target)
                print('已連接'+str(target))
                self.client_data.clear(self.name)
                break
            except socket.timeout:
                target = self.get_target(self.data, self.room)
                print('嘗試連接到', target)
        self.receive(self.socket)

    def close(self):
        self.client_data.clear(self.name)
        self.send(self.name + '離開聊天室', 1)
        self.send('exit', 2)
        self.socket.close()
        super().close()

    def receive(self, sock):
        sock.settimeout(60)
        while True:
            result = super().receive(sock)
            if result == 'close':
                print('break')
                break
            elif result is not None:
                self.window.add_new(result)

    def send(self, s, mode=0, one=None):
        data = super().send(s, mode)
        try:
            self.socket.send(data)
        except OSError:
            print('發送錯誤：套接字無連線')
            self.socket.close()


def begin(window, info):
    data = sheet.GetIP('IP')
    addr = data.search(info[0])
    if addr is None:
        return server(window, info)
    else:
        return client(window, info)
