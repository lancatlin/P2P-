#-*- coding: utf-8 -*-
from tkinter import *
import NetWork,threading

class window(Tk):
    def __init__(self):
        super().__init__()
        self.title('P2P Talking')
        self.geometry('350x700')
        rows = 1

        f1 = Frame(self)
        f1.grid(row=rows, columnspan=5, sticky=W, pady=8, padx=5)
        Label(f1, text='聊天室:', width=5).grid(row=rows, sticky=W)
        self.roomentry = Entry(f1, width=15)
        self.roomentry.grid(row=rows, column=1)
        rows += 1

        f2 = Frame(self)
        f2.grid(row=rows, columnspan=5, sticky=W, pady=8, padx=5)
        Label(f2, text='使用者名稱:', width=10).grid(row=rows, sticky=W, columnspan=2)
        self.nameentry = Entry(f2, width=10)
        self.nameentry.grid(row=rows, column=2)
        Button(f2, text='連接', width=5, command=lambda: self.setIp()).grid(row=rows, column=3)
        rows += 1

        Label(self, text='聊天內容:', width=8).grid(row=rows, columnspan=2, sticky=W)
        rows += 1

        self.talktext = Text(self, width=45, height=35)
        self.talktext.grid(row=rows, columnspan=5, padx=8)
        sb = Scrollbar(self)
        sb.grid(row=rows, column=4, sticky=E + W + S + N)
        self.talktext['yscrollcommand'] = sb.set
        sb['command'] = self.talktext.yview
        rows += 1

        inputf = Frame(self)
        inputf.grid(row=rows)
        Label(inputf, text='輸入:', width=5).grid(row=rows, sticky=W)
        self.inputentry = Entry(inputf, width=20)
        self.inputentry.grid(row=rows, column=1, columnspan=3, pady=5)
        self.inputentry.bind('<Return>', lambda x: self.enter())
        rows += 1

        self.info = StringVar()
        self.info.set('歡迎使用P2P')
        message = Label(self, textvariable=self.info, width=25)
        message.grid(row=rows, columnspan=5, sticky=N, pady=15)

        self.mainloop()
    def setIp(self):
        room = self.roomentry.get()
        self._print_('準備連接:'+room)
        self.net = NetWork.network(self)
        self.protocol("WM_DELETE_WINDOW", self.net.close)
        start = threading.Thread(target = self.net.start)
        start.setDaemon(True)
        start.start()
    def enter(self):
        self.net.user(self.inputentry.get())
        self.inputentry.delete(0,END)
    def _print_(self,s):
        print(s)
        self.info.set(s)
    def add_new(self,s):
        self.talktext.insert(END, '\n' + s)
        self.talktext.see(END)
        print(s)

window()
