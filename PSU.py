import pyvisa
import time
import matplotlib.pyplot as plt
import array

dataList = []


class E36731A(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup

        rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource("USBInstrument2")
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        self.dmm.timeout = 1000
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.query("*opc?")
        # self.dmm.write("DISP:TEXT " + '"Reality can be whatever I want"')
        # self.dmm.write("DISP:TEXT:CLE")
        rm.close()

    def apply(self, CHANNEL, VOLTAGE_SET, CURRENT_SET):
        self.Channel = CHANNEL
        self.setVoltage = VOLTAGE_SET
        self.setCurrent = CURRENT_SET

        self.dmm.write(
            "APPL "
            + self.Channel
            + ","
            + str(self.setVoltage)
            + ","
            + str(self.setCurrent)
        )

    def Emulate(self, Emul):
        self.emul = Emul
        self.dmm.write("EMUL " + Emul)

    def Output(self, state):
        self.dmm.write("OUTPUT " + state)

    def testFunc(self, minVoltage, maxVoltage, Current, Channel, step_size, dataList):
        self.dataList = dataList
        self.Channel = Channel
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.Current = Current
        self.step_size = step_size

        k = minVoltage
        i = 0
        while k <= maxVoltage:
            self.dmm.write(
                "APPL " + self.Channel + "," + str(k) + "," + str(self.Current)
            )
            print("Voltage:  Current:    ")
            print(self.dmm.query("APPL?"))
            self.dataList.insert(i, [k, self.Current])
            time.sleep(self.step_size)

            k += step_size
            i += 1
        print(self.dataList)


A = E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
# A.Output("ON")
# A.testFunc(5, 10, 2, "CH1", 0.5, dataList)
# A.Output("OFF")
