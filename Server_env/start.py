from tkinter import *
import window,NetWork,threading
class start(Tk):
    def __init__(self):
        super().__init__()
        self.title('P2P 聊天程式')
        self.geometry('400x200')

        rows = 0

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
        Button(f2, text='連接', width=5, command=lambda: self.begin()).grid(row=rows, column=3)
        rows += 1

        self.info = StringVar()
        self.info.set('歡迎使用P2P')
        Label(self, textvariable=self.info, width=25).grid(row=rows, columnspan=5, sticky=N, pady=15)

        self.mainloop()
    def begin(self):
        self.window = window.window()
        self.net = NetWork.network(self.window,self.nameentry.get(),self.roomentry.get())
        self.window.net = self.net
        self._print_('準備連接：'+self.roomentry.get()+'中...')
        self.net.start()
        start = threading.Thread(target=self.net.receive)
        start.setDaemon(True)
        start.start()
        self.window.mainloop()
    def _print_(self,s):
        print(s)
        self.info.set(s)
start()
