import time
from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox
from extra.spectro_rover import spectrometer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib

matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


root = spectrometer()
avg = 10
sec = 0
msec = 100
brate = 9600
mode = "z"
i = 0
spectrum = []
x, y = [], []


def set_val():
    global call, mode
    avg = int(call.avg.text())
    sec = int(call.sec.currentText())
    msec = int(call.msec.currentText())
    brate = int(call.baud.currentText())
    root.set_baud(brate)
    root.set_avg_num(avg)
    root.set_acquisition_time(sec * 1000 + msec)

    if call.bin.isChecked():
        mode = "b"
        root.spec_mode("b")

        print("Binary Mode Selected")

    if call.ascii.isChecked():
        mode = "a"
        root.spec_mode("a")
        print("Ascii Mode Selected")

    # graph mode
    if call.single.isChecked():
        if mode == "b":
            root.capture_binary()
    if call.cont.isChecked():
        print("continuous Mode Selected")

    print(avg)
    print(sec)
    print(msec)
    print(brate)


def start():
    root.spec_init()
    call.timer = QtCore.QTimer()
    if call.single.isChecked():
        update_plot()
    else:
        call.timer.setInterval(100)
        call.timer.timeout.connect(update_plot)
        call.timer.start()


def stop():
    root.port.close()


def pause():
    call.timer.stop()


def capture():
    msg = QMessageBox()
    msg.setWindowTitle("Capture")
    msg.setText("Figure Saved Sucessfully")
    x = msg.exec_()
    sc.fig.savefig('/home/devanshu/Desktop/sprctrometer/Figures/figure.png')
    sc.fig.savefig('/home/devanshu/Desktop/sprctrometer/Figures/figure.pdf')


def update_plot():
    arr = root.capture(mode)
    global sc
    sc.axes.plot(arr, color='grey')
    # sc.axes.set_xlim(left=max(0, i - 10), right=i + 10)
    sc.fig.canvas.draw()
    time.sleep(0.1)


app = QtWidgets.QApplication([])
call = uic.loadUi("spectrometer1.ui")
sc = MplCanvas(call.centralwidget, width=5, height=4, dpi=100)
call.gridLayout.addWidget(sc)
# call.timer = QtCore.QTimer()
# call.timer.setInterval(100)
# call.timer.timeout.connect(update_plot)
# call.timer.start()

call.start.clicked.connect(start)
call.set.clicked.connect(set_val)
call.stop.clicked.connect(stop)
call.capture.clicked.connect(capture)
call.pause.clicked.connect(pause)

call.show()
app.exec_()
