import numpy as np
import serial
import time


class spectrometer:
    baud_rate = {0: 115200, 1: 38400, 2: 19200, 3: 9600, 4: 4800, 5: 2400, 6: 1200, 7: 600}

    def __init__(self, port='/dev/ttyUSB0'):
        self.port = serial.Serial(port, 9600)
        self.data_mode = "a"  # ascii is default
        self.avg_num = 1  # 1 is default
        self.acquisition_time = 100  # 100 is default
        self.baud = 3  # 3 is default

    def spec_init(self):
        self.port.write(b"Q\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def spec_mode(self, data_mode="a"):
        self.data_mode = data_mode
        self.port.write(b"" + self.data_mode + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()

    def spec_reinit(self):
        self.port.write(b"Q\r\n")
        self.port.close()
        self.port = serial.Serial('/dev/ttyUSB0', self.baud_rate.get(self.baud))
        time.sleep(0.025)
        self.port.flushInput()

    def set_baud(self, val=3):
        if 0 <= val <= 7:
            self.baud = val
        self.port.write(b"K " + str(val) + "\r\n")
        self.spec_reinit()

    def capture_noisy(self):
        spectrum = np.zeros(2048)
        if self.data_mode == "a":
            self.port.write(b"S\r\n")
            time.sleep(0.025)
            self.port.readline()
            self.port.readline()
            for i in range(2048):
                in_spec = self.port.readline()  # reading from spectrometer , its in bytes and has \r\n
                in_spec = in_spec[:-2]  # removing \r\n
                in_spec = int(in_spec.decode("utf-8"))  # converting to string
                spectrum[i] = in_spec
            time.sleep(0.025)
            self.port.flushInput()
        return spectrum

    def capture_binary(self):
        spectrum = []
        in_spec = []
        self.port.write(b"S\r\n")
        time.sleep(0.025)
        self.port.readline()
        self.port.readline()
        while True:
            temp = self.port.read()
            if len(temp) == 0:
                break
            in_spec.append(ord(temp))
        time.sleep(0.025)
        i = 0
        for _ in in_spec:
            if i < len(in_spec):
                if in_spec[i] == 128:
                    spectrum.append(in_spec[i + 1] * 256 + in_spec[i + 2])
                    i += 3
                else:
                    if in_spec[i] > 128:
                        spectrum.append(spectrum[-1] + in_spec[i] - 256)
                    else:
                        spectrum.append(spectrum[-1] + in_spec[i])
                    i += 1
        time.sleep(0.025)
        self.port.flushInput()
        return spectrum

    def capture(self, mode):
        spectrum = []
        if mode == "a":
            spectrum = self.capture_noisy()
        elif mode == "b":
            spectrum = self.capture_binary()
        return spectrum


    def set_acquisition_time(self, acquisition_time=100):
        if 21 <= acquisition_time <= 65000:  # BTC110 range
            self.acquisition_time = acquisition_time
            self.port.write(b"I " + str(self.acquisition_time) + "\r\n")
            time.sleep(0.025)
            self.port.flushInput()

    def set_avg_num(self, avg_num=1):
        if 15 <= avg_num <= 65535:  # BTC110 Range
            self.avg_num = avg_num
            self.port.write(b"A " + str(self.avg_num) + "\r\n")
            time.sleep(0.025)
            self.port.flushInput()

    def set_coeff(self):
        for val in range(4):
            coeff = input()
            self.port.write(b"C " + str(val) + coeff + "\r\n")
        time.sleep(0.025)
        self.port.flushInput()


if __name__ == "__main__":
    pass
