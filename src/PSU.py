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
        self.dmm.write("*rst")

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
