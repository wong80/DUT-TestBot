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

    def strtoargs(self, args):
        temp = ""
        for item in args:
            temp = temp + item

        return temp


class Channel(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setChannelNumber(self, Channel_Number):
        self.instr.write("CHAN " + str(Channel_Number))

    def setChannelMode(self, Mode):
        self.instr.write("CHAN:ACT " + str(Mode))


class Mode(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setMode(self, Mode):
        self.instr.write("MODE " + str(Mode))


class Voltage(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCurrentLimit(self, value):
        self.instr.write("VOLT:STAT:ILIM " + str(value))


class Show(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def Display(self, Channel):
        self.instr.write("SHOW:DISP " + str(Channel))
