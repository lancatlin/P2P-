# P2P聊天程式

這是一個基於Python3.5 的點對點聊天程式。   
使用者只要約定共同的聊天室名稱，即可彼此通訊。  
聊天紀錄只會存在使用者的電腦，不會在網路上留下紀錄。  
不需辦帳戶，任意設定使用者名稱，可多人聊天，可與外網的朋友聊天   

###使用說明：
1. 下載[程式壓縮檔](https://github.com/lancatlin/P2P-/raw/master/P2P%E8%81%8A%E5%A4%A9%E7%A8%8B%E5%BC%8F.zip "程式壓縮檔")，並解壓縮到任意目錄
2. 依照作業系統執行windows.exe或著linux
3. 進入程式介面，輸入連接到的聊天室名稱與使用者名稱（注意：進入聊天室後就不能改變使用者名稱），並按下『連接』
4. 等待程式連接，便可和聊天室裡的其他人聊天！

###程式原理   
使用socket模組進行UDP打洞 -->NetWork.py  
將使用者IP位址存放於Google線上試算表，使用oauth2client和gspread進行編輯 -->server.py  
使用tkinter製作使用者介面 -->window.py,start.py
