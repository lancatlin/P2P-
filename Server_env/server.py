from oauth2client.service_account import ServiceAccountCredentials as SAC
import gspread

scopes = ['https://spreadsheets.google.com/feeds']
service = SAC.from_json_keyfile_name('P2P talking-041270e8f646.json',scopes)
gc = gspread.authorize(service)
sheet = gc.open('IP').sheet1
print(sheet.get_all_records())