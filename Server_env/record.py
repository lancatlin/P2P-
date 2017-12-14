import os
class Record:
    def __init__(self,window):
        self.window = window
    def find(self,room):
        self.room = 'saves/' + room + '.txt'
        try:
            file = open(self.room,'r')
            self.window.talktext.insert('end',file.read())
        except:
            pass
    def write(self):
        string = self.window.talktext.get(1.0,'end')
        with open(self.room,'w') as file:
            file.write(string)