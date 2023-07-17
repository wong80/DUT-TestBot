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

    def abort_acquire(self, Channel_Number):
        self.instr.write("ABOR:ACQ+(@" + str(Channel_Number) + ")")

    def abort_dlog(self):
        self.instr.write("ABOR:DLOG")

    def abort(self, Channel_Number):
        self.instr.write("ABOR (@" + str(Channel_Number) + ")")


class Apply(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def write(self, Channel_Number, Voltage, Current):
        self.instr.write(
            "APPL CH" + str(Channel_Number) + "," + str(Voltage) + "," + str(Current)
        )


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

    def displayState(self, state):
        self.instr.write("DISP:CHAN " + str(state))

    def displayText(self, string):
        self.instr.write('DISP:TEXT "' + str(string) + '"')

    def clearDisplayText(self):
        self.instr.write("DISP:TEXT:CLE")


class Emul(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def Emulate(self, mode):
        self.instr.write("EMUL " + str(mode))


class Fetch(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("FETC?")

    def query2(self, ChannelNumber, *args):
        if len(args) == 1:
            return self.instr.query(
                "FETC:" + self.strtoargs(args) + "? (@" + str(ChannelNumber) + ")"
            )

        elif len(args) == 2:
            return self.instr.query(
                "FETC:"
                + self.strtoargs(args[0])
                + ":"
                + self.strtoargs(args[1])
                + "? (@"
                + str(ChannelNumber)
                + ")"
            )


class Function(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setMode(self, MODE, ChannelNumber):
        self.instr.write("FUNC " + str(MODE) + ",(@" + str(ChannelNumber) + ")")


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

    def initiate(self):
        self.instr.write("INIT")

    def initiateAcquire(self, ChannelNumber):
        self.instr.write("INIT:ACQ (@" + str(ChannelNumber) + ")")

    def initiateDLog(self, filename):
        self.instr.write("INIT:DLOG " + str(filename))

    def initiateContinuous(self, state, ChannelNumber):
        self.instr.write(
            "INIT:CONT:TRAN " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )


class Output(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setOutputState(self, state):
        self.instr.write("OUTP " + str(state))

    def setOutputStateC(self, state, ChannelNumber):
        self.instr.write("OUTP " + str(state) + ",(@" + str(ChannelNumber) + ")")

    def coupleChannel(self, ChannelNumber):
        self.instr.write("OUTP:COUP:CHAN CH" + str(ChannelNumber))

    def setDelayOn(self, delay_time, ChannelNumber):
        self.instr.write(
            "OUTP:DEL:FALL " + str(delay_time) + ",(@" + str(ChannelNumber) + ")"
        )

    def setDelayOff(self, delay_time, ChannelNumber):
        self.instr.write(
            "OUTP:DEL:RISE " + str(delay_time) + ",(@" + str(ChannelNumber) + ")"
        )

    def setOutputMode(self, Mode, ChannelNumber):
        self.instr.write("OUTP:PMOD " + str(Mode) + ",(@" + str(ChannelNumber) + ")")

    def setInhibMode(self, Mode):
        self.instr.write("OUTP:INH:MODE " + str(Mode))

    def setPowerOnState(self, state):
        self.instr.write("OUTP:PON:STAT " + str(state))

    def clearLatchProtection(self, ChannelNumber):
        self.instr.write("INP:PRO:CLE (@" + str(ChannelNumber) + ")")

    def setRelayState(self, state):
        self.instr.write("OUTP:REL " + str(state))

    def shortInput(self, state):
        self.instr.write("INP:SHOR " + str(state))


class List(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setListCount(self, range, ChannelNumber):
        self.instr.write("LIST:COUN " + str(range) + ",(@" + str(ChannelNumber) + ")")

    def setCurrentList(self, list, ChannelNumber):
        self.instr.write("LIST:CURR " + str(list) + ",(@" + str(ChannelNumber) + ")")

    def queryCurrentPoints(self, ChannelNumber):
        self.instr.write("LIST:CURR:POIN? (@)" + str(ChannelNumber) + ")")


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


class MMemory(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def exportData(self, filename):
        self.instr.write("MMEM:EXP:DLOG " + str(filename))


class Power(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setInputPower(self, value, ChannelNumber):
        self.instr.write("POW " + str(value) + "(@" + str(ChannelNumber) + ")")

    def setTrigPower(self, value, ChannelNumber):
        self.instr.write("POW:TRIG " + str(value) + "(@" + str(ChannelNumber) + ")")

    def setPowerMode(self, mode, ChannelNumber):
        self.instr.write("POW:MODE " + str(mode) + ",(@" + str(ChannelNumber) + ")")

    def setProtectionDelay(self, delaytime, ChannelNumber):
        self.instr.write(
            "POW:PROT:DEL " + str(delaytime) + ",(@" + str(ChannelNumber) + ")"
        )

    def setProtectionState(self, state, ChannelNumber):
        self.instr.write(
            "POW:PROT:STAT " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setPowerRange(self, range, ChannelNumber):
        self.instr.write("POW:RANG " + str(range) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlew(self, rate, ChannelNumber):
        self.instr.write("POW:SLEW " + str(rate) + ",(@" + str(ChannelNumber) + ")")

    def setNegativeSlew(self, rate, ChannelNumber):
        self.instr.write("POW:SLEW:NEG " + str(rate) + ",(@" + str(ChannelNumber) + ")")

    def setSlewTracking(self, mode, ChannelNumber):
        self.instr.write(
            "POW:SLEW COUP " + str(mode) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTransientPower(self, power, ChannelNumber):
        self.instr.write("POW:TLEV " + str(power) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "POW:SLEW:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setNegativeSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "POW:SLEW:NEG:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )


class Read(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def query(self):
        return self.instr.query("READ?")


class Resistance(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setInputResistance(self, value, ChannelNumber):
        self.instr.write("RES " + str(value) + "(@" + str(ChannelNumber) + ")")

    def setTrigResistance(self, value, ChannelNumber):
        self.instr.write("RES:TRIG " + str(value) + "(@" + str(ChannelNumber) + ")")

    def setResistanceMode(self, mode, ChannelNumber):
        self.instr.write("RES:MODE " + str(mode) + ",(@" + str(ChannelNumber) + ")")

    def setResistanceRange(self, range, ChannelNumber):
        self.instr.write("RES:RANG " + str(range) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlew(self, rate, ChannelNumber):
        self.instr.write("RES:SLEW " + str(rate) + ",(@" + str(ChannelNumber) + ")")

    def setNegativeSlew(self, rate, ChannelNumber):
        self.instr.write("RES:SLEW:NEG " + str(rate) + ",(@" + str(ChannelNumber) + ")")

    def setSlewTracking(self, mode, ChannelNumber):
        self.instr.write(
            "RES:SLEW COUP " + str(mode) + ",(@" + str(ChannelNumber) + ")"
        )

    def setTransientPower(self, power, ChannelNumber):
        self.instr.write("RES:TLEV " + str(power) + ",(@" + str(ChannelNumber) + ")")

    def setPositiveSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "RES:SLEW:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def setNegativeSlewOverride(self, state, ChannelNumber):
        self.instr.write(
            "RES:SLEW:NEG:MAX " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )


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

    def setVoltageRangeDC(self, range):
        self.instr.write("VOLT:RANG " + str(range))

    def setVoltageResDC(self, string):
        self.instr.write("VOLT:RES " + str(string))

    def setVoltageRangeAC(self, range):
        self.instr.write("VOLT:AC:RANG " + str(range))

    def setVoltageResAC(self, string):
        self.instr.write("VOLT:AC:RES " + str(string))

    def setCurrentRangeDC(self, range):
        self.instr.write("CURR:RANG " + str(range))

    def setCurrentResDC(self, string):
        self.instr.write("CURR:RES " + str(string))

    def setCurrentRangeAC(self, range):
        self.instr.write("CURR:AC:RANG " + str(range))

    def setCurrentResAC(self, string):
        self.instr.write("CURR:AC:RES " + str(string))

    def setResistanceRange(self, range):
        self.instr.write("RES:RANG " + str(range))

    def setResistanceRes(self, string):
        self.instr.write("RES:RES " + str(string))

    def setResistanceOCompensated(self, string):
        self.instr.write("RES:OCOM " + str(string))

    def setFResistanceRange(self, range):
        self.instr.write("FRES:RANG " + str(range))

    def setFResistanceRes(self, string):
        self.instr.write("FRES:RES " + str(string))

    def setFResistanceOCompensated(self, string):
        self.instr.write("FRES:OCOM " + str(string))

    def setFrequencyAperture(self, value):
        self.instr.write("FREQ:APER " + str(value))

    def setFrequencyVoltageRange(self, value):
        self.instr.write("FREQ:VOLT:RANG " + str(value))

    def setFrequencyCurrentRange(self, value):
        self.instr.write("FREQ:CURR:RANG " + str(value))

    def setThermsistorResistance(self, value):
        self.instr.write("TEMP:TRAN:THER:TYPE " + str(value))

    def setCapacitanceRange(self, range):
        self.instr.write("CAP:RANG " + str(range))

    def enableCurrentDataLogging(self, state, ChannelNumber):
        self.instr.write(
            "SENS:DLOG:FUNC:VOLT " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def enableCurrentDataLogging(self, state, ChannelNumber):
        self.instr.write(
            "SENS:DLOG:FUNC:CURR " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def enableMinMaxLogging(self, state):
        self.instr.write("SENS:DLOG:FUNC:MINM " + str(state))

    def setTriggerOffset(self, offset_percent):
        self.instr.write("SENS:DLOG:OFFS " + str(offset_percent))

    def setSamplePeriod(self, time):
        self.instr.write("SENS:DLOG:PER " + str(time))

    def setSampleDuration(self, time):
        self.instr.write("SENS:DLOG:TIME " + str(time))

    def enableCurrentMeasurement(self, state, ChannelNumber):
        self.instr.write(
            "SENS:FUNC:CURR " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def enableVoltageMeasurement(self, state, ChannelNumber):
        self.instr.write(
            "SENS:FUNC:VOLT " + str(state) + ",(@" + str(ChannelNumber) + ")"
        )

    def specifySweepPoint(self, data_points, ChannelNumber):
        self.instr.write(
            "SENS:SWE:POIN " + str(data_points) + ",(@" + str(ChannelNumber) + ")"
        )

    def specifyOffsetSweepPoint(self, data_points, ChannelNumber):
        self.instr.write(
            "SENS:SWE:OFFS:POIN " + str(data_points) + ",(@" + str(ChannelNumber) + ")"
        )

    def specifyIntervalPoints(self, time, ChannelNumber):
        self.instr.write(
            "SENS:SWE:TINT " + str(time) + ",(@" + str(ChannelNumber) + ")"
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


class Transient(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setTransientCount(self, value, ChannelNumber):
        self.instr.write("TRAN:COUN " + str(value) + ",(@" + str(ChannelNumber) + ")")

    def setDutyCycle(self, value, ChannelNumber):
        self.instr.write("TRAN:DCYC " + str(value) + ",(@" + str(ChannelNumber) + ")")

    def setTransientFrequency(self, value, ChannelNumber):
        self.instr.write("TRAN:FREQ " + str(value) + ",(@" + str(ChannelNumber) + ")")

    def setTransientMode(self, Mode, ChannelNumber):
        self.instr.write("TRAN:MODE " + str(Mode) + ",(@" + str(ChannelNumber) + ")")

    def setTransientPulseWidth(self, value, ChannelNumber):
        self.instr.write("TRAN:TWID " + str(value) + ",(@" + str(ChannelNumber) + ")")


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


class Unit(Subsystem):
    def __init__(self, VISA_ADDRESS):
        super().__init__(VISA_ADDRESS)

    def setTemp(self, units):
        self.instr.write("UNIT:TEMP " + self.strtoargs(units))

    def queryTemp(self):
        return self.instr.query("UNIT:TEMP?")


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
