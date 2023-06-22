import pyvisa
import time
import matplotlib.pyplot as plt


class E36731A(object):
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
        # self.dmm.write("DISP:TEXT " + '"Reality can be whatever I want"')
        self.dmm.write("DISP:TEXT:CLE")

    def apply(self, CHANNEL, VOLTAGE_SET, CURRENT_SET):
        self.Channel = CHANNEL
        self.setVoltage = VOLTAGE_SET
        self.setCurrent = CURRENT_SET

        self.dmm.write(
            "APPL " + self.Channel + "," + self.setVoltage + "," + self.setCurrent
        )

    def Emulate(self, Emul):
        self.emul = Emul
        self.dmm.write("EMUL " + Emul)

    def Output(self, state):
        self.dmm.write("OUTPUT " + state)


A = E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
A.apply("CH1", "7", "2")
A.Output("ON")
time.sleep(5)
A.Output("OFF")
