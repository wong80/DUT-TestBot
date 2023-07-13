import DMM
import PSU
import ELoad
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


def VoltageMeasurement():
    Sense(ADDR3).setVoltageResDC("FAST")
    Display(ADDR1).displayState("Channel 3")
    Function(ADDR1).setMode("Current", 3)
    Voltage(ADDR2).setSenseMode("EXT", 1)
    A.currentSetup(1, 2, 3, 0.5)
    B.Voltage_Sweep(1, 30, 4, "CH1", 0.5)
    i = 0
    j = 0
    k = 0
    I1 = A.minCurrent
    V = B.minVoltage
    I = B.Current

    Output(ADDR1).setOutputStateC("ON", 3)
    Output(ADDR2).setOutputState("ON")

    while i < A.iterations:
        Current(ADDR1).setOutputCurrent(I1 - 0.001 * I1, 3)
        j = 0
        V = B.minVoltage
        while j < B.iterations:
            Apply(ADDR2).write(1, V, I)
            print("Voltage:", V, " Current:", I1)
            infoList.insert(k, [V, I1, i])

            temp_string = float(OPC(ADDR2).query())
            if temp_string == 1:
                dataList.insert(k, [float(Read(ADDR3).query()), I1])
                del temp_string

            V += B.step_size
            j += 1
            k += 1

        I1 += A.step_size
        i += 1

    Output(ADDR2).setOutputState("OFF")
    Output(ADDR1).setOutputStateC("OFF", 3)


def CurrentMeasurement():
    A.display("Channel 3")
    A.function("Voltage", 3)
    A.voltageSetup(0.5, 3, 3, 0.5)
    B.Current_Sweep(0.5, 1, 5, "CH1", 0.05)
    i = 0
    j = 0
    V1 = A.minVoltage
    V = B.Voltage
    I = B.minCurrent

    A.Output("ON", 3)
    B.Output("ON")

    while i < A.iterations:
        A.setVoltage(V1, 3)
        j = 0
        I = B.minCurrent
        while j < B.iterations:
            B.apply(V, I)
            print("Voltage:", V1, " Current:", I)
            infoList.insert(j, [V1, I])

            temp_string = float(B.dmm.query("*OPC?"))
            if temp_string == 1:
                dataList.insert(j, [V, float(C.dmm.query("READ?"))])
                del temp_string

            I += B.step_size
            j += 1

        V1 += A.step_size
        i += 1

    B.Output("OFF")
    A.Output("OFF", 3)


ADDR1 = "GPIB0::5::INSTR"
ADDR2 = "USB0::0x2A8D::0x5C02::MY62100050::0::INSTR"
ADDR3 = "USB0::0x2A8D::0x8E01::CN60440004::0::INSTR"
A = ELoad.N6701C(ADDR1)
B = PSU.E36731A(ADDR2)
C = DMM.EDU34450A(ADDR3)

VoltageMeasurement()

F = Data.instrumentData(ADDR1, ADDR2, ADDR3)


A.rm.close()
B.rm.close()
C.rm.close()
D = Data.datatoCSV(infoList, dataList)
E = Data.datatoGraph(infoList, dataList)
E.scatterCompare()
