# -*- coding: utf-8 -*-
# Author: gw19
# Copyright (c) 2017 GW19
# -----------------------------------#
#

import json
import sys
from datetime import datetime, timedelta
from PIL import Image
from PyQt4 import QtCore, QtGui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

QtCore.QTextCodec.setCodecForTr(
    QtCore.QTextCodec.codecForName('utf8')
)

class TraTicketBooker(QtGui.QDialog):
    # The GUI of TRA Ticket Booker.
    
    def __init__(self, parent=None):
        super(TraTicketBooker, self).__init__(parent)
        self.setWindowTitle('TRA Ticket Booker')
        self.setWindowIcon(QtGui.QIcon('Icons\\rocket_ship.png'))
        self.font_size = 12
        font_label_standard = QtGui.QFont('微軟正黑體', self.font_size)
        QtGui.QApplication.setFont(font_label_standard)
        QtGui.QApplication.setApplicationName('TRA Ticket Booker')
        QtGui.QApplication.setApplicationVersion('1.0')
        self.setWindowFlags(
            QtCore.Qt.WindowCloseButtonHint | 
            QtCore.Qt.WindowMinimizeButtonHint
        )
        QtGui.QApplication.setStyle('cleanlooks')
        
        # Set and Show Splash Screen.
        pic_splash = QtGui.QPixmap(
            'Icons\\splash_screen.png'
        )
        splash_screen = QtGui.QSplashScreen(
            pic_splash, 
            QtCore.Qt.WindowStaysOnTopHint
        )
        splash_font = splash_screen.font()
        splash_font.setFamily('華康中圓體')
        splash_font.setPixelSize(23)
        splash_screen.setFont(splash_font)
        splash_screen.show()
        processing_message = '正在初始化應用程式...'
        splash_screen.showMessage(
            splash_screen.tr(processing_message),
            QtCore.Qt.AlignBottom |
            QtCore.Qt.AlignHCenter|
            QtCore.Qt.AlignAbsolute,
            QtCore.Qt.black
        )
        
        # Get the List of ComboBoxes.
        self.station_list = self.get_station_list()
        if self.station_list == -1:
            QtGui.QMessageBox.critical(
                self, "Error", self.tr(
                    '車站資料讀取失敗，' + 
                    '請檢查檔案「station.json」' + 
                    '是否存在並與主程式置放於' + 
                    '同一個資料夾中。'
                )
            )
            sys.exit()

        # Set the Font of Labels.            
        self.font_label_go_back = QtGui.QFont(
            '微軟正黑體', self.font_size
        )
        self.font_label_go_back.setBold(True)

        # Get the Data of TRA.
        self.date_list = self.get_date_list()
        self.time_list = self.get_time_list()
        self.train_list = self.get_train_list()
        self.ticket_list = self.get_ticket_list()
        
        self.input_data = {}
        self.select_data = {}
        self.select_data_value = {}
        self.input_number = {}
        self.re_order = 0
        
        # Start UP the Selenium + PhantomJS Driver.
        self.driver = self.start_up_driver()
        
        # Close Splash Screen 
        # After Completely Initialized.
        splash_screen.close()
        
        # Setup the Initial Layouts.
        self.set_layout()
        
    def set_layout(self):
        # Setup the Initial Layouts.
        # -------------------------------------------------------------------#
        # ----------------------- Set the layout "ID". ----------------------#
        self.layout_id_label = QtGui.QGridLayout()
        self.layout_id_input = QtGui.QGridLayout()
        self.layout_id_ps = QtGui.QGridLayout()
        
        self.label_id = QtGui.QLabel('身份證字號')
        self.layout_id_label.addWidget(
            self.label_id, 0, 0
        )
        self.line_edit_id = QtGui.QLineEdit()
        self.layout_id_input.addWidget(
            self.line_edit_id, 0, 0
        )
        self.line_edit_id.setMaxLength(10) # Max Length of ID
        
        # Connecting to the Button-Event while Press "Enter".
        self.line_edit_id.returnPressed.connect(
            self.button_book_go_back_event
        )
        self.label_ps = QtGui.QLabel(
            'Enter＝訂來回票'
        )
        self.label_ps.setFont(
            QtGui.QFont('微軟正黑體', 11, italic=True)
        )
        self.layout_id_ps.addWidget(
            self.label_ps, 0, 0, 1, 2
        )
        
        # -------------------------------------------------------------------#
        # ---------------- Set the layout "Label, Go/Single". ---------------#
        self.layout_combo_label = QtGui.QGridLayout()
        self.layout_go_title = QtGui.QGridLayout()
        self.layout_go_combo = QtGui.QGridLayout()
        self.layout_button_book = QtGui.QGridLayout()
        
        self.title_go = QtGui.QLabel('【 出發/單程 】')
        self.layout_go_title.addWidget(
            self.title_go, 0, 0
        )
        self.title_go.setFont(
            self.font_label_go_back
        )
        # Align to Center of Label.
        self.title_go.setAlignment(
            QtCore.Qt.AlignCenter | 
            QtCore.Qt.AlignVCenter
        )
        
        # Station - From
        self.label_station_from = QtGui.QLabel('起站')
        self.layout_combo_label.addWidget(
            self.label_station_from, 1, 0
        )
        self.combo_box_station_go_from = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_station_go_from, 1, 0
        )
        self.combo_box_station_go_from.addItems(
            self.station_list
        )
        # (default 108-中壢)
        self.combo_box_station_go_from.setCurrentIndex(15)
        
        self.combo_box_station_go_from.activated.connect(
            self.cb_stn_from_event
        )
        
        # Station - End
        self.label_station_end = QtGui.QLabel('到站')
        self.layout_combo_label.addWidget(
            self.label_station_end, 2, 0
        )
        self.combo_box_station_go_end = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_station_go_end, 2, 0
        )
        self.combo_box_station_go_end.addItems(
            self.station_list
        )
        # (default 158-斗六)
        self.combo_box_station_go_end.setCurrentIndex(57)
        
        self.combo_box_station_go_end.activated.connect(
            self.cb_stn_end_event
        )
        
        # Date
        self.label_date = QtGui.QLabel('日期')
        self.layout_combo_label.addWidget(
            self.label_date, 3, 0
        )
        self.combo_box_date_go = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_date_go, 3, 0
        )
        self.combo_box_date_go.addItems(self.date_list)
        self.combo_box_date_go.setCurrentIndex(3)
        self.combo_box_date_go.activated.connect(
            self.cb_go_date_event
        )
        
        # Time - From
        self.label_time_from = QtGui.QLabel('起始時間')
        self.layout_combo_label.addWidget(
            self.label_time_from, 4, 0
        )
        self.combo_box_time_go_from = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_time_go_from, 4, 0
        )
        self.combo_box_time_go_from.addItems(self.time_list)
        self.combo_box_time_go_from.setCurrentIndex(17)
        self.combo_box_time_go_from.activated.connect(
            self.cb_go_time_event
        )
        
        # Time - End
        self.label_time_end = QtGui.QLabel('截止時間')
        self.layout_combo_label.addWidget(
            self.label_time_end, 5, 0
        )
        self.combo_box_time_go_end = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_time_go_end, 5, 0
        )
        self.combo_box_time_go_end.addItems(
            self.time_list[
                self.combo_box_time_go_from.currentIndex()+1:
            ]
        )
        self.combo_box_time_go_end.setCurrentIndex(1)
        
        # Train Type
        self.label_train = QtGui.QLabel('車種')
        self.layout_combo_label.addWidget(
            self.label_train, 6, 0
        )
        self.combo_box_train_go = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_train_go, 6, 0
        )
        self.combo_box_train_go.addItems(self.train_list)
        self.combo_box_train_go.setCurrentIndex(1)
        
        # Ticket - Numbers
        self.label_ticket = QtGui.QLabel('訂票張數')
        self.layout_combo_label.addWidget(
            self.label_ticket, 7, 0
        )
        self.combo_box_ticket_go = QtGui.QComboBox()
        self.layout_go_combo.addWidget(
            self.combo_box_ticket_go, 7, 0
        )
        self.combo_box_ticket_go.addItems(self.ticket_list)
        
        # Button - Buy Single Ticket
        self.button_book_single = QtGui.QPushButton(
            '\n訂單程票\n'
        )
        self.layout_button_book.addWidget(
            self.button_book_single, 0, 0
        )
        icon_single = QtGui.QIcon('Icons\\single_arrow.png')
        self.button_book_single.setIcon(icon_single)
        self.connect(
            self.button_book_single, 
            QtCore.SIGNAL('clicked()'), 
            self.button_book_single_event
        )
        self.button_book_single.setAutoDefault(False)
        
        # -------------------------------------------------------------------#
        # ---------------------- Set the layout "Back". ---------------------#
        self.layout_back_title = QtGui.QGridLayout()
        self.layout_back_combo = QtGui.QGridLayout()
        
        self.title_back = QtGui.QLabel('【 回程 】')
        self.layout_back_title.addWidget(
            self.title_back, 0, 0
        )
        self.title_back.setFont(
            self.font_label_go_back
        )
        # Align to Center of Label.
        self.title_back.setAlignment(
            QtCore.Qt.AlignCenter | 
            QtCore.Qt.AlignVCenter
        )
        
        # Station - From
        self.combo_box_station_back_from = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_station_back_from, 1, 0
        )
        self.combo_box_station_back_from.addItems(
            self.station_list
        )
        # (default 158-斗六)
        self.combo_box_station_back_from.setCurrentIndex(
            self.combo_box_station_go_end.currentIndex()
        )
        self.combo_box_station_back_from.setDisabled(True)
        
        # Station - End
        self.combo_box_station_back_end = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_station_back_end, 2, 0
        )
        self.combo_box_station_back_end.addItems(
            self.station_list
        )
        # (default 108-中壢)
        self.combo_box_station_back_end.setCurrentIndex(
            self.combo_box_station_go_from.currentIndex()
        )
        self.combo_box_station_back_end.setDisabled(True)
        
        # Date
        self.combo_box_date_back = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_date_back, 3, 0
        )
        self.combo_box_date_back.addItems(self.date_list)
        self.combo_box_date_back.setCurrentIndex(5)
        
        # Time - From
        self.combo_box_time_back_from = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_time_back_from, 4, 0
        )
        self.combo_box_time_back_from.addItems(
            self.time_list
        )
        self.combo_box_time_back_from.setCurrentIndex(17)
        self.combo_box_time_back_from.activated.connect(
            self.cb_back_time_event
        )
        
        # Time - End
        self.combo_box_time_back_end = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_time_back_end, 5, 0
        )
        self.combo_box_time_back_end.addItems(
            self.time_list[
                self.combo_box_time_back_from.currentIndex()+1:
            ]
        )
        self.combo_box_time_back_end.setCurrentIndex(1)
        
        # Train - Type
        self.combo_box_train_back = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_train_back, 6, 0
        )
        self.combo_box_train_back.addItems(
            self.train_list
        )
        self.combo_box_train_back.setCurrentIndex(1)
        
        # Ticket - Numbers
        self.combo_box_ticket_back = QtGui.QComboBox()
        self.layout_back_combo.addWidget(
            self.combo_box_ticket_back, 7, 0
        )
        self.combo_box_ticket_back.addItems(
            self.ticket_list
        )
        
        # Button - Buy Go-Back Ticket
        self.button_book_go_back = QtGui.QPushButton(
            '\n訂來回票\n'
        )
        self.layout_button_book.addWidget(
            self.button_book_go_back, 0, 1
        )
        icon_go_back = QtGui.QIcon(
            'Icons\\go_return_arrow.png'
        )
        self.button_book_go_back.setIcon(icon_go_back)
        self.connect(
            self.button_book_go_back, 
            QtCore.SIGNAL('clicked()'), 
            self.button_book_go_back_event
        )
        self.button_book_go_back.setAutoDefault(False)
        
        # -------------------------------------------------------------------#
        # -----------------Set the layout "Input and Result". ---------------#
        ## Show Image
        self.layout_input_result = QtGui.QGridLayout()
        self.label_auth_num = QtGui.QLabel(
            '【 認證碼顯示/輸入 】'
        )
        self.layout_input_result.addWidget(
            self.label_auth_num, 0, 0, 1, 2
        )
        self.label_auth_num.setFont(
            self.font_label_go_back
        )
        self.label_auth_num.setAlignment( # Align to Center
            QtCore.Qt.AlignCenter | 
            QtCore.Qt.AlignVCenter
        )
        self.pic_box = QtGui.QLabel()
        self.layout_input_result.addWidget(
            self.pic_box, 1, 0, 3, 2
        )
        self.pic_box.setStyleSheet(
            'border:1px solid rgb(0, 0, 0)'
        )
        
        ## Confirm and Send the Authent-Number.
        self.line_edit_num = QtGui.QLineEdit()
        self.layout_input_result.addWidget(
            self.line_edit_num, 4, 0
        )
        self.line_edit_num.setMaxLength(6) # Max Length of ID
        
        # Connecting to the Button-Event while Press "Enter".
        self.line_edit_num.returnPressed.connect(
            self.button_input_num_event
        )
        
        self.button_input_num = QtGui.QPushButton('確認')
        self.layout_input_result.addWidget(
            self.button_input_num, 4, 1
        )
        icon_input_num = QtGui.QIcon('Icons\\confirm.png')
        self.button_input_num.setIcon(icon_input_num)
        self.connect(
            self.button_input_num, 
            QtCore.SIGNAL('clicked()'), 
            self.button_input_num_event
        )
        self.button_input_num.setAutoDefault(False)
        
        ## Show Results
        self.label_result = QtGui.QLabel(
            '【 訂票結果 】'
        )
        self.layout_input_result.addWidget(
            self.label_result, 5, 0, 1, 2
        )
        self.label_result.setFont(
            self.font_label_go_back
        )
        # Align to Center of Label.
        self.label_result.setAlignment(
            QtCore.Qt.AlignCenter | 
            QtCore.Qt.AlignVCenter
        )
        #
        self.label_show_result = QtGui.QLabel()
        self.layout_input_result.addWidget(
            self.label_show_result, 6, 0, 8, 2
        )
        self.label_show_result.setStyleSheet(
            'border:1px solid rgb(0, 0, 0)'
        )
        self.label_show_result.setAlignment(
            QtCore.Qt.AlignTop | 
            QtCore.Qt.AlignLeft
        )
        self.label_show_result.setWordWrap(True)
        
        # -------------------------------------------------------------------#
        # ---------------- Make Layouts in the Main Window. -----------------#
        # ---------------- And Set the Location of Layouts. -----------------#
        self.layout_main = QtGui.QGridLayout(self)
        self.layout_main.setSpacing(10)
        
        # Layout ID Block
        self.layout_main.addLayout(
            self.layout_id_label, 0, 0
        )
        self.layout_main.addLayout(
            self.layout_id_input, 0, 1
        )
        self.layout_main.addLayout(
            self.layout_id_ps, 0, 2, 1, 2
        )
        # Layout Go Title Block
        self.layout_main.addLayout(
            self.layout_go_title, 1, 1
        )
        # Layout Back Title Block
        self.layout_main.addLayout(
            self.layout_back_title, 1, 2
        )
        # Layout Go-Back Combobox Block
        self.layout_main.addLayout(
            self.layout_combo_label, 2, 0
        )
        self.layout_main.addLayout(
            self.layout_go_combo, 2, 1
        )
        self.layout_main.addLayout(
            self.layout_back_combo, 2, 2
        )
        # Layout Single / Go-Back Button Block
        self.layout_main.addLayout(
            self.layout_button_book, 3, 1, 1, 2
        )
        # Layout Result Block
        self.layout_main.addLayout(
            self.layout_input_result, 1, 3, 4, 1
        )
        
        self.layout_main.setSizeConstraint(
            QtGui.QLayout.SetFixedSize
        )
        
        # -------------------------------------------------------------------#
        # -------------------------- Set the Size. --------------------------#
        ## QWidget Size
        width_pic_box = self.pic_box.width()
        reduce_ratio = 0.32
        
        self.line_edit_id.setFixedWidth(
            width_pic_box * reduce_ratio * 0.6
        )
        self.pic_box.setFixedWidth(
            width_pic_box * reduce_ratio
        )
        self.line_edit_num.setFixedWidth(
            width_pic_box * reduce_ratio * 0.6
        )
        self.button_input_num.setFixedWidth(
            width_pic_box * reduce_ratio * 0.356
        )
        self.label_show_result.setFixedWidth(
            width_pic_box * reduce_ratio
        )
        
        ## Icons Size
        size_set = [3, 4, 2] # For Windows 7
        # size_set = [4, 5, 2.5] # For Windows 10 
        self.button_book_single.setIconSize(
            QtCore.QSize(
                self.font_size * size_set[0], 
                self.font_size * size_set[0]
            )
        )
        self.button_book_go_back.setIconSize(
            QtCore.QSize(
                self.font_size * size_set[1], 
                self.font_size * size_set[1]
            )
        )
        self.button_input_num.setIconSize(
           QtCore.QSize(
                self.font_size * size_set[2], 
                self.font_size * size_set[2]
            )
        )
        
        # ComboBox Style
        self.combo_box_station_go_from.setStyle(
            QtGui.QStyleFactory.create('plastique')
        )
        self.combo_box_station_go_end.setStyle(
            QtGui.QStyleFactory.create('plastique')
        )
        self.combo_box_station_back_from.setStyle(
            QtGui.QStyleFactory.create('plastique')
        )
        self.combo_box_station_back_end.setStyle(
            QtGui.QStyleFactory.create('plastique')
        )
        
    # -----------------------------------------------------------------------#
    # ----------------------------- GUI Events. -----------------------------#
    def start_up_driver(self):
        driver = webdriver.PhantomJS()
        return driver
        
    def get_station_list(self):
        try:
            with open('station.json', 'r', encoding='utf8') as f:
                sdata = json.loads(f.read())
                # Sort it by station numbers
                sdata_sorted = sorted(
                    sdata, key=lambda s: s['時刻表編號']
                )
                station_list = []
                for ii in range(len(sdata_sorted)):
                    station_list.append(
                        '%03d' % int(sdata_sorted[ii]['編號']) 
                      + '-' 
                      + sdata_sorted[ii]['站名']
                    )
                return station_list
                    
        except IOError as ioerr:
            print('File Error: ' + str(ioerr))
            return -1

    def get_date_list(self):
        date_list = []
        for ii in range(17):
            if datetime.today().time().hour < 23:
                local_time = datetime.today() + timedelta(ii)
            else:
                local_time = datetime.today() + timedelta(ii + 1)
            lt_year, lt_mon, lt_day, lt_hour, lt_min, lt_sec, \
            lt_wday, lt_yday, lt_isdst = local_time.timetuple()
            date_list.append(
                '%04d/%02d/%02d' 
                % (lt_year, lt_mon, lt_day)
            )
        return date_list

    def get_time_list(self):
        time_list = []
        for ii in range(24):
            time_list.append('%02d:%02d' % (ii, 00))
        return time_list

    def get_train_list(self):
        train_list = ['全部車種', '自強號', '莒光號', '復興號']
        return train_list
        
    def get_ticket_list(self):
        ticket_list = ['1', '2', '3', '4', '5', '6']
        return ticket_list        
    
    def cb_stn_from_event(self):
        self.combo_box_station_back_end.setCurrentIndex(
            self.combo_box_station_go_from.currentIndex()
        )
        
    def cb_stn_end_event(self):
        self.combo_box_station_back_from.setCurrentIndex(
            self.combo_box_station_go_end.currentIndex()
        )
        
    def cb_go_date_event(self):
        self.combo_box_date_back.clear()
        self.combo_box_date_back.addItems(
            self.date_list[
                self.combo_box_date_go.currentIndex():
            ]
        )
        self.combo_box_date_back.setCurrentIndex(0)
        
    def cb_go_time_event(self):
        self.combo_box_time_go_end.clear()
        self.combo_box_time_go_end.addItems(
            self.time_list[
                self.combo_box_time_go_from.currentIndex()+1:
            ]
        )
        self.combo_box_time_go_end.setCurrentIndex(1)
        
    def cb_back_time_event(self):
        self.combo_box_time_back_end.clear()
        self.combo_box_time_back_end.addItems(
            self.time_list[
                self.combo_box_time_back_from.currentIndex()+1:
            ]
        )
        self.combo_box_time_back_end.setCurrentIndex(1)
        
    def button_book_single_event(self):
        # While Pushed the Button "Buy Single Ticket".
        self.input_data.clear()
        self.select_data.clear()
        self.select_data_value.clear()
        
        self.input_data.update({
            'person_id': self.line_edit_id.text()
        })
        self.select_data.update({
            'from_station': 
                self.combo_box_station_go_from.currentText(),
            'to_station': 
                self.combo_box_station_go_end.currentText(),
            'getin_date': 
                self.combo_box_date_go.currentText(),
            'getin_start_dtime': 
                self.combo_box_time_go_from.currentText(),
            'getin_end_dtime': 
                self.combo_box_time_go_end.currentText(),
            'train_type': 
                self.combo_box_train_go.currentText(),
            'order_qty_str': 
                self.combo_box_ticket_go.currentText(),
        })
        
        # Deal with the Values in order to Input Data in TRA.
        self.station_go_from_value = \
            self.combo_box_station_go_from.currentText().split('-')[0]
        self.station_go_end_value = \
            self.combo_box_station_go_end.currentText().split('-')[0]
            
        self.date_go_value = \
            self.combo_box_date_go.currentText() \
            + '-' + '%02d' % (
                self.date_list.index(
                    self.combo_box_date_go.currentText()
                )
            )
        
        if self.combo_box_train_go.currentIndex() == 0:
            self.train_go_value = '*4'
        else:
            self.train_go_value = \
                '*' + str(self.combo_box_train_go.currentIndex())
                
        self.select_data_value.update({
            'from_station': 
                self.station_go_from_value,
            'to_station': 
                self.station_go_end_value,
            'getin_date': 
                self.date_go_value,
            'getin_start_dtime': 
                self.combo_box_time_go_from.currentText(),
            'getin_end_dtime': 
                self.combo_box_time_go_end.currentText(),
            'train_type': 
                self.train_go_value,
            'order_qty_str': 
                self.combo_box_ticket_go.currentText(),
        })
        
        self.book_type = 1
        self.run_main_process()
        
    def button_book_go_back_event(self):
        # While Pushed the Button "Buy Go-Back Ticket".
        self.input_data.clear()
        self.select_data.clear()
        self.select_data_value.clear()

        self.input_data.update({
            'person_id': self.line_edit_id.text()
        })
        self.select_data.update({
            'from_station': 
                self.combo_box_station_go_from.currentText(),
            'to_station': 
                self.combo_box_station_go_end.currentText(),
            'getin_date': 
                self.combo_box_date_go.currentText(),
            'getin_date2': 
                self.combo_box_date_back.currentText(),
            'getin_start_dtime': 
                self.combo_box_time_go_from.currentText(),
            'getin_end_dtime': 
                self.combo_box_time_go_end.currentText(),
            'getin_start_dtime2': 
                self.combo_box_time_back_from.currentText(),
            'getin_end_dtime2': 
                self.combo_box_time_back_end.currentText(),
            'train_type': 
                self.combo_box_train_go.currentText(),
            'train_type2': 
                self.combo_box_train_back.currentText(),
            'order_qty_str': 
                self.combo_box_ticket_go.currentText(),
            'order_qty_str2': 
                self.combo_box_ticket_back.currentText()
        })
        
        # Deal with the Values in order to Input Data in TRA.
        self.station_go_from_value = \
            self.combo_box_station_go_from.currentText().split('-')[0]
        self.station_go_end_value = \
            self.combo_box_station_go_end.currentText().split('-')[0]
            
        self.date_go_value = \
            self.combo_box_date_go.currentText() \
            + '-' + '%02d' % (
                self.date_list.index(
                    self.combo_box_date_go.currentText()
                )
            )
        self.date_back_value = \
            self.combo_box_date_back.currentText() \
            + '-' + '%02d' % (
                self.date_list.index(
                    self.combo_box_date_back.currentText()
                )
            )
        
        if self.combo_box_train_go.currentIndex() == 0:
            self.train_go_value = '*4'
        else:
            self.train_go_value = \
                '*' + str(self.combo_box_train_go.currentIndex())
        if self.combo_box_train_back.currentIndex() == 0:
            self.train_back_value = '*4'
        else:
            self.train_back_value = \
                '*' + str(self.combo_box_train_back.currentIndex())
                
        self.select_data_value.update({
            'from_station': 
                self.station_go_from_value,
            'to_station': 
                self.station_go_end_value,
            'getin_date': 
                self.date_go_value,
            'getin_date2': 
                self.date_back_value,
            'getin_start_dtime': 
                self.combo_box_time_go_from.currentText(),
            'getin_end_dtime': 
                self.combo_box_time_go_end.currentText(),
            'getin_start_dtime2': 
                self.combo_box_time_back_from.currentText(),
            'getin_end_dtime2': 
                self.combo_box_time_back_end.currentText(),
            'train_type': 
                self.train_go_value,
            'train_type2': 
                self.train_back_value,
            'order_qty_str': 
                self.combo_box_ticket_go.currentText(),
            'order_qty_str2': 
                self.combo_box_ticket_back.currentText()
        })
        
        self.book_type = 2
        self.run_main_process()
    
    def button_input_num_event(self):
        # Get the Inputed Authent-Number
        self.input_number.clear()
        self.input_number = {
            'randInput': self.line_edit_num.text()
        }
        self.fill_input(self.input_number)
        # Submit Aythentication Number, 
        # Show Final Results
        self.submit_auth_number()


    # -----------------------------------------------------------------------#
    # --------------- MAIN PROCESS of Pushing Button "Booking" ------------- #
    def run_main_process(self):
        # Run the Main Process while Pushed the Button.
        # Connect to TRA Webpage
        self.connect_to_webpage()
        
        # -- Take Inputed Values (driver.fill) -- #
        self.fill_input(self.input_data)
        self.fill_select()
        
        # -- Submit User Data -- #
        self.submit_user_data()
        
        # -- Save and Open Authent-Number Image -- #
        self.save_and_open_image()  
        
    def connect_to_webpage(self):
        url_target_sg = 'http://railway1.hinet.net/csearch.htm'
        url_target_gb = 'http://railway.hinet.net/ctkind2.htm'
        self.driver.delete_all_cookies()
        
        wait = WebDriverWait(self.driver, timeout=6)
        try:
            # Booking Single Ticket.
            if self.book_type == 1:
                self.driver.get(url_target_sg)
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, 'button')
                    )
                )
            # Booking Go-Back Ticket.
            elif self.book_type == 2:
                self.driver.get(url_target_gb)
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, 'button')
                    )
                )
        except:
            self.label_show_result.setText(
                '【連線逾時或是網路不穩定】\n' + 
                '【請檢查網路環境以及是否為尖峰時段。】'
            )
        
    def fill_input(self, data_for_input):
        # Fill the data inputed by user into the form on the website.
        input_data_key = list(data_for_input)
        for ii in input_data_key:
            self.driver.execute_script(
                "document.querySelector('input[name=" + 
                '"' + ii + '"' + "]').value = " + "'" + 
                data_for_input[ii] + "'"
            )
            
    def fill_select(self):
        # Fill the data selected by user into the form on the website.
        select_data_key = list(self.select_data_value)
        for ii in select_data_key:
            self.driver.execute_script(
                "document.querySelector('select[name=" + 
                '"' + ii + '"' + "]').value = " + "'" + 
                self.select_data_value[ii] + "'"
            )
            
    def submit_user_data(self):
        # Submit to Authent-Number Page (press button).
        wait = WebDriverWait(self.driver, timeout=6)
        try:
            self.driver.execute_script(
                'document.getElementsByTagName("button")[0].click()'
            )
            wait.until(
                EC.presence_of_element_located(
                    (By.ID, 'idRandomPic')
                )
            )
        except:
            self.label_show_result.setText(
                '【連線逾時或是網路不穩定】\n' + 
                '【請檢查網路環境以及是否為尖峰時段。】'
            )
            
    def save_and_open_image(self):
        # Save Image
        image_path = 'temp\\ImageOut.png'
        element_img = self.driver.find_element_by_id('idRandomPic')
        left = element_img.location['x']
        top = element_img.location['y']
        right = element_img.location['x'] + element_img.size['width']
        bottom = element_img.location['y'] + element_img.size['height']
        self.driver.save_screenshot(image_path)
        im = Image.open(image_path) 
        im = im.crop((left, top, right, bottom))
        im.save(image_path)
        
        # Open Image
        try:
            self.pic_auth_num = QtGui.QPixmap(image_path)
            self.pic_box.setPixmap(self.pic_auth_num)
            
            # Clear and Focus to the Authent-Number Inputing Field.
            self.line_edit_num.clear()
            self.line_edit_num.setFocus()
            
            if self.re_order == 1:
                self.label_show_result.setText(
                    '→ 已重新執行訂票程序，請再次輸入認證碼。'
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(0, 0, 0);'
                )
                self.re_order = 0                
            
        except IOError as err:
            self.pic_box.setText(
                'File ERROR: ' + str(err)
            )
            self.label_show_result.setText(
                '顯示圖片程序發生錯誤，可能是找不到認證碼圖片檔，' + 
                '請重新操作。\n'
            )
            self.label_show_result.setStyleSheet(
                    'color: rgb(200, 0, 0);'
            )
    
    # -----------------------------------------------------------------------#
    # ----- MAIN PROCESS of Pushing Button "Submit authentication code"----- #
    def submit_auth_number(self):
        # Submit Authent-Number to the Next Page.
        self.driver.execute_script(
            'document.getElementsByTagName("button")[2].click();'
        )
        if self.book_type == 1:
            self.show_final_result_sg()

        elif self.book_type == 2:
            self.show_final_result_gb()
        
    def show_final_result_sg(self):
        # Show Final Results with Different Cases.
        try:
            wait = WebDriverWait(self.driver, timeout=2)
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, 'font'), '亂數號碼錯誤'
                )
            )
            
            result_final1 = self.driver.execute_script(
                'result_final = ' + 
                'document.getElementsByTagName("font")[0].innerText;' +
                'return result_final'
            )
            result_final2 = self.driver.execute_script(
                'result_final = ' + 
                'document.getElementsByTagName("font")[1].innerText;' +
                'return result_final'
            )
            self.label_show_result.setText(
                result_final1 + '或\n' + result_final2
                + '\n\n' + '→ 請重新輸入認證碼。'
            )
            self.label_show_result.setStyleSheet(
                'color: rgb(200, 0, 0);'
            )
            self.driver.execute_script(
                'find_reInput_btn = ' + 
                'document.getElementsByTagName("input");' + 
                'find_reInput_btn[find_reInput_btn.length-1].click();'
            )
            self.save_and_open_image()
            
        except:
            wait = WebDriverWait(self.driver, timeout=6)
            wait.until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, 'style')
                )
            )
            self.found_str_id = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("身分證字號錯誤");' + 
                'return find_index;'
            )
            self.found_str_fail = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("訂票額滿");' + 
                'return find_index;'
            )
            self.found_str_book_num = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("還有空位的車次如下");' + 
                'return find_index;'
            )
            
            if not self.found_str_id == -1:
                result_final = self.driver.execute_script(
                    'result_final = ' + 
                    'document.getElementsByTagName("font")' + 
                    '[1].innerText.slice(0, 9);' +
                    'return result_final;'
                )
                self.label_show_result.setText(
                    str(result_final) + 
                    '\n\n' + 
                    '→ 請重新輸入身分證字號。'
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(200, 0, 0);'
                )
                # Clear and Focus to the ID Inputing Field.
                self.line_edit_id.clear()
                self.line_edit_id.setFocus()
                
            elif not self.found_str_fail == -1:
                self.re_order = 1
                result1 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[0].innerText;' + 
                    'return result_final;'
                )
                result2 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                result1 = result1.split('─')[0].strip()
                result2 = result2.split('─')[0].strip()
                self.label_show_result.setText(
                    '訂單程票結果：' + 
                    result1 + ' 或 ' + result2 + 
                    '\n\n' + 
                    '→ 3秒後將重新為您執行訂票程序。'
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(200, 0, 0);'
                )
                QtCore.QTimer.singleShot(
                    3000, self.button_book_single_event
                )
                
            elif not self.found_str_book_num == -1:
                self.driver.execute_script(
                    'document.getElementsByTagName("a")[1].click();'
                )
                wait = WebDriverWait(self.driver, timeout=6)
                wait.until(
                    EC.text_to_be_present_in_element(
                        (By.TAG_NAME, 'strong'), 
                        '您的車票已訂到'
                    )
                )
                result_id = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                result_code = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[3].innerText;' + 
                    'return result_final;'
                )
                self.label_show_result.setText(
                    '【單程車票】\n\n' + 
                    '身份證字號：' + result_id + '\n\n' + 
                    '電腦代碼：' + result_code
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(0, 140, 0);'
                )        
                    
    def show_final_result_gb(self):
        # Show Final Results with Different Cases.
        try:
            wait = WebDriverWait(self.driver, timeout=2)
            wait.until(
                EC.text_to_be_present_in_element(
                    (By.TAG_NAME, 'font'), '亂數號碼錯誤'
                )
            )
            
            result_final1 = self.driver.execute_script(
                'result_final = ' + 
                'document.getElementsByTagName("font")[0].innerText;' +
                'return result_final'
            )
            result_final2 = self.driver.execute_script(
                'result_final = ' + 
                'document.getElementsByTagName("font")[1].innerText;' +
                'return result_final'
            )
            self.label_show_result.setText(
                result_final1 + '或\n' + result_final2
                + '\n\n' + '→ 請重新輸入認證碼。'
            )
            self.label_show_result.setStyleSheet(
                'color: rgb(200, 0, 0);'
            )
            self.driver.execute_script(
                'find_reInput_btn = ' + 
                'document.getElementsByTagName("input");' + 
                'find_reInput_btn[find_reInput_btn.length-1].click();'
            )
            self.save_and_open_image()
            
        except:
            wait = WebDriverWait(self.driver, timeout=6)
            wait.until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, 'Frame')
                )
            )
            self.driver.switch_to.frame(0)
            wait.until(
                EC.presence_of_element_located(
                    (By.TAG_NAME, 'strong')
                )
            )
            self.found_str_id = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("身分證字號錯誤");' + 
                'return find_index;'
            )
            self.found_str_fail = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("訂票額滿");' + 
                'return find_index;'
            )
            self.found_str_success = self.driver.execute_script(
                'var find_index;' + 
                'find_index = document.documentElement.' + 
                'innerHTML.indexOf("電腦代碼");' + 
                'return find_index;'
            )
            
            if not self.found_str_id == -1:
                result_final = self.driver.execute_script(
                    'result_final = ' + 
                    'document.getElementsByTagName("font")' + 
                    '[1].innerText.slice(0, 9);' +
                    'return result_final;'
                )
                self.label_show_result.setText(
                    str(result_final) + 
                    '\n\n' + 
                    '→ 請重新輸入身分證字號。'
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(200, 0, 0);'
                )
                # Clear and Focus to the ID Inputing Field.
                self.line_edit_id.clear()
                self.line_edit_id.setFocus()
                
            elif not self.found_str_fail == -1:
                self.re_order = 1
                result_go1 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[0].innerText;' + 
                    'return result_final;'
                )
                result_go2 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(1)
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, 'strong')
                    )
                )
                result_bk1 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[0].innerText;' + 
                    'return result_final;'
                )
                result_bk2 = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("li")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                result_go1 = result_go1.split('─')[0].strip()
                result_go2 = result_go2.split('─')[0].strip()
                result_bk1 = result_bk1.split('─')[0].strip()
                result_bk2 = result_bk2.split('─')[0].strip()
                self.label_show_result.setText(
                    '去程結果：' + 
                    result_go1 + ' 或 ' + result_go2 + 
                    '\n\n' + 
                    '回程結果：' + 
                    result_bk1 + ' 或 ' + result_bk2 + 
                    '\n\n' + 
                    '→ 3秒後將重新為您執行訂票程序。'
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(200, 0, 0);'
                )
                QtCore.QTimer.singleShot(
                    3000, self.button_book_go_back_event
                )
                
            elif not self.found_str_success == -1:
                result_go_id = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                result_go_code = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[3].innerText;' + 
                    'return result_final;'
                )
                self.driver.switch_to.default_content()
                self.driver.switch_to.frame(1)
                wait.until(
                    EC.presence_of_element_located(
                        (By.TAG_NAME, 'strong')
                    )
                )
                result_bk_id = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[1].innerText;' + 
                    'return result_final;'
                )
                result_bk_code = self.driver.execute_script(
                    'var result_final = ' + 
                    'document.getElementsByTagName("span")' + 
                    '[3].innerText;' + 
                    'return result_final;'
                )
                self.label_show_result.setText(
                    '【出發車票】\n' + 
                    '身份證字號：' + result_go_id + '\n' + 
                    '電腦代碼：' + result_go_code + 
                    '\n\n' + 
                    '【回程車票】\n' + 
                    '身份證字號：' + result_bk_id + '\n' + 
                    '電腦代碼：' + result_bk_code
                )
                self.label_show_result.setStyleSheet(
                    'color: rgb(0, 140, 0);'
                )
        
def main():
    # This is a very important solution 
    # for the problem in the IPython console.
    app_main = 0
    # ---------------------------------------------------------------------- #
    app_main = QtGui.QApplication(
        sys.argv, 
        QtCore.Qt.WindowStaysOnTopHint
    )
    app_main.processEvents()
    
    # Show Main Window
    tra_ticket_booker = TraTicketBooker()
    tra_ticket_booker.show()
    
    sys.exit(app_main.exec_())
    tra_ticket_booker.driver.quit()
    
if __name__ == "__main__":
    main()
