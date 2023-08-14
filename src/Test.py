import pyvisa
import sys
import data
from time import sleep

sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)

from IEEEStandard import OPC, WAI, TRG


from Keysight import (
    Read,
    Apply,
    Display,
    Function,
    Output,
    Sense,
    Voltage,
    Current,
    Configure,
    Delay,
    Trigger,
    Sample,
    Initiate,
    Fetch,
    OSC,
)


class Dimport:
    def __init__():
        pass

    def getClasses(module_name):
        module = __import__(module_name)
        Read = getattr(module, "Read")
        Apply = getattr(module, "Apply")
        Display = getattr(module, "Display")
        Function = getattr(module, "Function")
        Output = getattr(module, "Output")
        Sense = getattr(module, "Sense")
        Configure = getattr(module, "Configure")
        Delay = getattr(module, "Delay")
        Trigger = getattr(module, "Trigger")
        Sample = getattr(module, "Sample")
        Initiate = getattr(module, "Initiate")
        Fetch = getattr(module, "Fetch")
        Status = getattr(module, "Status")
        Voltage = getattr(module, "Voltage")
        Current = getattr(module, "Current")

        return (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        )


from xlreport import xlreport

infoList = []
dataList = []


class VisaResourceManager:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.rm = rm

    def openRM(self, *args):
        try:
            for i in range(len(args)):
                instr = self.rm.open_resource(args[i])
                instr.baud_rate = 9600
                print(instr.query("*IDN?"))

            return 1, None
        except pyvisa.VisaIOError as e:
            print(e.args)
            return 0, e.args

    def closeRM(self):
        self.rm.close()


class VoltageMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, Instrument, param1, param2):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("VOLT")
        Sense(self.DMM).setVoltageResDC("FAST")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Voltage(self.DMM).setNPLC(10)
        Sense(self.DMM).setVoltageRangeDC(10)
        self.param1 = param1
        self.param2 = param2

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def Voltage_Sweep(self, minVoltage, maxVoltage, step_size):
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.voltage_step_size = step_size
        self.voltage_iter = ((maxVoltage - minVoltage) / step_size) + 1

    def Advanced_Settings(self, Range, Aperture, AutoZero, InputZ):
        self.Range = Range
        self.Aperture = Aperture
        self.AutoZero = AutoZero
        self.InputZ = InputZ

    def executeOLD(self):
        self.settings(0.00025, 0.0015)
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)
        i = 0
        j = 0
        k = 0
        I_fixed = self.minCurrent
        V = self.minVoltage
        I = self.maxCurrent + 1

        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.current_iter:
            Current(self.ELoad).setOutputCurrent(
                I_fixed - 0.001 * I_fixed, self.ELoad_Channel
            )
            j = 0
            V = self.minVoltage
            while j < self.voltage_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                infoList.insert(k, [V, I_fixed, i])
                temp_string = float(OPC(self.PSU).query())
                if temp_string == 1:
                    dataList.insert(k, [float(Read(self.DMM).query()), I_fixed])
                    del temp_string
                V += self.voltage_step_size
                j += 1
                k += 1
            I_fixed += self.current_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV_Accuracy(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeNEW(self):
        self.settings(0.00035, 0.0015)
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)
        i = 0
        j = 0
        k = 0
        I_fixed = self.minCurrent
        V = self.minVoltage
        I = self.maxCurrent + 1
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.current_iter:
            Current(self.ELoad).setOutputVoltage(
                I_fixed - 0.001 * I_fixed, self.ELoad_Channel
            )
            j = 0
            I = self.minVoltage
            while j < self.voltage_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                infoList.insert(k, [V, I_fixed, i])
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                V += self.voltage_step_size
                j += 1
                k += 1

            I_fixed += self.current_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeVoltageMeasurementA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        minCurrent,
        maxCurrent,
        current_stepsize,
        minVoltage,
        maxVoltage,
        voltage_stepsize,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        dataList = []
        infoList = []
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)
        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)

        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.param1 = Error_Gain
        self.param2 = Error_Offset

        i = 0
        j = 0
        k = 0
        I_fixed = float(minCurrent)
        V = float(minVoltage)
        I = float(maxCurrent) + 1
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < current_iter:
            Current(ELoad).setOutputCurrent(I_fixed - 0.001 * I_fixed, ELoad_Channel)
            j = 0
            V = float(minVoltage)
            while j < voltage_iter:
                Apply(PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                infoList.insert(k, [V, I_fixed, i])
                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                Delay(self.PSU).write(DownTime)
                V += float(voltage_stepsize)
                j += 1
                k += 1

            I_fixed += float(current_stepsize)
            i += 1

        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList

    def executeVoltageMeasurementB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        minCurrent,
        maxCurrent,
        current_stepsize,
        minVoltage,
        maxVoltage,
        voltage_stepsize,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        dataList = []
        infoList = []
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)
        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)

        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.param1 = Error_Gain
        self.param2 = Error_Offset

        i = 0
        j = 0
        k = 0
        I_fixed = float(minCurrent)
        V = float(minVoltage)
        I = float(maxCurrent) + 1
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < current_iter:
            Current(ELoad).setOutputCurrent(I_fixed - 0.001 * I_fixed, ELoad_Channel)
            j = 0
            V = float(minVoltage)
            while j < voltage_iter:
                Apply(PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                infoList.insert(k, [V, I_fixed, i])
                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                TRG(self.DMM)

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                    del temp_string

                Delay(self.PSU).write(DownTime)
                V += float(voltage_stepsize)
                j += 1
                k += 1

            I_fixed += float(current_stepsize)
            i += 1

        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList

    def test(self):
        Configure(self.DMM).write("CURR")


class CurrentMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, Instrument, param1, param2):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Sense(self.DMM).setCurrentResDC("FAST")
        Configure(self.DMM).write("Current")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Voltage", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        self.param1 = param1
        self.param2 = param2

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def Voltage_Sweep(self, minVoltage, maxVoltage, step_size):
        self.minVoltage = minVoltage
        self.maxVoltage = maxVoltage
        self.voltage_step_size = step_size
        self.voltage_iter = ((maxVoltage - minVoltage) / step_size) + 1

    def execute(self):
        self.settings(0.00035, 0.0015)
        self.Current_Sweep(0.5, 2, 0.5)
        self.Voltage_Sweep(1, 5, 1)
        i = 0
        j = 0
        k = 0
        V_fixed = self.minVoltage
        I = self.minCurrent
        V = self.maxVoltage + 1

        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.voltage_iter:
            Voltage(self.ELoad).setOutputVoltage(
                V_fixed - 0.001 * V_fixed, self.ELoad_Channel
            )
            j = 0
            I = self.minCurrent
            while j < self.current_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                I += self.current_step_size
                j += 1
                k += 1

            V_fixed += self.voltage_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeCurrentMeasurementA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        minCurrent,
        maxCurrent,
        current_stepsize,
        minVoltage,
        maxVoltage,
        voltage_stepsize,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setCurrent_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
    ):
        dataList = []
        infoList = []
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("Current")
        Trigger(self.DMM).setSource("BUS")
        Sense(DMM).setCurrentResDC(setCurrent_Res)
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)

        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()
        else:
            Sense(self.DMM).setCurrentRangeDC(Range)
        self.param1 = Error_Gain
        self.param2 = Error_Offset

        i = 0
        j = 0
        k = 0
        V_fixed = float(minVoltage)
        V = float(maxVoltage) + 1
        I = float(minCurrent)
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < voltage_iter:
            Voltage(ELoad).setOutputVoltage(V_fixed - 0.001 * V_fixed, ELoad_Channel)
            j = 0
            I = float(minCurrent)
            while j < current_iter:
                Apply(PSU).write(PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])

                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break
                I += float(current_stepsize)
                j += 1
                k += 1

            V_fixed += float(voltage_stepsize)
            i += 1
        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList

    def executeCurrentMeasurementB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        minCurrent,
        maxCurrent,
        current_stepsize,
        minVoltage,
        maxVoltage,
        voltage_stepsize,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setCurrent_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        dataList = []
        infoList = []
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        Configure(self.DMM).write("Current")
        Trigger(self.DMM).setSource("BUS")
        Sense(DMM).setCurrentResDC(setCurrent_Res)
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)

        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()
        else:
            Sense(self.DMM).setCurrentRangeDC(Range)
        self.param1 = Error_Gain
        self.param2 = Error_Offset

        i = 0
        j = 0
        k = 0
        V_fixed = float(minVoltage)
        V = float(maxVoltage) + 1
        I = float(minCurrent)
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < voltage_iter:
            Voltage(ELoad).setOutputVoltage(V_fixed - 0.001 * V_fixed, ELoad_Channel)
            j = 0
            I = float(minCurrent)
            while j < current_iter:
                Apply(PSU).write(PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])

                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                TRG(self.DMM)

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                    del temp_string

                Delay(self.PSU).write(DownTime)
                I += float(current_stepsize)
                j += 1
                k += 1

            V_fixed += float(voltage_stepsize)
            i += 1
        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList


