from oauth2client.service_account import ServiceAccountCredentials as SAC
import gspread

class GetIP:
    def __init__(self):
        scopes = ['https://spreadsheets.google.com/feeds']
        service = SAC.from_json_keyfile_name('P2P talking-041270e8f646.json',scopes)
        gc = gspread.authorize(service)
        self.sheet = gc.open('IP').sheet1
        self.all = self.sheet.get_all_records()
    def search(self,name):
        all = self.all
        for i in all:
            if i['Name'] == name:
                return (i['IP'],i['port'])
        return None
    def set_IP(self,name,ip,port):
        self.sheet.append_row([name,ip,port])
        self.all = self.sheet.get_all_records()
        print(self.all)
    def clear(self,name):
        all = self.sheet.get_all_records()
        all_len = len(all)
        print(all,all_len,name)
        for i in range(all_len):
            if all[i]['Name'] == name:
                self.sheet.delete_row(i+2)
                print(i+1)
                break
if __name__ == '__main__':
    test = GetIP()
    t = test.search('lancat')
    test.set_IP('try4','26',2000)
    test.clear('try4')
    print(test.all)