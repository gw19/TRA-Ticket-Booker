# TRA-Ticket-Booker
## 台灣鐵路訂票應用程式
這是一個練習用 Python 寫的小作品，開啟後在界面中輸入身份證字號並選擇搭乘資訊，訂票後會出現認證碼，輸入完畢按下確認後顯示訂票結果。</br></br>
主要是想利用 Python + Selenium + PyQt4 練習實作一些小程式，可練習到的技巧範圍包括<strong>網路爬蟲</strong>、<strong>網站測試</strong>、<strong>網頁自動化操作</strong>、<strong>GUI設計</strong>等等。因為我並沒有很多編程實戰經驗，程式碼的架構與邏輯可能不是這麼專業，如果您覺得有需要改進的或是任何建議，期望您有空時能夠來信指正，我會非常感謝您！</br></br>Email：gw.chen19@gmail.com
### 需要用到的程式語言、套件與其版本：</br>
Python >= 3.4</br>
Selenium</br>
PhantomJS</br>
PyQt4</br>
PIL</br>
datetime</br>
json</br></br>
註：需要自行下載 PhantomJS 這個 headless browser，然後與主程式放在同一個資料夾即可（不需要先啟動它），它能讓您執行訂票程式時在背景靜靜地啟動瀏覽器而不會開啟視窗。可至官網下載：http://phantomjs.org/<br></br>
### 應用程式功能展示：

1. <strong>訂票成功</strong></br></br>
 ![image] (https://raw.githubusercontent.com/gw19/TRA-Ticket-Booker/master/screenshots/Ticket_Successful.gif)</br></br></br>
 
2. <strong>票已售完</strong></br></br>
 ![image] (https://github.com/gw19/TRA-Ticket-Booker/blob/master/screenshots/Ticket_Sold_Out.gif)</br></br></br>

3. <strong>認證碼輸入錯誤</strong></br></br>
 ![image] (https://github.com/gw19/TRA-Ticket-Booker/blob/master/screenshots/Auth_Num_Error.gif)</br></br></br>
 
4. <strong>身份證字號輸入錯誤</strong></br></br>
 ![image] (https://github.com/gw19/TRA-Ticket-Booker/blob/master/screenshots/ID_Error.gif)</br></br></br>
