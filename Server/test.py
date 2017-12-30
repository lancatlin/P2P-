from user import sheet
import socket
import network
from multiprocessing import Process


class test:
    def test_sheet(self,s):
        ip_sheet = sheet.GetIP(s)
        ip_sheet.set_IP('test', '0.0.0.0', '192.168.1.255', 12345)
        i = ip_sheet.search('test')
        if i is None:
            return '無法查找到test'
        elif i not in ip_sheet.get_all():
            return 'get_all 不符合結果'
        ip_sheet.clear('test')
        i = ip_sheet.search('test')
        if i is not None:
            return '刪除失敗'
        return '測試成功'

    def test_server(self):
        port = 44458
        server = network.ServerNet(port)
        Process(target=server.start).start()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(('127.0.0.1', port))
        data = s.recv(1024)
        print(data)
        s.send('room:room'.encode())
        data = s.recv(1024)
        print(data)
        s.send('set:room,0.0.0.0,192.168.1.1,12345'.encode())
        data = s.recv(1024)
        print(data)
        s.send('room:room'.encode())
        print(s.recv(1024))
        s.close()


t = test()
t.test_server()
