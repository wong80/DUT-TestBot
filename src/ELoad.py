import pyvisa


class N6701C:
    def __init__(self, VISA_ADDRESS):
        # ResourceManager Setup
        self.rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = self.rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600

        self.dmm.write("*rst")

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
