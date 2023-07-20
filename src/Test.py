import pyvisa
import sys
import Data


sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)

from IEEEStandard import OPC
from Subsystems import Read, Apply, Display, Function, Output, Sense, Voltage, Current

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
            instr.write("*RST")
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
        self.Current_Sweep(1, 2, 0.5)
        self.Voltage_Sweep(1, 30, 0.5)
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

        F = Data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = Data.datatoCSV(infoList, dataList)
        E = Data.datatoGraph(infoList, dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

    def executeA(
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
    ):
        dataList = []
        infoList = []
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)
        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)
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

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [float(Read(DMM).query()), I_fixed])
                    del temp_string

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
