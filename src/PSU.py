import pyvisa

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
        # print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.write("VOLT:SENSE:SOUR EXT,(@1)")
        # # self.dmm.write("DISP:TEXT " + '"Reality can be whatever I want"')
        # self.dmm.write("DISP:TEXT:CLE")

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

    def Emulate(self, Emul):
        self.emul = Emul
        self.dmm.write("EMUL " + Emul)

    def Output(self, state):
        self.dmm.write("OUTPUT " + state)

    def Voltage_Sweep(self, minVoltage, maxVoltage, Current, Channel, step_size):
        self.Channel = Channel
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.Current = Current
        self.step_size = step_size
        self.iterations = ((maxVoltage - minVoltage) / step_size) + 1

    def Current_Sweep(self, minCurrent, maxCurrent, Voltage, Channel, step_size):
        self.Channel = Channel
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.Voltage = Voltage
        self.step_size = step_size
        self.iterations = ((maxCurrent - minCurrent) / step_size) + 1


# A = E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
