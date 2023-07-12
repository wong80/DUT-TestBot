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


class Calibration(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def calibration(self):
        return self.instr.query("CAL?")

    def calibrationCount(self):
        return self.instr.query("CAL:COUN?")

    def setSecureCode(self, new_code):
        self.instr.write("CAL:SEC:CODE " + self.strtoargs(new_code))

    def setSecureState(self, state):
        self.instr.write("CAL:SEC:STAT " + self.strtoargs(state))

    def querySecureState(self):
        return self.instr.query("CAL:SEC:STAT?")

    def calibrationString(self, string):
        self.instr.write('CAL:STR "' + self.strtoargs(string) + '"')

    def calibrationValue(self, value):
        self.instr.write("CAL:VAL " + self.strtoargs(value))

    def calibrationStore(self):
        self.instr.write("CAL:STOR")


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


class LXI(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setIdentityState(self, state):
        self.instr.write("LXI:IDEN " + self.strtoargs(state))

    def queryIdentityState(self):
        return self.instr.query("LXI:IDEN?")

    def setMDNS(self, state):
        self.instr.write("LXI:MDNS:ENAB" + self.strtoargs(state))

    def queryMDNShost(self):
        return self.instr.query("LXI:MDNS:ENAB?")

    def resolvedMDNS(self):
        return self.instr.query("LXI:MDNS:HNAM:RES?")

    def setMDNSName(self, name):
        self.instr.write('LXI:MDNS:SNAM:DES "' + self.strtoargs(name) + '"')

    def queryMDNSName(self):
        return self.instr.query("LXI:MDNS:SNAM:DES?")

    def queryMDSNservice(self):
        return self.instr.query("LAXI:MDNS:SNAM:RES?")

    def reset(self):
        self.dmm.write("LXI:RES")

    def restart(self):
        self.dmm.write("LXI:REST")


class Measure(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def config(self, *args):
        if len(args) == 1:
            self.instr.write("MEAS:" + self.strtoargs(args))

        elif len(args) == 2:
            self.instr.write(
                "MEAS:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

        elif len(args) == 3:
            self.instr.write(
                "MEAS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.instr.query("MEAS:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.instr.query(
                "MEAS:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )

        elif len(args) == 3:
            return self.instr.query(
                "MEAS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + "?"
            )


class Memory(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(args) == 1:
            self.instr.write("MEM:STAT:" + self.strtoargs(args))

        elif len(args) == 2:
            self.instr.write(
                "MEM:STAT:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.instr.query("MEM:STAT:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.instr.query(
                "MEM:STAT:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + "?"
            )


class Read(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)
        return self.instr.query("READ?")


class Sample(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        self.instr.write("SAMP:" + self.strtoargs(args))

    def query(self, *args):
        return self.instr.query("SAMP:" + self.strtoargs(args) + "?")


class Sense(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, *args):
        if len(args) == 1:
            self.instr.write("SENS:" + self.strtoargs(args))

        elif len(args) == 2:
            self.instr.write(
                "SENS:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1])
            )

        elif len(args) == 3:
            self.instr.write(
                "SENS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
            )

        elif len(args) == 4:
            self.instr.write(
                "SENS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + ":"
                + self.strtoargs(args[3])
            )

    def query(self, *args):
        if len(args) == 1:
            return self.instr.query("SENS:" + self.strtoargs(args) + "?")

        elif len(args) == 2:
            return self.instr.query(
                "SENS:" + self.strtoargs(args[0]) + ":" + self.strtoargs(args[1]) + "?"
            )

        elif len(args) == 3:
            return self.instr.query(
                "SENS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + "?"
            )

        elif len(args) == 4:
            return self.instr.query(
                "SENS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + ":"
                + self.strtoargs(args[2])
                + ":"
                + self.strtoargs(args[3])
                + "?"
            )


class Status(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def operationCondition(self):
        return self.instr.query("STAT:OPER:COND?")

    def operationEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:OPER:ENAB")

        elif len(*args) == 1:
            self.instr.write("STAT:OPER:ENAB " + self.strtoargs(args))

    def statusOperation(self):
        return self.instr.query("STAT:OPER?")

    def preset(self):
        return self.instr.query("STAT:PRES")

    def questionableCondition(self):
        return self.instr.query("STAT:QUES:COND?")

    def questionableEnable(self, *args):
        if len(*args) == 0:
            self.instr.write("STAT:QUES:ENAB")

        elif len(*args) == 1:
            self.instr.write("STAT:QUEST:ENAB " + self.strtoargs(args))

    def questionableCondition(self):
        return self.instr.query("STAT:QUES?")


class System(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def beeper(self):
        self.instr.write("SYST:BEEP")

    def beeperStatus(self, *args):
        self.instr.write("SYST:BEEP:STAT " + self.strtoargs(args))

    def LANControl(self):
        return self.instr.query("SYST:COMM:LAN:CONT?")

    def LAN_DHCP(self, *args):
        self.instr.write("SYST:COMM:DHCP " + self.strtoargs(args))

    def LAN_DNS(self, DNS_Address):
        self.instr.write('SYST:COMM:DNS "' + self.strtoargs(DNS_Address) + '"')

    def LAN_Domain(self):
        return self.instr.query("SYST:COMM:LAM:DOM?")

    def LAN_DNS(self, DNS_Address):
        self.instr.write('SYST:COMM:DNS "' + self.strtoargs(DNS_Address) + '"')

    def LAN_GATE(self, Gate_Address):
        self.instr.write('SYST:COMM:LAN:GATE "' + self.strtoargs(Gate_Address) + '"')

    def LAN_Host(self, HostName):
        self.instr.write('SYST:COMM:LAN:HOST "' + self.strtoargs(HostName) + '"')

    def LAN_IP(self, IP_Address):
        self.instr.write('SYST:COMM:LAN:IPAD "' + self.strtoargs(IP_Address) + '"')

    def LAN_MAC(self):
        return self.instr.query("SYST:COMM:LAN:MAC?")

    def LAN_SMask(self, mask):
        self.instr.write('SYST:COMM:LAN:SMAS "' + self.strtoargs(mask) + '"')

    def TELN_WMsg(self, string):
        self.instr.write('SYST:COMM:LAN:TELN:WMES "' + self.strtoargs(string) + '"')

    def LAN_Update(self):
        self.instr.write("SYSTS:COMM:LAN:UPD")

    def TCP_Control(self):
        return self.instr.query("SYST:COMM:TCP:CONT?")

    def setDate(self, YYYY, MM, DD):
        self.instr.write(
            "SYST:DATE "
            + self.strtoargs(YYYY)
            + ","
            + self.strtoargs(MM)
            + ","
            + self.strtoargs(DD)
        )

    def queryDate(self):
        return self.instr.query("DATE?")

    def setLFrequency(self, delay_time):
        self.instr.write("SYST:LFR " + self.strtoargs(delay_time))

    def queryLFrequency(self):
        return self.instr.query("SYST:LFR?")

    def systemLocal(self):
        self.instr.write("SYST:LOC")

    def systemPreset(self):
        self.instr.write("SYST:PRES")

    def setSystemState(self, stateNo):
        self.instr.write("SYST:SET " + self.strtoargs(stateNo))

    def setTime(self, hh, mm, ss):
        self.instr.write(
            "SYST:TIME "
            + self.strtoargs(hh)
            + ","
            + self.strtoargs(mm)
            + ","
            + self.strtoargs(ss)
        )

    def queryTime(self):
        return self.instr.query("SYST:TIME?")

    def version(self):
        return self.instr.query("SYST:VERS?")


class Trigger(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCount(self, *args):
        self.instr.write("TRIG:COUN " + self.strtoargs(*args))

    def queryCount(self, *args):
        return self.instr.query("TRIG:COUN? " + self.strtoargs(*args))

    def setSource(self, *args):
        self.instr.write("TRIG:SOUR" + self.strtoargs(*args))

    def querySource(self):
        return self.instr.query("TRIG:SOUR?")


class Unit(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setTemp(self, units):
        self.instr.write("UNIT:TEMP " + self.strtoargs(units))

    def queryTemp(self):
        return self.instr.query("UNIT:TEMP?")
