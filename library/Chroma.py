import pyvisa


class Subsystem(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        try:
            # Visa Address is found under Keysight Connection Expert
            self.instr = rm.open_resource(self.VISA_ADDRESS)

        except pyvisa.VisaIOError as e:
            print(e.args)


class Channel(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setChannelNumber(self, Channel_Number):
        self.instr.write(f"CHAN {Channel_Number}")

    def setChannelMode(self, Mode):
        self.instr.write(f"CHAN:ACT {Mode}")


class Mode(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setMode(self, Mode):
        self.instr.write(f"MODE {Mode}")


class Voltage(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCurrentLimit(self, value):
        self.instr.write(f"VOLT:STAT:ILIM {value}")


class Show(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def Display(self, Channel):
        self.instr.write(f"SHOW:DISP {Channel}")
