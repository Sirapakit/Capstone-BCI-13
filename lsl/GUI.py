import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QSplitter, QHBoxLayout,QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import math
import pylsl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import List
import time
import demo_inlet 

plot_duration = 5 # how many seconds of data to show
update_interval = 500  # ms between screen updates
pull_interval = 500 # ms between each pull operation

class Inlet:
    def __init__(self, info: pylsl.StreamInfo):
        self.inlet = pylsl.StreamInlet(info, max_buflen=plot_duration,
                                       processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.name = info.name()
        self.channel_count = info.channel_count()

    def pull_and_plot(self, plot_time: float, plt: pg.PlotItem):
        
        pass

class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]

    def __init__(self, info: pylsl.StreamInfo, plt: pg.PlotItem):
        super().__init__(info)
        # calculate the size for our buffer, i.e. two times the displayed data
        bufsize = (2 * math.ceil(info.nominal_srate() * plot_duration), info.channel_count())
        self.buffer = np.empty(bufsize, dtype=self.dtypes[info.channel_format()])
        empty = np.array([])
        # create one curve object for each channel/line that will handle displaying the data
        self.curves = [pg.PlotCurveItem(x=empty, y=empty , autoDownsample=True) for _ in range(self.channel_count)]
        for curve in self.curves:
            plt.addItem(curve)

    def pull_and_plot(self, plot_time, plt):
        # pull the data
        _, ts = self.inlet.pull_chunk(timeout=0.0,
                                      max_samples=self.buffer.shape[0],
                                      dest_obj=self.buffer)
       
        if ts:
            ts = np.asarray(ts)
            y = self.buffer[0:ts.size, :]
            this_x = None
            old_offset = 0
            new_offset = 0
            for ch_ix in range(self.channel_count):
                old_x, old_y = self.curves[ch_ix].getData()
                if ch_ix == 0:
                    old_offset = old_x.searchsorted(plot_time)
                    new_offset = ts.searchsorted(plot_time)
                    this_x = np.hstack((old_x[old_offset:], ts[new_offset:]))
                this_y = np.hstack((old_y[old_offset:], y[new_offset:, ch_ix] - ch_ix))
                self.curves[ch_ix].setData(this_x, this_y)

class MarkerInlet(Inlet):
    def __init__(self, info: pylsl.StreamInfo):
        super().__init__(info)

    def pull_and_plot(self, plot_time, plt):
        strings, timestamps = self.inlet.pull_chunk(0)
        if timestamps:
            for string, ts in zip(strings, timestamps):
                plt.addItem(pg.InfiniteLine(ts, angle=90, movable=False, label=string[0]))

class Home_page(QMainWindow):
    def __init__(self, parent=None):
        super(Home_page, self).__init__(parent)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        # self.central_widget.setStyleSheet("background-color: lightskyblue;")
 
        page1 = HomeWindow(self)
        page1.test_btn.clicked.connect(self.test_window)
        page1.realtime_btn.clicked.connect(self.realtime_window)
        self.central_widget.addWidget(page1)        
 
        self.setGeometry(300, 100, 970, 670) 
        # self.showMaximized()
        self.setWindowTitle('Seizure Prediction')
        self.setWindowIcon(QIcon('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\brain (1).png'))

    def test_window(self):
        page_tw = Test_page(self)
        self.central_widget.addWidget(page_tw)
        self.central_widget.setCurrentWidget(page_tw)
    
    def realtime_window(self):
        page_rt = Realtime_page(self)
        self.central_widget.addWidget(page_rt)
        self.central_widget.setCurrentWidget(page_rt)
 
