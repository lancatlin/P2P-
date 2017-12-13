from tkinter import *

def encode(s,x):
    code = s
    T_code = ''
    for i in code:
        T_code += chr(ord(i) - x)
    return T_code
class login:
    def __init__(self):
        self.start = False
        x = 10
        try:
            f = open('code.sc','r')
            self.code = encode(f.read(),x)
        except:
            self.start = True
    def wait_login(self):
        if self.start:
            return True
        _font = lambda b: ('微軟正黑體', b)
        self.window = Tk()
        self.window.geometry('300x100')
        self.window.title('login')
        Label(self.window,text='輸入密碼:',font=_font(10)).grid(column=0,padx=5,pady=15)
        self.entry = Entry(self.window,font=_font(10),width=20,show='*')
        self.entry.grid(column=1,row=0)
        self.entry.bind('<Return>',lambda x:self.get_login())
        self.var = StringVar()
        Label(self.window,textvariable=self.var,font=_font(10)).grid(row=1,columnspan=2)
        self.window.mainloop()
    def get_login(self):
        if self.entry.get() == self.code:
            self.var.set('登入成功!')
            self.start = True
            self.window.destroy()
        else:
            self.var.set('密碼錯誤，請再試一次')
            self.entry.delete(0,'end')
if __name__ == '__main__':
    boot = login()
    boot.wait_login()