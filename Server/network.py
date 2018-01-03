import socket
import select
import queue
import re
import json


class ServerNet:
    def __init__(self, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        setting = json.load(open('/home/lancat/文件/P2P-/setting.json', 'r'))
        address = (setting['ip'], setting['port'])
        self.socket.bind(address)
        self.socket.listen(5)
        self.ip_list = {}
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
                            try:
                                info = self.ip_list[room]
                                self.send(s, 'room:'+','.join([info['wan'], info['lan'], info['port']]))
                            except KeyError:
                                self.send(s, 'None')
                        #如果對方要設定
                        elif mode == 'set':
                            print('server:set')
                            info = re.match(
                                '(?P<mode>[^:,]+):(?P<name>[^:,]+),(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)',
                                data).groupdict()
                            print(info)
                            self.ip_list[info['name']] = {
                                'sock':s,
                                'wan':info['wan'],
                                'lan':info['lan'],
                                'port':info['port']
                            }
                            self.send(s, 'set down')
                        #如果使用者請求連結到某個server
                        elif mode == 'connect':
                            info = re.match(
                                '(?P<mode>[^:,]+):(?P<name>[^:,]+),(?P<wan>[^:,]+),(?P<lan>[^:,]+),(?P<port>[^:,]+)',
                                data).groupdict()
                            print('connect to %s' % info['name'])
                            try:
                                target = self.ip_list[info['name']]['sock']
                                ms = 'connect:'+','.join([info['wan'], info['lan'], info['port']])
                                self.send(target, ms)
                                s.send('down')
                            except KeyError:
                                self.send(s, 'error')
                                print('error: 沒有此聊天室')
                        elif mode == 'del':
                            info = data.split(':')[1]
                            self.ip_list.pop(info, None)
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
    server = ServerNet(55559)
    server.start()