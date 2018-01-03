#-*- coding: utf-8 -*-
from tkinter import *
import sound
import queue
from user import record


class window(Tk):
    def __init__(self, setting):
        super().__init__()
        self.title('P2P Talking')
        self.geometry('350x700')
        self.sound = sound.player()
        rows = 1
        
        ft = lambda s:('微軟正黑體', s)   #設定字體，傳入size，回傳一個tuple
        f1 = Frame(self)
        f1.grid(row=rows, sticky=W, padx=10, pady=5)
        Label(f1, text='聊天室:  ', font=ft(15)).grid(row=0, sticky=W)
        Label(f1, text=setting['room'], font=ft(15)).grid(row=0, column=1, sticky=W)

        rows += 1
        f2 = Frame(self)
        f2.grid(row=rows, sticky=W, padx=10, pady=5)
        Label(f2, text='使用者:  ', font=ft(15)).grid(row=0, sticky=W)
        Label(f2, text=setting['name'], font = ft(15)).grid(row=0, column=1, sticky=W)
        rows += 1

        self.talktext = Text(self, width=35, height=20, font=ft(12))
        self.talktext.grid(row=rows, columnspan=5, padx=8)
        sb = Scrollbar(self, width=20)      #滾輪設定
        sb.grid(row=rows, column=4, sticky=E + S + N)
        self.talktext['yscrollcommand'] = sb.set
        sb['command'] = self.talktext.yview
        self.record = record.Record(self)
        self.record.find(setting['room'])
        rows += 1

        inputf = Frame(self)
        inputf.grid(row=rows)
        Label(inputf, text='輸入:', width=5, font=ft).grid(row=rows, sticky=W)
        self.inputentry = Entry(inputf, width=20, font=ft)
        self.inputentry.grid(row=rows, column=1, columnspan=3, pady=5)
        self.inputentry.bind('<Return>', lambda x: self.enter())      #將enter鍵綁定到enter函數
        rows += 1

        self.info = StringVar()         #信息列的stringvar
        self.info.set('歡迎使用P2P')
        #Label(self, textvariable=self.info, width=25, font=ft(20)).grid(row=rows, columnspan=5, sticky=N, pady=15)

    def setIp(self, n):                  #設定self.net，將離開的函數指派給net.close
        self.net = n
        self.protocol("WM_DELETE_WINDOW", self.close)

    def enter(self):
        self.net.send(self.inputentry.get())
        self.inputentry.delete(0, END)

    def close(self):
        self.net.close()
        self.destroy()

    def _print_(self, s):
        print(s)
        self.info.set(s)

    def add_new(self):
        try:
            s = self.net.to_print.get(False)
            if s[0] == '@':
                s = s[1::]
            self.talktext.insert(END, '\n' + s)
            self.talktext.see(END)
            print(s)
            #self.record.write()    先不要寫紀錄
        except queue.Empty:
            pass

    def mainloop(self, n=0):
        while True:
            self.add_new()
            super().update_idletasks()
            super().update()
