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


class Current(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputCurrent(self, Current, ChannelNumber):
        self.instr.write("CURR " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def OutputCurrentStepSize(self, Current, ChannelNumber):
        self.instr.write("CURR:STEP " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setTriggeredCurrent(self, Current, ChannelNumber):
        self.instr.write("CURR:TRIG " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setCurrentLimit(self, Current, ChannelNumber):
        self.instr.write("CURR:LIM " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setCurrentMode(self, Mode, ChannelNumber):
        self.instr.write("CURR:MODE " + Mode + ",(@" + str(ChannelNumber) + ")")

    def CLECurrentProtection(self, ChannelNumber):
        self.instr.write("CURR:PROT:CLE (@" + str(ChannelNumber) + ")")

    def setProtectionDelay(self, delay_time, ChannelNumber):
        self.instr.write(
            "CURR:PROT:DEL " + str(delay_time) + ",(@" + str(ChannelNumber) + ")"
        )

    def enableCurrentProtection(self, state, ChannelNumber):
        self.instr.write(
            "CURR:PROT:STAT " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def queryCurrentTrip(self):
        return self.instr.query("CURR:PROT:TRIP?")

    def setCurrentRange(self, range, ChannelNumber):
        self.instr.write("CURR:RANG " + str(range) + ",(@" + str(ChannelNumber) + ")")

    def enableLowRangeCurrent(self, mode):
        self.instr.write("CURR:SENS:LOW " + str(mode))

    def setPositiveSlew(self, Current, ChannelNumber):
        self.instr.write("CURR:SLEW " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setNegativeSlew(self, Current, ChannelNumber):
        self.instr.write(
            "CURR:SLEW:NEG " + str(Current) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTransInput(self, Current, ChannelNumber):
        self.instr.write("CURR:TLEV " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setTerminal(self, terminal):
        self.instr.write("CURR:TERM " + str(terminal))

    def setApertureTime(self, seconds):
        self.instr.write("CURR:DC:APER " + str(seconds))

    def setNPLC(self, value):
        self.instr.write("CURR:DC:NPLC " + str(value))

    def setAutoZero(self, state):
        self.instr.write("SYST:AZER:STAT " + state)


class System(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)


class Voltage(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputVoltage(self, Current, ChannelNumber):
        self.instr.write("VOLT " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def OutputVoltageStepSize(self, Current, ChannelNumber):
        self.instr.write("VOLT:STEP " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setTriggeredVoltage(self, Current, ChannelNumber):
        self.instr.write("VOLT:TRIG " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setVoltageLimit(self, Current, ChannelNumber):
        self.instr.write("VOLT:LIM " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setVoltageMode(self, Mode, ChannelNumber):
        self.instr.write("VOLT:MODE " + Mode + ",(@" + str(ChannelNumber) + ")")

    def CLEVoltageProtection(self, ChannelNumber):
        self.instr.write("VOLT:PROT:CLE (@" + str(ChannelNumber) + ")")

    def setProtectionDelay(self, delay_time, ChannelNumber):
        self.instr.write(
            "VOLT:PROT:DEL " + str(delay_time) + ",(@" + str(ChannelNumber) + ")"
        )

    def enableVoltageProtection(self, state, ChannelNumber):
        self.instr.write(
            "VOLT:PROT:STAT " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTripVoltage(self, voltage, ChannelNumber):
        self.instr.write("VOLT:PROT " + str(voltage) + ",(@" + str(ChannelNumber) + ")")

    def setVoltageRange(self, range, ChannelNumber):
        self.instr.write("VOLT:RANG " + str(range) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlew(self, Current, ChannelNumber):
        self.instr.write("VOLT:SLEW " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setNegativeSlew(self, Current, ChannelNumber):
        self.instr.write(
            "VOLT:SLEW:NEG " + str(Current) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTransInput(self, Current, ChannelNumber):
        self.instr.write("VOLT:TLEV " + str(Current) + ",(@" + str(ChannelNumber) + ")")

    def setSlewTracking(self, mode, ChannelNumber):
        self.instr.write(
            "VOLT:SLEW COUP " + str(mode) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTransientPower(self, power, ChannelNumber):
        self.instr.write("VOLT:TLEV " + str(power) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "VOLT:SLEW:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setNegativeSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "VOLT:SLEW:NEG:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setSenseMode(self, state, ChannelNumber):
        self.instr.write(
            "VOLT:SENS:SOUR " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def specifyVoltageOn(self, Voltage, ChannelNumber):
        self.instr.write(
            "VOLT:INH:VON " + str(Voltage) + ",(@" + str(ChannelNumber) + ")"
        )

    def setInhibMode(self, mode, ChannelNumber):
        self.instr.write(
            "VOLT:INH:VON:MODE " + str(mode) + ",(@" + str(ChannelNumber) + ")"
        )

    def setApertureMode(self, mode):
        self.instr.write("VOLT:APER:ENAB " + str(mode))

    def setApertureTime(self, seconds):
        self.instr.write("VOLT:DC:APER " + str(seconds))

    def setNPLC(self, value):
        self.instr.write("VOLT:DC:NPLC " + str(value))

    def setAutoZero(self, state):
        self.instr.write("SYST:AZER:STAT " + state)

    def setAutoImpedanceMode(self, mode):
        self.instr.write("VOLT:IMP:AUTO " + str(mode))


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


class Measure(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def singleChannelQuery(self, *args):
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

    def multipleChannelQuery(self, ChannelNumber, *args):
        if len(args) == 1:
            return self.instr.query(
                "MEAS:" + self.strtoargs(args) + "? " + "(@" + str(ChannelNumber) + ")"
            )

        elif len(args) == 2:
            return self.instr.query(
                "MEAS:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + "? "
                + "(@"
                + str(ChannelNumber)
                + ")"
            )


class Trigger(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setCount(self, num):
        self.instr.write("TRIG:COUN " + str(num))

    def queryCount(self, *args):
        return self.instr.query("TRIG:COUN? " + self.strtoargs(*args))

    def setSource(self, *args):
        self.instr.write("TRIG:SOUR " + self.strtoargs(*args))

    def querySource(self):
        return self.instr.query("TRIG:SOUR?")

    def triggerAcquire(self, ChannelNumber):
        self.instr.write("TRIG:ACQ (@" + str(ChannelNumber) + ")")

    def setTriggeredCurrent(self, value, ChannelNumber):
        self.instr.write(
            "TRIG:ACQ:CURR " + str(value) + ",(@" + str(ChannelNumber) + ")"
        )

    def setCurrentSlope(self, state, ChannelNumber):
        self.instr.write(
            "TRIG:ACQ:CURR:SLOP " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTriggeredVoltage(self, value, ChannelNumber):
        self.instr.write(
            "TRIG:ACQ:VOLT " + str(value) + ",(@" + str(ChannelNumber) + ")"
        )

    def setVoltageSlope(self, state, ChannelNumber):
        self.instr.write(
            "TRIG:ACQ:VOLT:SLOP " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTriggerDelay(self, time):
        self.instr.write("TRIG:DEL " + str(time))
