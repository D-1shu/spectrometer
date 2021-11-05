import serial
import time
import numpy as np
import matplotlib.pyplot as plt


def arr_plot(arr):
    plt.plot(arr)
    plt.show()
    time.sleep(2)
    plt.close()


class spectrometer:
    baud_rate = {0: 115200, 1: 38400, 2: 19200, 3: 9600, 4: 4800, 5: 2400, 6: 1200, 7: 600}

    def __init__(self, port='/dev/ttyUSB0'):
        self.port = serial.Serial(port, 9600)
        self.data_mode = 'a'  # b (binary) is default
        self.raman_arr = []
        self.avg_num = 1  # 1 is default
        self.integration_time = 21  # 21 is default
        self.darkspectrum = []
        self.baud = 3  # 3 is default
        self.delay = 35  # 35 is default

    def spec_init(self):
        self.port.write(b"Q\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def spec_reset(self):
        self.port.write(b"Q\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def spec_mode(self, data_mode='b'):
        self.data_mode = data_mode
        self.port.write(b"" + self.data_mode + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    """def spec_binary(self):
        self.data_mode = 'b'
        self.spec_mode()

    def spec_ascii(self):
        self.data_mode = 'a'
        self.spec_mode()"""

    def spec_reinitialize(self):
        self.port.write(b"Q\r\n")
        self.port.close()
        self.port = serial.Serial('/dev/ttyUSB0', self.baud_rate.get(self.baud))
        time.sleep(0.025)
        self.port.flushInput()

    def set_baud(self, val=3):
        if 0 <= val <= 7:
            self.baud = val
        self.port.write(b"K " + str(val) + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def decompress(self):
        pass

    def spec_acq(self):
        if self.data_mode == 'a':
            self.port.write(b"S\r\n")
            time.sleep(0.025)
            self.port.flushInput()
            for p in range(0, 2048):
                in_spec = self.port.readline()  # reading from spectrometer , its in bytes and has \r\n
                in_spec = in_spec[:-2]  # removing \r\n
                in_spec = int(in_spec.decode("utf-8"))  # converting to string
                self.raman_arr.append(in_spec)  # adding to the array
            time.sleep(0.025)
            self.port.flushInput()
        elif self.data_mode == 'b':
            pass

    def dark_spec_acq(self):
        if self.data_mode == 'a':
            self.port.write(b"S\r\n")
            time.sleep(0.025)
            self.port.flushInput()
            for p in range(0, 2048):
                in_spec = self.port.readline()  # reading from spectrometer , its in bytes and has \r\n
                in_spec = in_spec[:-2]  # removing \r\n
                in_spec = int(in_spec.decode("utf-8"))  # converting to string
                self.darkspectrum.append(in_spec)  # adding to the array
            time.sleep(0.025)
            self.port.flushInput()

    def raman_arr_calc(self):
        # dark spectrum
        self.dark_spec_acq()
        arr_plot(self.darkspectrum)

        time.sleep(2)

        # pixel values
        self.spec_acq()
        arr_plot(self.raman_arr)

        self.raman_arr = np.array(self.raman_arr)
        self.darkspectrum = np.array(self.darkspectrum)

        # corrected pixel values
        self.raman_arr = self.raman_arr - self.darkspectrum
        arr_plot(self.raman_arr)


    def set_integration_time(self, integration_time=21):
        if 21 <= integration_time <= 65000:  # BTC110 range
            self.integration_time = integration_time
            self.port.write(B"I " + str(self.integration_time) + "\r\n")
            time.sleep(0.025)
            self.port.flushInput()

    def set_avg_num(self, avg_num=1):
        if 15 <= avg_num <= 65535:  # BTC110 Range
            self.avg_num = avg_num
            self.port.write(B"A " + str(self.avg_num) + "\r\n")
            time.sleep(0.025)
            self.port.flushInput()

    def spec_values(self):
        self.port.write(b"S\r\n")
        time.sleep(0.025)
        self.port.readline()
        time.sleep(0.025)
        self.port.readline()
        time.sleep(0.025)
        self.port.flushInput()

        """temp = self.port.readline()
        temp.decode('unicode-escape')
        time.sleep(0.025)
        print(temp)"""

    def set_coeff(self):
        for val in range(4):
            coeff = input()
            self.port.write(B"C " + str(val) + coeff + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def set_pixel_mode(self, mode, n, x=0, y=0):
        if mode == 0:
            self.port.write(B"P 0\r\n")
        elif mode == 1:
            self.port.write(B"P 1 " + str(n) + "\r\n")
        elif mode == 2:
            self.port.write(B"P 2 " + str(n) + "\r\n")
        elif mode == 3:
            if x < y:
                self.port.write(B"P 3 " + str(x) + " " + str(y) + " " + str(n) + "\r\n")
        elif mode == 4:
            temp = " "
            if 0 <= n <= 6:
                for z in range(n):
                    temp += str(np.random.randint(0, 2048)) + " "
                self.port.write(B"P 4 " + str(n) + temp[:-1] + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def time_delay(self, delay):
        if 35 <= delay <= 65000:
            self.delay = delay
            self.port.write(B"T " + str(self.integration_time) + "\r\n")
            time.sleep(0.025)
            self.port.flushInput()

    def cont_plot(self, t=100):
        fig = plt.figure()
        t *= 5
        for p in range(t):
            plt.plot(self.raman_arr)
            plt.draw()
            self.spec_acq()
            plt.pause(0.2)
            fig.clear()


if __name__ == "__main__":
    test = spectrometer()
    test.spec_init()
    test.spec_mode()

    test.raman_arr_calc()
    test.cont_plot()  # 100 sec

# test git pull
