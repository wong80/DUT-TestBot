import pyvisa
import time
import matplotlib.pyplot as plt

list = []


class DMM(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        self.dmm.timeout = 1000
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.query("*opc?")

    def config(self, *args):
        if len(args) == 1:
            str1 = ""

            for item in args:
                str1 = str1 + item

            self.dmm.write("CONF:" + str1)

        elif len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            self.dmm.write("CONF:" + str1 + ":" + str2)

        elif len(args) == 3:
            str1 = ""
            str2 = ""
            str3 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item

            self.dmm.write("CONF:" + str1 + ":" + str2 + ":" + str3)
            self.dmm.timeout = 1000

    def step_measure(self):
        self.dmm.timeout = 7000
        print(self.dmm.query("READ?"))

    # There is a limit to the resolution of the data
    def cont_measure(self, DURATION, NUMBER_OF_SAMPLES, list):
        self.duration = DURATION
        self.samples = NUMBER_OF_SAMPLES
        self.list = list
        self.dmm.timeout = 7000
        for i in range(int(self.duration)):
            list.append(float(self.dmm.query("READ?")))
            time.sleep(self.duration / self.samples)

        print(list)

    def measure(self, DURATION, period, list, *args):
        self.duration = DURATION
        self.list = list
        self.period = period

        if len(args) == 1:
            str = ""

            for item in args:
                str = str + item

            cmd = "MEAS:" + str + "?"

        elif len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            cmd = "MEAS:" + str1 + ":" + str2 + "?"

        elif len(args) == 3:
            str1 = ""
            str2 = ""
            str3 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item

            cmd = "MEAS:" + str1 + ":" + str2 + ":" + str3 + "?"

        for i in range(int(self.duration)):
            self.dmm.timeout = 7000
            list.append(float(self.dmm.query(cmd)))
            time.sleep(self.period)

        print(list)

    def setFunction(self, *args):
        str1 = ""
        for item in args[0]:
            str1 = str1 + item

        self.dmm.write("CALC:FUNC " + str1)
        self.dmm.write("CALC:STAT ON")

    def setLimit(self, *args):
        str1 = ""
        str2 = ""
        for item in args[0]:
            str1 = str1 + item
        for item in args[1]:
            str2 = str2 + item

        self.dmm.write("CALC:LIM:" + str1 + " " + str2)

    def calcLimit(self, *args):
        str1 = ""
        for item in args:
            str1 = str1 + item

        print(self.dmm.query("CALC:LIM:" + str1 + "?"))

    def calcAverage(self):
        print("Average: " + self.dmm.query("CALC:AVER:AVER?"))

        print("Samples: " + self.dmm.query("CALC:AVER:COUN?"))

        print("Max: " + self.dmm.query("CALC:AVER:MAX?"))

        print("Min: " + self.dmm.query("CALC:AVER:MIN?"))

    def Sense(self, *args):
        if len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            print(str1 + " " + str2 + " has been updated.")
            self.dmm.write("SENS:" + str1 + ":" + str2)

        elif len(args) == 3:
            str1 = ""
            str2 = ""
            str3 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item

            print(str1 + " " + str2 + " " + str3 + " has been updated.")
            self.dmm.write("SENS:" + str1 + ":" + str2 + ":" + str3)
            self.dmm.timeout = 1000

        elif len(args) == 4:
            str1 = ""
            str2 = ""
            str3 = ""
            str4 = ""

            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item
            for item in args[3]:
                str4 = str4 + item

            print(str1 + " " + str2 + " " + str3 + " " + str4 + " has been updated.")
            self.dmm.write("SENS:" + str1 + ":" + str2 + ":" + str3 + ":" + str4)
            self.dmm.timeout = 1000

    def QSense(self, *args):
        if len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            print("\n")
            print(
                "Current status of "
                + str1
                + " "
                + str2
                + ": "
                + self.dmm.query("SENS:" + str1 + ":" + str2 + "?")
            )
            self.dmm.timeout = 1000
        elif len(args) == 3:
            str1 = ""
            str2 = ""
            str3 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item

            print("\n")
            print(
                "Current status of "
                + str1
                + " "
                + str2
                + " "
                + str3
                + ": "
                + self.dmm.query("SENS:" + str1 + ":" + str2 + ":" + str3 + "?")
            )

            self.dmm.timeout = 7000

        elif len(args) == 4:
            str1 = ""
            str2 = ""
            str3 = ""
            str4 = ""

            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item
            for item in args[2]:
                str3 = str3 + item
            for item in args[3]:
                str4 = str4 + item

            print("\n")
            print(
                "Current status of "
                + str1
                + " "
                + str2
                + " "
                + str3
                + " "
                + str4
                + ": "
                + self.dmm.query(
                    "SENS:" + str1 + ":" + str2 + ":" + str3 + ":" + str4 + "?"
                )
            )

            self.dmm.timeout = 1000


class plotGraph:
    def plotting(list):
        plt.plot(list)
        # naming the x axis
        plt.xlabel("x - axis")
        # naming the y axis
        plt.ylabel("y - axis")
        # giving a title to my graph
        plt.title("Graph Title")

        plt.show()


A = DMM("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")
A.config("Primary", "Voltage")
A.Sense("Primary", "Voltage", "AC", "RES FAST")
A.QSense("Primary", "Voltage", "Range")
