import socket
import select
import queue
import re


class ServerNet:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('127.0.0.1', port)
        self.socket.bind(address)
        self.socket.listen(5)
        self.ip_list = []
        self.inputs = [self.socket]
        self.outputs = []
        self.messange = {}

    def start(self):
        timeout = 5
        self.socket.settimeout(timeout)
        byte_long = 1024
        while True:
            read, write, error = select.select(self.inputs, self.outputs, self.inputs, timeout)
            # 如果啥都沒有
            if not (read or write or error):
                continue
            for s in read:
                # 如果socket是自己，代表有新連線
                if s is self.socket:
                    new, address = self.socket.accept()
                    print(address)
                    self.inputs.append(new)
                    self.messange[new] = queue.Queue()
                    self.send(new, 'get it')
                #從已知的連接發送過來，接收資料
                else:
                    data = s.recv(byte_long)
                    #如果有訊息
                    if data:
                        data = data.decode()
                        mode = re.match('[^:]+', data).group()
                        #對方要查詢room
                        if mode == 'room':
                            room = re.search('(?<=:).+', data).group()
                            print(room)
                            for i in self.ip_list:
                                if i['name'] == room:
                                    self.send(s,','.join([i['wan'], i['lan'], i['port']]))
                                    break
                            else:
                                self.send(s,'None')
                        #如果對方要設定
                        elif mode == 'set':
                            print('server:set')
                            info = re.match(
                                '(?P<mode>[^:,]+):(?P<name>[^:,]+),(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)',
                                data)
                            new_one = info.groupdict()
                            print(new_one)
                            self.ip_list.append(new_one)
                            self.send(s, 'set down')
                        elif mode == 'connect':
                            info = re.match(
                                '(?P<mode>[^:,]+):(?P<name>[^:,]+),(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)',
                                data).groupdict()
                            print('connect to %s' % info['name'])
                            for i in self.ip_list:
                                if i['name'] == room:
                                    self.send(s,','.join([i['wan'], i['lan'], i['port']]))
                                    break
                            else:
                                self.send(s,'None')

                    #沒訊息，關閉連接
                    else:
                        print('close')
                        self.inputs.remove(s)
                        s.close()
            for s in write:
                try:
                    msg = self.messange[s].get(False)
                except queue.Empty:
                    print('queue is empty')
                else:
                    s.send(msg.encode())
                self.outputs.remove(s)

    def recv(self,sock):
        data = sock.recv(1024)
        return data.decode()

    def send(self, sock, string):
        self.outputs.append(sock)
        self.messange[sock].put(string)


if __name__ == '__main__':
    server = ServerNet()
    server.start()