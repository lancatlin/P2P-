import sheet
import network


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
            print(i)
            return '刪除失敗'
        return '測試成功'


t = test()
print(t.test_sheet('IP'))