class LoadRegulation:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, param1, param2):
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC("FAST")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        self.param1 = param1
        self.param2 = param2

    def specifications(self, V_rating, I_rating, P_rating):
        self.V_rating = V_rating
        self.I_rating = I_rating
        self.P_rating = P_rating
        self.V_max = self.P_rating / self.I_rating

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def execute(self):
        # Fixed Settings
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        V_Rating = 30
        I_Rating = 20
        P_Rating = 200

        I_Max = P_Rating / V_Rating
        Apply(self.PSU).write(self.PSU_Channel, V_Rating, I_Rating)
        Output(self.PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(self.PSU)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        V_NL = float(Fetch(self.DMM).query())

        Current(self.ELoad).setOutputCurrent(I_Max, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            V_FL = float(Fetch(self.DMM).query())
            del temp_string

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        print(V_NL, V_FL)

        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        print(30 * 0.0001 + 0.002)
        print(Voltage_Regulation)

    def executeCV_LoadRegulationA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(DMM).write("Voltage")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltage_Sense, 1)
        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        I_Max = self.P_Rating / self.V_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        TRG(DMM)
        Delay(self.PSU).write(UpTime)
        V_NL = float(Fetch(DMM).query())
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(I_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Initiate(DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        Delay(self.PSU).write(UpTime)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            V_FL = float(Fetch(self.DMM).query())
            del temp_string

        Delay(self.PSU).write(DownTime)
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Voltage Regulation (CV): (%)", Desired_Voltage_Regulation)
        print("Calculated Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4))

    def executeCV_LoadRegulationB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(DMM).write("Voltage")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltage_Sense, 1)
        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        I_Max = self.P_Rating / self.V_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                V_NL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                V_NL = float(Fetch(self.DMM).query())
                break
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(I_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)

        WAI(self.ELoad)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        Delay(self.PSU).write(UpTime)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                V_FL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                V_FL = float(Fetch(self.DMM).query())
                break

        Delay(self.PSU).write(DownTime)
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation (CV): (%)", Desired_Voltage_Regulation)
        print(
            "Calculated Load Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4)
        )

    def executeCC_LoadRegulationA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(DMM).write("Current")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)
        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()

        else:
            Sense(self.DMM).setCurrentRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        V_Max = self.P_Rating / self.I_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        TRG(DMM)
        Delay(self.PSU).write(UpTime)
        I_NL = float(Fetch(DMM).query())
        Delay(self.PSU).write(DownTime)
        Voltage(ELoad).setOutputVoltage(V_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Initiate(DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        Delay(self.PSU).write(UpTime)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            I_FL = float(Fetch(self.DMM).query())
            del temp_string

        Delay(self.PSU).write(DownTime)
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation(CC): (%)", Desired_Voltage_Regulation)
        print("Calculated Load Regulation(CC): (%)", round(Voltage_Regulation, 4))

    def executeCC_LoadRegulationB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(DMM).write("Current")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)
        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()

        else:
            Sense(self.DMM).setCurrentRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        V_Max = self.P_Rating / self.I_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                I_NL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                I_NL = float(Fetch(self.DMM).query())
                break
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(V_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)

        WAI(self.ELoad)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        Delay(self.PSU).write(UpTime)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                I_FL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                I_FL = float(Fetch(self.DMM).query())
                break

        Delay(self.PSU).write(DownTime)
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation (CC): (%)", Desired_Voltage_Regulation)
        print("Calculated Load Regulation (CC): (%)", round(Voltage_Regulation, 4))


class RiseFallTime:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.OSC = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def test(self):
        OSC(self.OSC).setup()
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Apply(self.PSU).write(self.PSU_Channel, 30, 20)
        Output(self.PSU).setOutputState("ON")
        Current(self.ELoad).setOutputCurrent(6.66, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        OSC(self.OSC).standby()
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        OSC(self.OSC).readRiseTime()
        OSC(self.OSC).standby()
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        OSC(self.OSC).readFallTime()
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