class HomeWindow(QWidget):
    def __init__(self, parent=None):
        super(HomeWindow, self).__init__(parent)

        self.logo_layout = QHBoxLayout()
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_widget = QWidget()
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\logo.png')
        self.logo_label.setPixmap(self.pixmap)
        self.logo_layout.addWidget(self.logo_label)
        self.logo_widget.setLayout(self.logo_layout) 
        self.logo_widget.setStyleSheet("background-color: lightskyblue;")
        self.logo_widget.resize(self.pixmap.width(), self.pixmap.height())

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignCenter)
        self.right_widget = QWidget()
        font_label = QFont()
        font_label.setPointSize(30)
        font_label.setBold(True)
        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setText('WELCOME!')
        self.label.setFont(font_label)
        self.label.setStyleSheet("color: black;")
        font_btn = QFont()
        font_btn.setPointSize (14)
        self.btn_test = QPushButton('Test System')
        self.btn_test.setFont(font_btn)
        self.btn_test.setFixedSize(350,70)
        self.btn_test.setStyleSheet("border-radius : 30; border : 5px solid white; background-color: black; color: white;")
        self.btn_realtime = QPushButton('Real Time Seizure Prediction')
        self.btn_realtime.setFont(font_btn)
        self.btn_realtime.setFixedSize(350,70)
        self.btn_realtime.setStyleSheet("border-radius : 30; border : 5px solid white; background-color: black; color: white;")
        self.right_layout.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.label)
        self.right_layout.addWidget(self.btn_test)
        self.right_layout.addWidget(self.btn_realtime)
        self.right_widget.setLayout(self.right_layout)
        self.test_btn = self.btn_test   
        self.realtime_btn = self.btn_realtime      

        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.logo_widget)
        self.splitter1.addWidget(self.right_widget)
        self.splitter1.setStretchFactor(1, 1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.splitter1)
        self.setLayout(self.layout)

class Test_page(QMainWindow):
    def __init__(self, parent=None):
        super(Test_page, self).__init__(parent)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
 
        page2 = MainWindow(self)
        page2.back_btn.clicked.connect(self.back_homewindow)
        self.central_widget.addWidget(page2)
    
    def back_homewindow(self):
        page_hw = Home_page(self)
        self.central_widget.addWidget(page_hw)
        self.central_widget.setCurrentIndex(self.central_widget.currentIndex()+1)

