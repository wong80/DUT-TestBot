import pyvisa


class Subsystem(object):
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


class Abort(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

        self.instr.write("ABOR")


class Calculate(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def function(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:FUNC " + self.strtoargs(args))

    def state(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:STAT " + self.strtoargs(args))

    def limit_lower(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:LIM:LOW " + self.strtoargs(args))

    def limit_lower(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:LIM:UPP " + self.strtoargs(args))

    def Average(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:AVER:" + self.strtoargs(args) + "?")

    def DBref(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:DB:REF " + self.strtoargs(args))

    def offset(self, *args):
        if len(*args) == 1:
            self.instr.write("CALC:NULL:OFFS " + self.strtoargs(args))

    def query(self, ans):
        return self.instr.query(ans)


class Configure(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(args) == 1:
            self.dmm.write("CONF:" + self.strtoargs(args))

        elif len(args) == 2:
            self.dmm.write(
                "CONF:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

        elif len(args) == 3:
            self.dmm.write(
                "CONF:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.dmm.query("CONF:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.dmm.query(
                "CONF:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )

        elif len(args) == 3:
            return self.dmm.query(
                "CONF:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + "?"
            )


class Data(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def data(self):
        return self.instr.query("DATA:DATA? NVMEM")

    def delete(self):
        self.instr.query("DATA:DEL NVMEM")

    def last(self):
        return self.instr.query("DATA:LAST?")

    def datapoints(self):
        return self.instr.query("DATA:POIN? NVMEM")


class Display(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def display(self, *args):
        if len(args) == 1:
            self.dmm.write("DISP:" + self.strtoargs(args))

        elif len(args) == 2:
            self.dmm.write(
                "DISP:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.dmm.query("DISP:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            self.dmm.query(
                "DISP:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )


class Fetch(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)
        return self.instr.query("FETC?")


class Format(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("*FORM:OUTP?")

    def write(self, *args):
        if len(*args) == 0:
            self.instr.write("FORM:OUTP " + self.strtoargs(args))


class Initiate(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)
        self.instr.write("INIT")


class Measure(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def config(self, *args):
        if len(args) == 1:
            self.dmm.write("CONF:" + self.strtoargs(args))

        elif len(args) == 2:
            self.dmm.write(
                "CONF:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

        elif len(args) == 3:
            self.dmm.write(
                "CONF:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.dmm.query("CONF:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.dmm.query(
                "CONF:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )

        elif len(args) == 3:
            return self.dmm.query(
                "CONF:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + "?"
            )
