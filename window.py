from tkinter import *
import threading,tkmain,time,data

d = data.data()
def setIp():
    global d
    ip = str(ipentry.get())
    _print_('準備連接:'+ip)
    start = threading.Thread(target = tkmain.main,args=(ip,d))
    start.setDaemon(True)
    start.start()
def enter():
    tkmain.input = inputentry.get()
    inputentry.delete(0,END)
def _print_(s):
    global info
    print(s)
    info.set(s)
def port():
    global d
    while True:
        if d.port != portentry.get():
            try:
                d.port = int(portentry.get())
            except:
                pass
            portentry.delete(0,END)
            portentry.insert(0,d.port)
            time.sleep(2)
        time.sleep(1)
def waitprint():
    global info
    global d
    while True:
        if d.toprint != '':
            _print_(d.toprint)
            d.toprint = ''
        if d.totext != '' :
            talktext.insert(END,'\n'+d.totext)
            d.totext = ''
            talktext.see(END)
            print(d.totext)
        if d.name != nameentry.get():
            d.name = nameentry.get()
        time.sleep(0.05)
window = Tk()
window.title('P2P Talking')
window.geometry('350x650')

rows=1

f1 = Frame(window)
f1.grid(row=rows,columnspan=5,sticky=W,pady=8,padx=5)
Label(f1,text='Ip:',width=5).grid(row=rows,sticky=W)
ipentry = Entry(f1,width=10)
ipentry.grid(row=rows,column=1)
Label(f1,text='port:',width=5).grid(row=rows,column=2)
portentry = Entry(f1,width=5)
portentry.grid(row=rows,column=3)
rows+=1

f2 = Frame(window)
f2.grid(row=rows,columnspan=5,sticky=W,pady=8,padx=5)
Label(f2,text='使用者名稱:',width=10).grid(row=rows,sticky=W,columnspan=2)
nameentry = Entry(f2,width=10)
nameentry.grid(row=rows,column=2)
Button(f2,text='連接',width=5,command=lambda:setIp()).grid(row=rows,column=3)
rows+=1

Label(window,text='聊天內容:',width=8).grid(row=rows,columnspan=2,sticky=W)
rows+=1

talktext = Text(window,width=45,height=35)
talktext.grid(row=rows,columnspan=5,padx=8)
sb = Scrollbar(window)
sb.grid(row=rows,column=4,sticky=E+W+S+N)
talktext['yscrollcommand'] = sb.set
sb['command']=talktext.yview
rows+=1

inputf=Frame(window)
inputf.grid(row=rows)
Label(inputf,text='輸入:',width=5).grid(row=rows,sticky=W)
inputentry = Entry(inputf,width=20)
inputentry.grid(row=rows,column=1,columnspan=3,pady=5)
inputentry.bind('<Return>',lambda x:enter())
rows+=1

info = StringVar()
info.set('歡迎使用P2P')
message = Label(window,textvariable=info,width = 25)
message.grid(row=rows,columnspan=5,sticky=N,pady=15)
getprint = threading.Thread(target=waitprint,args=())
getprint.setDaemon(True)
getprint.start()
getport = threading.Thread(target=port,args=())
getport.setDaemon(True)
getport.start()
window.mainloop()