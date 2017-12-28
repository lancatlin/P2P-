from oauth2client.service_account import ServiceAccountCredentials as SAC
import gspread,key

class GetIP:
    def __init__(self,sheet):
        k = key.key()
        k.read()
        scopes = ['https://spreadsheets.google.com/feeds']
        service = SAC.from_json_keyfile_name('key.json',scopes)
        gc = gspread.authorize(service)
        k.remove()
        self.sheet = gc.open(sheet).sheet1
        self.all = self.sheet.get_all_records()
    def search(self,name):
        all = self.get_all()
        for i in all:
            if i['Name'] == name:
                return i
        return None
    def set_IP(self,name,wan,lan,port):
        self.sheet.append_row([name,wan,lan,port])
        self.all = self.sheet.get_all_records()
        print(self.all)
    def clear(self,name):
        all = self.sheet.get_all_records()
        all_len = len(all)
        print('clear')
        for i in range(all_len):
            if all[i]['Name'] == name:
                self.sheet.delete_row(i+2)
                break
    def get_all(self):
        return self.sheet.get_all_records()
if __name__ == '__main__':
    test = GetIP('client')
    print(test.get_all())