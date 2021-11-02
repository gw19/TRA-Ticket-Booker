# TRA-Ticket-Booker
## 台灣鐵路訂票應用程式（練習用）（已不適用新版臺鐵訂票系統，且不再更新）
（已不適用新版臺鐵訂票系統，且不再更新）這是一個練習用 Python 寫的小程式，僅僅算是初學者練習的過程。開啟後在界面中輸入身份證字號並選擇搭乘資訊，訂票後會出現認證碼，輸入完畢按下確認後顯示訂票結果。</br></br>
主要是想利用 Python + Selenium + PyQt4 練習實作一些小程式，可練習到的技巧範圍包括<strong>網路爬蟲</strong>、<strong>網站測試</strong>、<strong>網頁自動化操作</strong>、<strong>GUI設計</strong>等等。因為沒有很多編程實戰經驗，再次強調此程式碼的架構與邏輯僅僅算是初學者練習的過程，如果您覺得有需要改進的或是任何建議，期望您有空時能夠來信指正，我會非常感謝您！</br></br>Email：imgw19@gmail.com
### 需要用到的程式語言、套件與其版本：
* Python >= 3.4
* Selenium
* PhantomJS
* PyQt4
* PIL
* datetime
* json
<br>
註：需要自行下載 PhantomJS 這個 headless browser，然後與主程式放在同一個資料夾即可（不需要先啟動它），它能讓您執行訂票程式時在背景靜靜地啟動瀏覽器而不會開啟視窗。可至官網下載：http://phantomjs.org/

### 應用程式功能展示：

1. <strong>訂票成功</strong><br><br>
 ![ticket_successful](https://cloud.githubusercontent.com/assets/24193072/25806338/6b5c4960-3435-11e7-9bdc-c3f3b6c1e24d.gif)<br><br>
 
2. <strong>票已售完</strong><br><br>
 ![ticket_sold_out](https://cloud.githubusercontent.com/assets/24193072/25806374/87de7ae0-3435-11e7-9005-4c42272cb924.gif)<br><br>

3. <strong>認證碼輸入錯誤</strong><br><br>
 ![auth_num_error](https://cloud.githubusercontent.com/assets/24193072/25806467/dc07f416-3435-11e7-8c9a-8ed3ca3596f9.gif)<br><br>
 
4. <strong>身份證字號輸入錯誤</strong><br><br>
 ![id_error](https://cloud.githubusercontent.com/assets/24193072/25806416/a8ecc9bc-3435-11e7-82f3-c38e16c03293.gif)<br><br>
