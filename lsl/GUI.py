from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QSplitter, QHBoxLayout,QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QProcess
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import List

import sys
import numpy as np
import math
import pylsl
import pyqtgraph as pg
import time

PLOT_DURATION = 5 # how many seconds of data to show
UPDATE_INTERVAL = 500  # ms between screen updates
PULL_INTERVAL = 500 # ms between each pull operation
PREICTAL_PERIOD_MIN = 59 # mins
PREICTAL_PERIOD_SEC = 60 # secs

class Inlet:
    def __init__(self, info: pylsl.StreamInfo):
        self.inlet = pylsl.StreamInlet(info, max_buflen=PLOT_DURATION,
                                       processing_flags=pylsl.proc_clocksync | pylsl.proc_dejitter)
        self.name = info.name()
        self.channel_count = info.channel_count()

    def pull_and_plot(self, plot_time: float, plt: pg.PlotItem):
        
        pass

class DataInlet(Inlet):
    dtypes = [[], np.float32, np.float64, None, np.int32, np.int16, np.int8, np.int64]

    def __init__(self, info: pylsl.StreamInfo, plt: pg.PlotItem):
        super().__init__(info)
      
        bufsize = (2 * math.ceil(info.nominal_srate() * PLOT_DURATION), info.channel_count())
        self.buffer = np.empty(bufsize, dtype=self.dtypes[info.channel_format()])
        empty = np.array([])
       
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
        self.color_palette = QPalette()
        self.gradient = QLinearGradient(0, 0, 0, 1200)
        self.gradient.setColorAt(0.4, QColor(0, 0, 0))
        self.gradient.setColorAt(1.0, QColor(210, 104, 84))
        self.color_palette.setBrush(QPalette.Window, QBrush(self.gradient))
        self.setPalette(self.color_palette)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget) 

        page1 = HomeWindow(self)
        page1.test_btn.clicked.connect(self.test_window)
        page1.realtime_btn.clicked.connect(self.realtime_window)
        self.central_widget.addWidget(page1)        
 
        # self.setGeometry(300, 100, 970, 670) 
        self.showMaximized()
        self.setWindowTitle('NEUROMATE')
        self.setWindowIcon(QIcon('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\neuromate-brain.png'))

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

        self.logo_layout = QVBoxLayout()
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_widget = QWidget()
        self.logo_label = QLabel()
        self.pixmap = QPixmap('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\neuromate-logo-bigbrain (2).png')
        self.logo_label.setPixmap(self.pixmap)

        font_slogan = QFont('Tw Cen MT',20)
        self.slogan_label = QLabel('-Be seizure savvy by Neuromate saver-')
        self.slogan_label.setFont(font_slogan)
        self.slogan_label.setAlignment(Qt.AlignCenter)
        self.slogan_label.setStyleSheet("color: white;")
        self.logo_layout.addWidget(self.logo_label)
        self.logo_layout.addWidget(self.slogan_label)
        self.logo_widget.setLayout(self.logo_layout) 
        self.logo_widget.resize(self.pixmap.width(), self.pixmap.height())

        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignCenter)
        self.btn_widget = QWidget()
        self.label = QLabel('\t\t\t\t\t')
        font_btn = QFont('Tw Cen MT',30)
        self.btn_test = QPushButton('TEST')
        self.btn_test.setFont(font_btn)
        self.btn_test.setFixedSize(400,100)
        self.btn_test.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 50;"
                             "background-color : black;"
                             "color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}"
                             )
        self.btn_realtime = QPushButton('REAL TIME')
        self.btn_realtime.setFont(font_btn)
        self.btn_realtime.setFixedSize(400,100)
        self.btn_realtime.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 50;"
                             "background-color : black;"
                             "color: white;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}"
                             )
        self.btn_layout.setAlignment(Qt.AlignCenter)
        self.btn_layout.addWidget(self.btn_test)
        self.btn_layout.addWidget(self.label)
        self.btn_layout.addWidget(self.btn_realtime)
        self.btn_widget.setLayout(self.btn_layout)
        self.test_btn = self.btn_test   
        self.realtime_btn = self.btn_realtime      

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.logo_widget)
        self.layout.addWidget(self.btn_widget)
        self.setLayout(self.layout)

