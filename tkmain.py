import socket,_thread,time,sys

def main(ip,d):
    def server(ADDR,ip):
        nonlocal mode,data
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.bind(ADDR)
        print(ADDR)
        addr = ip,d.port
        _thread.start_new_thread(test,(s ,addr,ADDR))
        data , addr = s.recvfrom(1024)
        mode = False
        _print('已連接')
        print(data)
        s.sendto('ok'.encode('UTF-8'),addr)
        s.sendto(data,(addr[0],d.port))
        _thread.start_new_thread(user,(s ,addr))
        while True:
            data,addr = s.recvfrom(1024)
            data = data.decode('UTF-8')
            d.totext = data
            time.sleep(0.5)
        s.close
    def user(s,addr):
        global input
        while True:
            while input == '':
                time.sleep(0.01)
            data=input
            now = time.strftime("[%H-%M]")
            data=now+data
            d.totext = '<You>'+data
            if data == 'end':
                break
            data = '<'+d.name+'>'+data
            data=data.encode('UTF-8')
            s.sendto(data,addr)
            input = ''
        s.close
        sys.exit()
    def test(s,addr,ADDR):
        nonlocal mode
        nonlocal data
        if mode:
            print('準備連接'+str(addr))
            x = 0
            while mode and x <= 1000:
                s.sendto(data,addr)
                time.sleep(0.2)
                x+=1
            if mode:
                _print('連線失敗')
                sys.exit()
            else:
                _print('已連接')
    def _print(s):
        string = str(s)
        d.toprint = string
    HOST,PORT = socket.gethostname(),d.port
    HOST = socket.gethostbyname(HOST)
    ADDR = (HOST,PORT)
    mode = True
    data = ('test,'+'lancat,'+str(ADDR[0])+','+str(ADDR[1])).encode()
    time.sleep(0.5)
    server(ADDR,ip)
input=''
if __name__ == '__main__':
    main(input('輸入ip:'))