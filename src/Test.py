import pyvisa
import sys
import Data


sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)

from IEEEStandard import OPC, WAI, TRG
from Subsystems import (
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
    Data,
)
from xlreport import xlreport

infoList = []
dataList = []


class VisaResourceManager:
    def __init__(self):
        rm = pyvisa.ResourceManager()
        self.rm = rm

    def openRM(self, *args):
        for i in range(len(args)):
            instr = self.rm.open_resource(args[i])
            instr.baud_rate = 9600
            print(instr.query("*IDN?"))

    def closeRM(self):
        self.rm.close()


class VoltageMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, param1, param2):
        Sense(self.DMM).setVoltageResDC("FAST")
        Sense(self.DMM).setVoltageRangeDC(0.1)
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
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
        self.settings(0.00025, 0.0015)
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 9, 0.5)
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

                WAI(self.PSU)

                V += self.voltage_step_size
                j += 1
                k += 1

            I_fixed += self.current_step_size
            i += 1

        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)

        F = Data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = Data.datatoCSV_Accuracy(infoList, dataList)
        E = Data.datatoGraph(infoList, dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeVoltageMeasurement(
        self,
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
        setVoltage_Range,
    ):
        dataList = []
        infoList = []
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)

        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)

        if setVoltage_Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()
        else:
            Sense(self.DMM).setVoltageRangeDC(setVoltage_Range)

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

                temp_string = float(OPC(PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [float(Read(DMM).query()), I_fixed])
                    del temp_string

                WAI(PSU)
                V += float(voltage_stepsize)
                j += 1
                k += 1

            I_fixed += float(current_stepsize)
            i += 1

        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList


class CurrentMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, param1, param2):
        Sense(self.DMM).setCurrentResDC("FAST")
        # Configure(self.DMM).write("Current")
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

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [V_fixed, float(Read(self.DMM).query())])
                    del temp_string

                WAI(self.PSU)
                I += self.current_step_size
                j += 1
                k += 1

            V_fixed += self.voltage_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = Data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = Data.datatoCSV(infoList, dataList)
        E = Data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeCurrentMeasurement(
        self,
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
        setCurrent_Range,
    ):
        dataList = []
        infoList = []
        Sense(DMM).setVoltageResDC(setVoltage_Res)
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltage_Sense, PSU_Channel)

        if setCurrent_Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()
        else:
            Sense(self.DMM).setCurrentRangeDC(setCurrent_Range)
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

                temp_string = float(OPC(PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [V_fixed, float(Read(DMM).query())])
                    del temp_string

                WAI(PSU)
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
        self.settings(0.0001, 0.002)
        self.specifications(30, 20, 200)
        self.Current_Sweep(0.25, 6, 0.25)
        iter = 0
        k = 0
        I_max = self.maxCurrent + 0.1
        V = self.V_rating
        I_min = self.minCurrent
        Output(self.PSU).setOutputState("ON")
        Apply(self.PSU).write(self.PSU_Channel, V, I_max)

        V_NL = float(Read(self.DMM).query())

        while iter < self.current_iter:
            Current(self.ELoad).setOutputCurrent(I_min, self.ELoad_Channel)
            Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
            temp_string = float(OPC(self.ELoad).query())
            print("Current : ", I_min, "Load :", I_min * V)
            infoList.insert(k, [I_min, I_min * V])

            if temp_string == 1:
                dataList.insert(k, [float(Read(self.DMM).query()), I_min * V])
                del temp_string

            I_min += self.current_step_size
            k += 1
            iter += 1

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        D = Data.datatoCSV_Regulation(
            infoList, dataList, self.V_rating, self.param1, self.param2, V_NL
        )


class DataBuffer:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def run(self):
        Trigger(self.DMM).setSource("BUS")
        Trigger(self.DMM).setTriggerDelay(4)
        Trigger(self.DMM).setCount(4)
        Sample(self.DMM).setSampleCount(30)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        print(Fetch(self.DMM).query())
        # Delay(self.DMM, 1000)
        # print(Read(self.DMM).query())
        print(Data(self.DMM).data())
