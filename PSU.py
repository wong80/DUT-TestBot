import pyvisa
import time
import matplotlib.pyplot as plt
import array

infoList = []


class E36731A(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        self.rm = rm
        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource(self.VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        self.dmm.timeout = 1000
        print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        # self.dmm.query("*opc?")
        # # self.dmm.write("DISP:TEXT " + '"Reality can be whatever I want"')
        # self.dmm.write("DISP:TEXT:CLE")

        # self.Output("ON")
        self.testSetup(1, 30, 2, "CH1", 1, infoList)
        # self.Output("OFF")
        # rm.close()

    def apply(self, VOLTAGE_SET, CURRENT_SET):
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
        # self.dmm.query("OPC?")

    def Emulate(self, Emul):
        self.emul = Emul
        self.dmm.write("EMUL " + Emul)

    def Output(self, state):
        self.dmm.write("OUTPUT " + state)

    def testSetup(self, minVoltage, maxVoltage, Current, Channel, step_size, infoList):
        self.infoList = infoList
        self.Channel = Channel
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.Current = Current
        self.step_size = step_size
        self.iterations = (maxVoltage - minVoltage + 1) / step_size

        # k = minVoltage
        # i = 0
        # while k <= maxVoltage:
        #     self.dmm.write(
        #         "APPL " + self.Channel + "," + str(k) + "," + str(self.Current)
        #     )
        #     print("Voltage:  Current:    ")
        #     print(self.dmm.query("APPL?"))
        #     self.infoList.insert(i, [k, self.Current])
        #     time.sleep(2.18)

        #     k += step_size
        #     i += 1
        # print(self.infoList)


# A = E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
# A.execute()
# A.Output("ON")
# A.testFunc(1, 5, 3, "CH1", 1, infoList)
# A.Output("OFF")