class Realtime_page(QMainWindow):
    def __init__(self, parent=None):
        super(Realtime_page, self).__init__(parent)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
 
        page3 = MainWindow(self)
        page3.back_btn.clicked.connect(self.back_homewindow)
        self.central_widget.addWidget(page3)
    
    def back_homewindow(self):
        page_hw = Home_page(self)
        self.central_widget.addWidget(page_hw)
        self.central_widget.setCurrentIndex(self.central_widget.currentIndex()+1)

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.logo_layout = QHBoxLayout()
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_widget = QWidget()
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\logo.png')
        self.logo_label.setPixmap(self.pixmap)
        self.logo_layout.addWidget(self.logo_label)
        self.logo_widget.setLayout(self.logo_layout) 
        self.logo_widget.setStyleSheet("background-color: lightskyblue;")
        self.logo_widget.resize(self.pixmap.width(), self.pixmap.height())
   
        self.inlets: List[Inlet] = []
        print("looking for streams")
        self.streams = pylsl.resolve_streams()
        # Create the pyqtgraph window
        self.pw_fp2_f8 = pg.PlotWidget(title='LSL Plot: Fp2-F8 Channel')
        self.plt_fp2_f8 = self.pw_fp2_f8.getPlotItem()
        self.pw_f8_t8 = pg.PlotWidget(title='LSL Plot: F8-T8 Channel')
        self.plt_f8_t8 = self.pw_f8_t8.getPlotItem()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.pw_fp2_f8)
        self.left_layout.addWidget(self.pw_f8_t8)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignCenter)
        font_btn = QFont()
        font_btn.setPointSize(14)
        font_btn.setBold(True)
        self.btn_play = QPushButton('Play')  
        self.btn_play.setFont(font_btn)
        self.btn_play.setFixedSize(100,40)
        self.btn_play.setStyleSheet("border-radius : 20; border : 2px solid lightskyblue; background-color: white; color: black;")
        self.btn_play.clicked.connect(self.update_lsl)
        self.btn_layout.addWidget(self.btn_play)
        self.left_layout.addLayout(self.btn_layout)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)

        font_stage = QFont()
        font_stage.setPointSize (10)
        font_stage.setBold (True)
        font_stage.setPointSize (14)
        self.p = None
        self.text_stage = QPlainTextEdit()
        # self.text_stage.setPlainText('       Seizure Stage')
        self.text_stage.setFont(font_stage)
        self.text_stage.setFixedHeight(50)
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignCenter)
        self.right_layout.addWidget(self.text_stage)

        self.count = 0
        self.start = False
        font_timer = QFont()
        font_timer.setPointSize (20)
        font_timer.setBold (True)
        self.label_layout = QHBoxLayout()
        self.label = QLabel("//COUNTDOWN-TIMER//", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font_timer)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)
        self.label_layout.addWidget(self.label)
        self.right_layout.addLayout(self.label_layout)
        self.btn_back_layout = QHBoxLayout()
        self.btn_back = QPushButton('Back')
        self.btn_back.setFont(font_btn)
        self.btn_back.setFixedSize(200,40)
        self.btn_back.setStyleSheet("border-radius : 20; background-color: lightskyblue; color: black;")
        self.btn_back_layout.addWidget(self.btn_back)
        self.right_layout.addLayout(self.btn_back_layout)
        self.back_btn = self.btn_back
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.left_widget)
        self.splitter1.addWidget(self.right_widget)
        self.splitter1.setStretchFactor(1, 1)

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.logo_widget)
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.setStretchFactor(1, 1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.splitter2)
        self.setLayout(self.layout)

    def update_lsl(self):
        for info in self.streams:
            if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    and info.channel_format() != pylsl.cf_string and info.name() == 'Fp2-F8':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_fp2_f8))

            if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    and info.channel_format() != pylsl.cf_string and info.name() == 'F8-T8':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_f8_t8))
            
        mintime = pylsl.local_clock() - plot_duration
        for inlet in self.inlets:
            inlet.pull_and_plot(mintime, self.plt_fp2_f8)
            inlet.pull_and_plot(mintime, self.plt_f8_t8)
                
        # create a timer that will move the view every update_interval ms
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.scroll)
        self.update_timer.start(update_interval)

        # create a timer that will pull and add new data occasionally
        self.pull_timer = QtCore.QTimer()
        self.pull_timer.timeout.connect(self.update_lsl)
        self.pull_timer.start(pull_interval)
        self.start_process()
        
    def scroll(self):
        fudge_factor = pull_interval * .002
        plot_time = pylsl.local_clock()
        self.pw_fp2_f8.setXRange(plot_time - plot_duration + fudge_factor, plot_time - fudge_factor)
        self.pw_f8_t8.setXRange(plot_time - plot_duration + fudge_factor, plot_time - fudge_factor)
        
    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.finished.connect(self.process_finished)
            self.p.start("python", ['./demo_inlet.py'])

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def message(self,s):
        font = QFont ()
        font.setPointSize(14)
        font.setBold(True)
        self.text_stage.setPlainText(s)
        self.text_stage.setFont(font)
        if s == '       Non-seizure':
            self.count = 30
            self.start = False
            text = "00:" + str(self.count) + " s"
            self.label.setText(text)
        self.text_stage.setFont(font)
        
        if s == '\tPreictal':
            self.start = True
        self.text_stage.setFont(font)
        
        if s == '\tSeizure':
            self.start = False
            self.label.setText(" Seizure !!!! ")
        self.text_stage.setFont(font)

        
    def process_finished(self):
        self.p = None
    
    def showTime(self):
        if self.start:
            self.count -= 1
            time.sleep(0.4)

        if self.start:
            text = "00:" + str(self.count) + " s"
            self.label.setText(text)
        
        if self.count < 10:
            text = "00:" + "0" + str(self.count) + " s"
            self.label.setText(text)
  
        if self.count == 0:
            self.start = False
            self.count = 30
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Home_page()
    win.show()
    app.exec_()