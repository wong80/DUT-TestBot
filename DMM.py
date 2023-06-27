import pyvisa
import time
import matplotlib.pyplot as plt

dataList = []


class EDU34450A(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        self.rm = rm
        # Visa Address is found under Keysight Connection Expert
        self.dmm = self.rm.open_resource(self.VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        # self.dmm.query("*opc?")

        # self.config("Primary", "Voltage")
        # self.Sense("Voltage", "DC", "RES FAST")
        # self.execute()

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

    def step_measure(self):
        self.dmm.timeout = 7000
        print(self.dmm.query("READ?"))

    # There is a limit to the resolution of the data
    def cont_measure(self):
        self.dataList = dataList
        self.dmm.timeout = 7000

        dataList.append(float(self.dmm.query("READ?")))

        print(dataList)

    def measure(self, DURATION, period, dataList, *args):
        self.duration = DURATION
        self.dataList = dataList
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
            self.dmm.timeout = 3000
            self.dataList.insert(i, [float(self.dmm.query(cmd))])
            time.sleep(0.5)

        # print(dataList)

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

    def execute(self):
        self.measure(30, 1, dataList, "Voltage", "DC")
        # self.rm.close()


class plotGraph:
    def plotting(self, list):
        plt.plot(list)
        # naming the x axis
        plt.xlabel("x - axis")
        # naming the y axis
        plt.ylabel("y - axis")
        # giving a title to my graph
        plt.title("Graph Title")

        plt.show()


class N6701C(EDU34450A):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.query("*opc?")

    def measure(self, DURATION, period, list, CHANNEL_NUMBER, *args):
        self.duration = DURATION
        self.list = list
        self.period = period

        if len(args) == 1:
            local_str = ""

            for item in args:
                local_str = local_str + item

            cmd = "MEAS:" + local_str + "?" + " (@" + str(CHANNEL_NUMBER) + ")"

        elif len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            cmd = "MEAS:" + str1 + ":" + str2 + "?" + " (@" + str(CHANNEL_NUMBER) + ")"

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

            cmd = (
                "MEAS:"
                + str1
                + ":"
                + str2
                + ":"
                + str3
                + "?"
                + " (@"
                + str(CHANNEL_NUMBER)
                + ")"
            )

        for i in range(int(self.duration)):
            # self.dmm.timeout = 10000
            # print(cmd)
            list.append(float(self.dmm.query(cmd)))
            time.sleep(self.period)

        print(list)

    def Output(self, state, CHANNEL_NUMBER):
        self.channel_number = CHANNEL_NUMBER
        self.dmm.write("OUTPUT " + state + "," + " (@" + CHANNEL_NUMBER + ")")

    def setCurrent(self, value, CHANNEL_NUMBER):
        self.dmm.write("CURR " + value + "," + " (@" + CHANNEL_NUMBER + ")")

    def Measure(self, param, CHANNEL_NUMBER):
        print(self.dmm.query("MEAS:" + param + "?" + " (@" + CHANNEL_NUMBER + ")"))

    def testFunc(self):
        print("test")


# A = EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")
# A.Sense("Voltage", "DC", "RES FAST")
# A.config("Primary", "Voltage")
# A.measure(5, 1, dataList, "Voltage", "DC")


# B = N6701C("USB0::0x2A8D::0x0102::MY56000223::0::INSTR")
# B.Output("ON", "3")
# B.setCurrent("1", "3")
# B.measure(50, 0.1, list, 3, "Current")
# C = plotGraph()
# C.plotting(list)
