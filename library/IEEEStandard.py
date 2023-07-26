import pyvisa


class IEEE_488(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.instr = rm.open_resource(self.VISA_ADDRESS)

    def strtoargs(self, args):
        temp = ""
        for item in args:
            temp = temp + item

        return temp


class CLS(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*CLS")


class ESE(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*ESE?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*ESE")

        if len(*args) == 1:
            self.instr.write("*ESE " + self.strtoargs(args))


class ESR(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        return self.instr.query("*ESR?")


class IDN(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*IDN?")


class OPC(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self):
        self.instr.write("*OPC")

    def query(self):
        return self.instr.query("*OPC?")


class RST(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        return self.instr.query("*RST?")


class PSC(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*PSC?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*PSC")

        elif len(*args) == 1:
            self.instr.write("*PSC " + self.strtoargs(args))


class SRE(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*SRE?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("*SRE")

        if len(*args) == 1:
            self.instr.write("*SRE " + self.strtoargs(args))


class STB(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.query("*STB?")


class TRG(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*TRG")


class TST(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        return self.instr.query("*TST?")


class WAI(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("*WAI")


class RCL(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(*args) == 1:
            self.instr.write("*RCL " + self.strtoargs(args))


class SAV(IEEE_488):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(*args) == 1:
            self.instr.write("*SAV " + self.strtoargs(args))
