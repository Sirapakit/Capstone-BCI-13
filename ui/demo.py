import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel, QFrame, QSplitter, QHBoxLayout,QVBoxLayout, QPushButton, QPlainTextEdit
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QProcess
from qtwidgets import Toggle, AnimatedToggle
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import numpy as np
import math
import pylsl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui, QtWidgets
from typing import List

plot_duration = 5  # how many seconds of data to show
update_interval = 60  # ms between screen updates
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
        # ts will be empty if no samples were pulled, a list of timestamps otherwise
        if ts:
            ts = np.asarray(ts)
            y = self.buffer[0:ts.size, :]
            this_x = None
            old_offset = 0
            new_offset = 0
            for ch_ix in range(self.channel_count):
                # we don't pull an entire screen's worth of data, so we have to
                # trim the old data and append the new data to it
                old_x, old_y = self.curves[ch_ix].getData()
                # the timestamps are identical for all channels, so we need to do
                # this calculation only once
                if ch_ix == 0:
                    # find the index of the first sample that's still visible,
                    # i.e. newer than the left border of the plot
                    old_offset = old_x.searchsorted(plot_time)
                    # same for the new data, in case we pulled more data than
                    # can be shown at once
                    new_offset = ts.searchsorted(plot_time)
                    # append new timestamps to the trimmed old timestamps
                    this_x = np.hstack((old_x[old_offset:], ts[new_offset:]))
                # append new data to the trimmed old data
                this_y = np.hstack((old_y[old_offset:], y[new_offset:, ch_ix] - ch_ix))
                # replace the old data
                self.curves[ch_ix].setData(this_x, this_y)


class MarkerInlet(Inlet):
    def __init__(self, info: pylsl.StreamInfo):
        super().__init__(info)

    def pull_and_plot(self, plot_time, plt):
        strings, timestamps = self.inlet.pull_chunk(0)
        if timestamps:
            for string, ts in zip(strings, timestamps):
                plt.addItem(pg.InfiniteLine(ts, angle=90, movable=False, label=string[0]))


class Window(QWidget):
    # def main():
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)    
        inlets: List[Inlet] = []
        print("looking for streams")
        streams = pylsl.resolve_streams()

        # Create the pyqtgraph window
        self.pw = pg.PlotWidget(title='LSL Plot')
        
        plt = self.pw.getPlotItem()

        # plt.enableAutoRange(x=False, y=True)

        # iterate over found streams, creating specialized inlet objects that will
        # handle plotting the data
        for info in streams:
            if info.type() == 'Markers':
                if info.nominal_srate() != pylsl.IRREGULAR_RATE \
                        or info.channel_format() != pylsl.cf_string:
                    print('Invalid marker stream ' + info.name())
                print('Adding marker inlet: ' + info.name())
                inlets.append(MarkerInlet(info))
            elif info.nominal_srate() != pylsl.IRREGULAR_RATE \
                    and info.channel_format() != pylsl.cf_string:
                print('Adding data inlet: ' + info.name())
                inlets.append(DataInlet(info, plt))
            else:
                print('Don\'t know what to do with stream ' + info.name())

        def scroll():
            """Move the view so the data appears to scroll"""
            # We show data only up to a timepoint shortly before the current time
            # so new data doesn't suddenly appear in the middle of the plot
            fudge_factor = pull_interval * .002
            plot_time = pylsl.local_clock()
            self.pw.setXRange(plot_time - plot_duration + fudge_factor, plot_time - fudge_factor)

        def update():
            # def update(self):
            # Read data from the inlet. Use a timeout of 0.0 so we don't block GUI interaction.
                mintime = pylsl.local_clock() - plot_duration
            # call pull_and_plot for each inlet.
            # Special handling of inlet types (markers, continuous data) is done in
            # the different inlet classes.
                for inlet in inlets:
                    inlet.pull_and_plot(mintime, plt)

        # create a timer that will move the view every update_interval ms
        update_timer = QtCore.QTimer()
        update_timer.timeout.connect(scroll)
        update_timer.start(update_interval)
        # create a timer that will pull and add new data occasionally
        pull_timer = QtCore.QTimer()
        pull_timer.timeout.connect(update)
        pull_timer.start(pull_interval)

        self.left_layout = QHBoxLayout(self)
        self.left_layout.addWidget(self.pw)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.left_layout)

        self.l_bottom_layout = QHBoxLayout()
        toggle_1_label = QLabel()
        toggle_1_label.setText('Test with 50Hz Filter')
        toggle_2_label = QLabel()
        toggle_2_label.setText('Test with 60Hz Filter')
        toggle_1 = Toggle()  # default color
        toggle_1.released.connect(update)
        toggle_2 = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        ) # orange color
        self.l_bottom_layout.addWidget(toggle_1_label)
        self.l_bottom_layout.addWidget(toggle_1)
        self.l_bottom_layout.addWidget(toggle_2_label)
        self.l_bottom_layout.addWidget(toggle_2)
        self.l_bottom_widget = QWidget()
        self.l_bottom_widget.setLayout(self.l_bottom_layout)

        font_stage = QFont()
        font_stage.setPointSize (10)
        font_stage.setBold (True)
        font_stage.setWeight (20)
        self.text_stage_label = QLabel()
        self.text_stage_label.setText('Seizure Stage')
        self.text_stage_label.setFont(font_stage)
        self.p = None
        self.btn = QPushButton('Test Seizure Stage')
        self.btn.pressed.connect(self.start_process)
        self.text_stage = QPlainTextEdit()
        self.right_layout = QVBoxLayout()
        self.right_layout.addWidget(self.btn)
        self.right_layout.addWidget(self.text_stage_label)
        self.right_layout.addWidget(self.text_stage)
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)

        second = 30
        self.count = second * 10
        self.start = False
        font_timer = QFont()
        font_timer.setPointSize (14)
        font_timer.setBold (True)
        font_timer.setWeight (20)
        self.label = QLabel("//COUNTDOWN-TIMER//", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setFont(font_timer)
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(100)
        self.r_bottom_layout = QVBoxLayout()
        self.r_bottom_layout.addWidget(self.label)
        self.r_bottom_widget = QWidget()
        self.r_bottom_widget.setLayout(self.r_bottom_layout)


        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.left_widget)
        self.splitter1.addWidget(self.l_bottom_widget)
        self.splitter1.setStretchFactor(1, 1)

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.right_widget)
        self.splitter2.addWidget(self.r_bottom_widget)
        self.splitter2.setStretchFactor(1, 1)

        self.splitter3 = QSplitter(Qt.Horizontal)
        self.splitter3.addWidget(self.splitter1)
        self.splitter3.addWidget(self.splitter2)
        self.splitter3.setStretchFactor(1, 1)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.splitter3)
        self.setLayout(self.layout)

    def message(self, s):
        font = QFont ()
        font.setPointSize (14)
        font.setBold (False)
        font.setWeight (50)
        self.text_stage.setPlainText(s)
        if s == "\tSeizure-onset":
            self.start = True
        self.text_stage.setFont(font)
        
    def start_process(self):
        if self.p is None:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self.handle_stdout)
            self.p.finished.connect(self.process_finished)
            self.p.start("python", ['demo_stage.py'])

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def process_finished(self):
        self.p = None
    
    def showTime(self):
        if self.start:
            self.count -= 1
  
        if self.count == 0:
            self.start = False
            self.label.setText(" Seizure !!!! ")
  
        if self.start:
            text = str(self.count / 10) + " s"
            self.label.setText(text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    app.exec_()