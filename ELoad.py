import pyvisa


class N6701C:
    def __init__(self, VISA_ADDRESS):
        # ResourceManager Setup
        self.rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = self.rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.query("*opc?")

    def display(self, *args):
        if len(args) == 1:
            str1 = ""

            for item in args:
                str1 = str1 + item
            self.dmm.write("DISP:" + str1)

        elif len(args) == 2:
            str1 = ""
            str2 = ""
            for item in args[0]:
                str1 = str1 + item
            for item in args[1]:
                str2 = str2 + item

            self.dmm.write("DISP:" + str1 + ":" + str2)

    def setCurrent(self, value, CHANNEL_NUMBER):
        self.dmm.write("CURR " + str(value) + "," + " (@" + str(CHANNEL_NUMBER) + ")")

    def setVoltage(self, value, CHANNEL_NUMBER):
        self.dmm.write("VOLT " + str(value) + "," + " (@" + str(CHANNEL_NUMBER) + ")")

    def function(self, param, CHANNEL_NUMBER):
        self.dmm.write("FUNC " + param + "," + " (@" + str(CHANNEL_NUMBER) + ")")

    def Output(self, state, CHANNEL_NUMBER):
        self.dmm.write("OUTP " + state + "," + " (@" + str(CHANNEL_NUMBER) + ")")

    def voltageSetup(self, minVoltage, maxVoltage, Channel, step_size):
        self.Channel = Channel
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.step_size = step_size
        self.iterations = ((maxVoltage - minVoltage) / step_size) + 1

    def currentSetup(self, minCurrent, maxCurrent, Channel, step_size):
        self.Channel = Channel
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.step_size = step_size
        self.iterations = ((self.maxCurrent - self.minCurrent) / self.step_size) + 1


# A = N6701C("USB0::0x2A8D::0x0102::MY56000223::0::INSTR")
# A.display("Channel 3")
# A.function("Voltage", 3)
# A.setVoltage(2, 3)
# A.Output("ON", 3)
# A.rm.close()
