import time
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from spectrometer_commands import spectrometer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    # noinspection PyUnusedLocal
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


class GUI:

    def __init__(self):

        self.root = spectrometer()
        self.avg = 10
        self.sec = 0
        self.msec = 100
        self.brate = 9600
        self.mode = "z"
        self.spectrum = []
        self.app = QtWidgets.QApplication([])
        self.call = uic.loadUi("spectrometer1.ui")
        self.sc = MplCanvas(self.call.centralwidget, width=5, height=4, dpi=100)
        self.call.gridLayout.addWidget(self.sc)

    def open(self):
        self.call.show()
        self.app.exec()

    def set_val(self):
        self.avg = int(self.call.avg.text())
        self.sec = int(self.call.sec.currentText())
        self.msec = int(self.call.msec.currentText())
        self.brate = int(self.call.baud.currentText())
        self.root.set_baud(self.brate)
        self.root.set_avg_num(self.avg)
        self.root.set_acquisition_time(self.sec * 1000 + self.msec)

        if self.call.bin.isChecked():
            self.mode = "b"
            self.root.spec_mode("b")

            print("Binary Mode Selected")

        if self.call.ascii.isChecked():
            self.mode = "a"
            self.root.spec_mode("a")
            print("Ascii Mode Selected")

        # graph mode
        if self.call.single.isChecked():
            if self.mode == "b":
                self.root.capture_binary()
        if self.call.cont.isChecked():
            print("continuous Mode Selected")

    def start(self):
        self.root.spec_init()
        self.call.timer = QtCore.QTimer()
        if self.call.single.isChecked():
            self.update_plot()
        else:
            self.call.timer.setInterval(100)
            self.call.timer.timeout.connect(self.update_plot)
            self.call.timer.start()

    def stop(self):
        self.root.port.close()

    def pause(self):
        self.call.timer.stop()

    def capture(self):
        msg = QMessageBox()
        msg.setWindowTitle("Capture")
        msg.setText("Figure Saved Successfully")
        msg.exec_()
        self.sc.fig.savefig('/home/devanshu/Desktop/sprctrometer/Figures/figure.png')
        self.sc.fig.savefig('/home/devanshu/Desktop/sprctrometer/Figures/figure.pdf')

    def update_plot(self):
        arr = self.root.capture(self.mode)
        self.sc.axes.plot(arr, color='grey')
        # sc.axes.set_xlim(left=max(0, i - 10), right=i + 10)
        self.sc.fig.canvas.draw()
        time.sleep(0.1)
#

ui = GUI()
ui.open()