class Test_page(QMainWindow):
    def __init__(self, parent=None):
        super(Test_page, self).__init__(parent)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.color_palette = QPalette()
        self.color_palette.setColor(QPalette.Background, QColor('#111111'))
        self.setPalette(self.color_palette)
        self.setAutoFillBackground(True)
 
        page2 = TestWindow(self)
        page2.back_btn.clicked.connect(self.back_homewindow)
        self.central_widget.addWidget(page2)

    def back_homewindow(self):
        page_hw = Home_page(self)
        self.page_hw_palette = QPalette()
        self.gradient = QLinearGradient(0, 0, 0, 1200)
        self.gradient.setColorAt(0.4, QColor(0, 0, 0))
        self.gradient.setColorAt(1.0, QColor(210, 104, 84))
        self.page_hw_palette.setBrush(QPalette.Background, QBrush(self.gradient))
        self.setPalette(self.page_hw_palette)
        self.setAutoFillBackground(True)
        self.central_widget.addWidget(page_hw)
        self.central_widget.setCurrentIndex(self.central_widget.currentIndex()+1)

class TestWindow(QWidget):
    def __init__(self, parent=None):
        super(TestWindow, self).__init__(parent)

        self.logo_layout = QHBoxLayout()
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_widget = QWidget()
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\neuromate-logo-bigbrain-top.png')
        self.logo_label.setPixmap(self.pixmap)
        self.logo_layout.addWidget(self.logo_label)
        self.logo_widget.setLayout(self.logo_layout) 
        self.logo_widget.setStyleSheet("background-color: black;")
   
        self.inlets: List[Inlet] = []
        print("looking for streams")
        self.streams = pylsl.resolve_streams()

        self.pw_bipolar_ch1 = pg.PlotWidget(title='LSL Plot: First Bipolar Channel (Database)')
        self.plt_bipolar_ch1 = self.pw_bipolar_ch1.getPlotItem()
        self.pw_bipolar_ch2 = pg.PlotWidget(title='LSL Plot: Second Bipolar Channel (Database)')
        self.plt_bipolar_ch2 = self.pw_bipolar_ch2.getPlotItem()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.pw_bipolar_ch1)
        self.left_layout.addWidget(self.pw_bipolar_ch2)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignCenter)
        font_btn = QFont('Tw Cen MT',16)
        font_btn.setBold(True)
        self.btn_play = QPushButton('PLAY')  
        self.btn_play.setFont(font_btn)
        self.btn_play.setFixedSize(200,50)
        self.btn_play.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 20;"
                             "background-color : #D26854;"
                             "color: black;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}")
        self.btn_play.clicked.connect(self.update_lsl)
        self.play_btn = self.btn_play
        self.btn_layout.addWidget(self.btn_play)
        self.left_layout.addLayout(self.btn_layout)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)

        self.p = None
        self.text_stage = QPlainTextEdit()

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignCenter)
     
        self.count_min = PREICTAL_PERIOD_MIN
        self.count_sec = PREICTAL_PERIOD_SEC
        self.start = False
        font_label = QFont('Tw Cen MT',30)
        font_btn.setBold(True)
        self.label_layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText('SEIZURE\nSTAGE')
        self.label.setFixedHeight(200)
        self.label.setFixedWidth(300)
        self.label.setStyleSheet("border-radius: 75; background-color: #DBB3AD;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font_label)

        self.label_layout.addWidget(self.label)
        self.right_layout.addLayout(self.label_layout)

        self.btn_back_layout = QHBoxLayout()
        self.btn_back_layout.setAlignment(Qt.AlignCenter)
        self.btn_back = QPushButton('BACK')
        self.btn_back.setFont(font_btn)
        self.btn_back.setFixedSize(200,50)
        self.btn_back.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 25;"
                             "background-color : #D26854;"
                             "color: black;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}")
        
        self.empty_bottom_label = QLabel('\n\n\n\n\n\n\n')

        self.btn_back_layout.addWidget(self.empty_bottom_label)
        self.btn_back_layout.addWidget(self.btn_back)
        self.right_layout.addLayout(self.btn_back_layout)
        self.back_btn = self.btn_back
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.left_widget)
        self.splitter1.addWidget(self.right_widget)
        self.splitter1.setSizes([1500,300])
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
                    and info.channel_format() != pylsl.cf_string and info.name() == 'bipolar_ch1_database':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_bipolar_ch1))

            if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    and info.channel_format() != pylsl.cf_string and info.name() == 'bipolar_ch2_database':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_bipolar_ch2))
            
        mintime = pylsl.local_clock() - PLOT_DURATION
        for inlet in self.inlets:
            inlet.pull_and_plot(mintime, self.plt_bipolar_ch1)
            inlet.pull_and_plot(mintime, self.plt_bipolar_ch2)
                
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.scroll)
        self.update_timer.start(UPDATE_INTERVAL)

        self.pull_timer = QtCore.QTimer()
        self.pull_timer.timeout.connect(self.update_lsl)
        self.pull_timer.start(PULL_INTERVAL)
        self.start_process()
        
    def scroll(self):
        fudge_factor = PULL_INTERVAL * .002
        plot_time = pylsl.local_clock()
        self.pw_bipolar_ch1.setXRange(plot_time - PLOT_DURATION + fudge_factor, plot_time - fudge_factor)
        self.pw_bipolar_ch2.setXRange(plot_time - PLOT_DURATION + fudge_factor, plot_time - fudge_factor)
        
    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.finished.connect(self.process_finished)
            self.p.start("python", ['C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\demo_inlet.py'])
            # self.p.start("python", ['C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\demo_stage.py'])

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def message(self,s):
        if s == 'Non-seizure':
            self.start = False
            self.label.setText("NON\nSEIZURE")
        
        if s == 'Preictal':
            self.start = True
            self.show_time()
        
        if s == 'Seizure':
            self.start = False
            self.label.setText("SEIZURE")

    def process_finished(self):
        self.p = None

    def show_time(self):
        if self.start:
            self.count_sec -= 1
            if self.count_sec == -1:
                self.count_min -= 1
                self.count_sec = PREICTAL_PERIOD_SEC

            if self.count_min == 0:
                self.start = False
                self.count_min = PREICTAL_PERIOD_MIN
                self.count_sec = PREICTAL_PERIOD_SEC
        
        if self.start:
            text = str(self.count_min) + ':' +  str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_sec < 10:
            text = str(self.count_min) + ":" + "0" + str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_min < 10:
            text = '0' + str(self.count_min) + ':' +  str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_sec < 10 and self.count_min < 10:
            text = '0' + str(self.count_min) + ':' + '0' + str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
    
