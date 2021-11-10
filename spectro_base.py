"""
acq time
    allowed by spectrometer: 21-65000 ms
    default 100ms
    step size 100ms
    values = {100 msec , 200 msec ....900msec, }

averages
    allowed by spectrometer: 1-65535
    default 1
    values = 1 to 100

!!!!! currently the code doesnt check range of acq time 
or averages and similarly for all other parameters

!!!!! acq time and averages are not according to github 
issues specification
!!!!! binary mode should be added
"""
import threading

import numpy as np

from spectro_rover import spectrometer
import matplotlib.pyplot as plt


class gui:
    def __init__(self):
        self.baud = {0: 115200, 1: 38400, 2: 19200, 3: 9600, 4: 4800, 5: 2400, 6: 1200, 7: 600}

        # default parameter values
        self.parameters = {"averages": 1, "acq_time": 100, "baud_rate": 3, "data_mode": "a",
                           "acq_mode": "single"}
        self.rover = spectrometer()
        self.dark_spectrum = []
        self.noisy_spectrum = []
        self.clean_spectrum = []

    def print_parameters(self):
        for key, value in self.parameters.items():
            print("{} = {}".format(key, value) + " ")

    def set_parameters(self):
        print("Enter parameters: (avg, acq time, baud rate, data mode, acq mode)")
        self.parameters["averages"] = input("Enter average param: ")
        self.parameters["acq_time"] = input("Enter acquisition time: ")
        self.parameters["baud_rate"] = input("Enter baud rate: ")
        self.parameters["data_mode"] = raw_input("Enter data mode: ")
        self.parameters["acq_mode"] = raw_input("Enter single/ continuous: ")

        # Setting parameters to the rover
        self.rover.spec_mode(self.parameters.get("data_mode"))
        self.rover.set_baud(self.parameters.get("baud_rate"))
        self.rover.set_acquisition_time(self.parameters.get("acq_time"))
        self.rover.set_avg_num(self.parameters.get("averages"))

        print("Successfully set parameters ")
        self.print_parameters()

    def plot_single(self, spectrum):
        """
            Plots the spectrum and saves it as .png
        """
        plt.plot(spectrum)
        plt.show()
        if spectrum == self.clean_spectrum:
            plt.savefig("clean_speactrum.png")
        elif spectrum == self.dark_spectrum:
            plt.savefig("dark_spectrum.png")
        plt.close()

    def cont_plot(self):
        fig = plt.figure()

        for _ in range(100):
            self.fetch_noisy_spectrum()
            x = np.array(self.noisy_spectrum) - np.array(self.dark_spectrum)
            plt.plot(x)
            plt.draw()
            plt.pause(0.25)
            fig.clear()

    def save_as_dat(self, spectrum):
        """
            Creates .dat file for the spectrum
        """
        text = ""
        if spectrum == self.clean_spectrum:
            text = "clean_spectrum.dat"
        elif spectrum == self.dark_spectrum:
            text = "dark_spectrum.dat"
        with open(text, "w") as f:
            for pixel in spectrum:
                f.write("%s\n" % pixel)

    def fetch_dark_spectrum(self):
        """
        Calls the lower level function defined in avinash.py
        to fetch the dark spectrum values as a list.
        """
        # self.dark_spectrum = capture_dark()
        self.dark_spectrum = self.rover.capture_dark()

    def fetch_noisy_spectrum(self):
        """
        Calls the lower level function defined in avinash.py
        to fetch the noisy(raw) spectrum values as a list.
        """
        # self.noisy_spectrum = capture_noisy()
        self.noisy_spectrum = self.rover.capture_noisy()

    def remove_noise(self):
        """
            Subtracts dark spectrum from noisy spectrum
        """
        noisy = np.array(self.noisy_spectrum)
        dark = np.array(self.dark_spectrum)
        self.clean_spectrum = noisy - dark

    def start_acq(self):
        """
            Initialises spectrometer. Sets spectrometer settings (acq time, data mode etc).
            Calls methods to fetches and plot spectrums
        """
        # call spec_init() from avinash.py
        # call function in avinash.py to set settings
        self.rover.spec_init()
        self.rover.spec_mode(self.parameters.get("data_mode"))
        while True:
            if self.parameters["acq_mode"] == "single":

                self.fetch_dark_spectrum()
                self.plot_single(self.dark_spectrum)
                self.save_as_dat(self.dark_spectrum)

                self.fetch_noisy_spectrum()
                self.remove_noise()

                self.plot_single(self.clean_spectrum)
                self.save_as_dat(self.clean_spectrum)

            elif self.parameters["acq_mode"] == "continuous":

                self.fetch_dark_spectrum()
                self.plot_single(self.dark_spectrum)
                self.save_as_dat(self.dark_spectrum)

                self.cont_plot()

            else:
                print("[ERROR]: Incorrect value for acq_mode")


def user_menu(obj):
    """
        User menu that takes input from user and drives program execution
    """
    # flag to prevent spawning another "Start" thread. False means no "Start" thread exists.
    start_status = False

    while True:

        program_command = raw_input("\nEnter Command.....")

        if program_command == "Set" or program_command == "set":
            obj.set_parameters()

        elif ((program_command == "Start" or program_command == "start_status") and start_status is False):
            start_status = True
            acquisition_thread = threading.Thread(target=obj.start_acq)
            acquisition_thread.setDaemon(True)
            acquisition_thread.start()

        elif program_command == "End" or program_command == "end":
            print("Ending spectrum acquisition")
            start_status = False
            break

        else:
            print("[ERROR]: Incorrect command input")


def main():
    print(''' 
    #######################################################################                
                            BTC 110 Spectrometer
                                Team RoverX
    
    
    Parameter Desciption
    #################################################
    1) Number of averages: 1 to 100
    2) Acquisition Time: 100ms to 10s. (Enter value in ms)
    3) Baud Rate: { 115200, 38400, 19200, 9600, 4800, 2400, 1200, 600 }
    4) Data Mode: a (ASCII) or b (Binary)
    5) Acquisition Mode: single or continuous
    
    
    Program Commands
    #################################################
    Type "Set" to set parameters
    Type "Start" to commence spectrum acquisition
    Type "End" to end spectrum acquisition
    
    ''')

    obj = gui()
    user_menu(obj)


if __name__ == "__main__":
    main()