class Realtime_page(QMainWindow):
    def __init__(self, parent=None):
        super(Realtime_page, self).__init__(parent)
        self.UI()
 
    def UI(self):
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        self.color_palette = QPalette()
        self.color_palette.setColor(QPalette.Background, QColor('#111111'))
        self.setPalette(self.color_palette)
        self.setAutoFillBackground(True)
 
        page3 = RealtimeWindow(self)
        page3.back_btn.clicked.connect(self.back_homewindow)
        self.central_widget.addWidget(page3)

    def back_homewindow(self):
        page_hw = Home_page(self)
        self.page_hw_palette = QPalette()
        self.gradient = QLinearGradient(0, 0, 0, 1200)
        self.gradient.setColorAt(0.4, QColor(0, 0, 0))
        self.gradient.setColorAt(1.0, QColor(210, 104, 84))
        self.page_hw_palette.setBrush(QPalette.Background, QBrush(self.gradient))
        self.setPalette(self.page_hw_palette)
        self.setAutoFillBackground(True)
        self.central_widget.addWidget(page_hw)
        self.central_widget.setCurrentIndex(self.central_widget.currentIndex()+1)
    
class RealtimeWindow(QWidget):
    def __init__(self, parent=None):
        super(RealtimeWindow, self).__init__(parent)

        self.logo_layout = QHBoxLayout()
        self.logo_layout.setAlignment(Qt.AlignCenter)
        self.logo_widget = QWidget()
        self.logo_label = QLabel(self)
        self.pixmap = QPixmap('C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\neuromate-logo-bigbrain-top.png')
        self.logo_label.setPixmap(self.pixmap)
        self.logo_layout.addWidget(self.logo_label)
        self.logo_widget.setLayout(self.logo_layout) 
        self.logo_widget.setStyleSheet("background-color: black;")
   
        self.inlets: List[Inlet] = []
        print("looking for streams")
        self.streams = pylsl.resolve_streams()

        self.pw_bipolar_ch1 = pg.PlotWidget(title='LSL Plot: First Bipolar Channel')
        self.plt_bipolar_ch1 = self.pw_bipolar_ch1.getPlotItem()
        self.pw_bipolar_ch2 = pg.PlotWidget(title='LSL Plot: Second Bipolar Channel')
        self.plt_bipolar_ch2 = self.pw_bipolar_ch2.getPlotItem()

        self.left_layout = QVBoxLayout()
        self.left_layout.addWidget(self.pw_bipolar_ch1)
        self.left_layout.addWidget(self.pw_bipolar_ch2)
        self.btn_layout = QHBoxLayout()
        self.btn_layout.setAlignment(Qt.AlignCenter)
        font_btn = QFont('Tw Cen MT',16)
        font_btn.setBold(True)
        self.btn_play = QPushButton('PLAY')  
        self.btn_play.setFont(font_btn)
        self.btn_play.setFixedSize(200,50)
        self.btn_play.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 20;"
                             "background-color : #D26854;"
                             "color: black;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}")
        self.btn_play.clicked.connect(self.update_lsl)
        self.play_btn = self.btn_play
        self.btn_layout.addWidget(self.btn_play)
        self.left_layout.addLayout(self.btn_layout)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)

        self.p = None
        self.text_stage = QPlainTextEdit()

        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignCenter)
     
        self.start = False
        font_label = QFont('Tw Cen MT',30)
        font_btn.setBold(True)
        self.label_layout = QVBoxLayout()
        self.label = QLabel()
        self.label.setText('SEIZURE\nSTAGE')
        self.label.setFixedHeight(200)
        self.label.setFixedWidth(300)
        self.label.setStyleSheet("border-radius: 75; background-color: #DBB3AD;")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font_label)
        self.timer = QTimer(self)
        self.timer.start(100)

        self.label_layout.addWidget(self.label)
        self.right_layout.addLayout(self.label_layout)
        self.empty_bottom_label = QLabel('\n\n\n\n\n\n\n')

        self.btn_back_layout = QHBoxLayout()
        self.btn_back_layout.setAlignment(Qt.AlignCenter)
        self.btn_back = QPushButton('BACK')
        self.btn_back.setFont(font_btn)
        self.btn_back.setFixedSize(200,50)
        self.btn_back.setStyleSheet("QPushButton"
                             "{"
                             "border-radius : 25;"
                             "background-color : #D26854;"
                             "color: black;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : #E1E2E4;"
                             "color: black;"
                             "}")
        self.btn_back_layout.addWidget(self.empty_bottom_label)
        self.btn_back_layout.addWidget(self.btn_back)
        self.right_layout.addLayout(self.btn_back_layout)
        self.back_btn = self.btn_back
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.left_widget)
        self.splitter1.addWidget(self.right_widget)
        self.splitter1.setSizes([1500,300])
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
                    and info.channel_format() != pylsl.cf_string and info.name() == 'bipolar_ch1':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_bipolar_ch1))

            if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    and info.channel_format() != pylsl.cf_string and info.name() == 'bipolar_ch2':
                # print('Adding data inlet: ' + info.name())
                self.inlets.append(DataInlet(info, self.plt_bipolar_ch2))
            
        mintime = pylsl.local_clock() - PLOT_DURATION
        for inlet in self.inlets:
            inlet.pull_and_plot(mintime, self.plt_bipolar_ch1)
            inlet.pull_and_plot(mintime, self.plt_bipolar_ch2)
                
        self.update_timer = QtCore.QTimer()
        self.update_timer.timeout.connect(self.scroll)
        self.update_timer.start(UPDATE_INTERVAL)

        self.pull_timer = QtCore.QTimer()
        self.pull_timer.timeout.connect(self.update_lsl)
        self.pull_timer.start(PULL_INTERVAL)
        self.start_process()
        
    def scroll(self):
        fudge_factor = PULL_INTERVAL * .002
        plot_time = pylsl.local_clock()
        self.pw_bipolar_ch1.setXRange(plot_time - PLOT_DURATION + fudge_factor, plot_time - fudge_factor)
        self.pw_bipolar_ch2.setXRange(plot_time - PLOT_DURATION + fudge_factor, plot_time - fudge_factor)
        
    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.finished.connect(self.process_finished)
            self.p.start("python", ['C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\demo_inlet.py'])
            # self.p.start("python", ['C:\\Users\\ASUS\\Desktop\\testdata\\GUI\\demo_stage.py'])

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def message(self,s):
        if s == 'Non-seizure':
            self.start = False
            self.label.setText("NON\nSEIZURE")
        
        if s == 'Preictal':
            self.start = True
            self.show_time()
        
        if s == 'Seizure':
            self.start = False
            self.label.setText("SEIZURE")

    def process_finished(self):
        self.p = None
    
    def show_time(self):
        if self.start:
            self.count_sec -= 1
            if self.count_sec == -1:
                self.count_min -= 1
                self.count_sec = PREICTAL_PERIOD_SEC

            if self.count_min == 0:
                self.start = False
                self.count_min = PREICTAL_PERIOD_MIN
                self.count_sec = PREICTAL_PERIOD_SEC
        
        if self.start:
            text = str(self.count_min) + ':' +  str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_sec < 10:
            text = str(self.count_min) + ":" + "0" + str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_min < 10:
            text = '0' + str(self.count_min) + ':' +  str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)
            
        if self.count_sec < 10 and self.count_min < 10:
            text = '0' + str(self.count_min) + ':' + '0' + str(self.count_sec) + " s"
            self.label.setText('PREICTAL\n' + text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Home_page()
    win.show()
    app.exec_()