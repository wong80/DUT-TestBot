import DMM
import PSU
import Data

infoList = []
dataList = []


def VoltageMeasurement():
    C.config("Current", "DC")
    C.Sense("Voltage", "RES FAST")
    B.Voltage_Sweep(1, 10, 3, "CH1", 1)
    k = 0
    V = B.minVoltage
    I = B.Current

    B.Output("ON")
    while k < B.iterations:
        B.apply(V, I)
        print("Voltage:", V, " Current:", I)
        infoList.insert(k, [V, I])

        temp_string = float(B.dmm.query("*OPC?"))
        if temp_string == 1:
            dataList.append(float(C.dmm.query("READ?")))
            del temp_string

        I += B.step_size
        k += 1


def CurrentMeasurement():
    B.Current_Sweep(0.5, 2, 5, "CH1", 0.05)
    k = 0
    V = B.Voltage
    I = B.minCurrent

    B.Output("ON")
    while k < B.iterations:
        B.apply(V, I)
        print("Voltage:", V, " Current:", I)
        infoList.insert(k, [V, I])

        temp_string = float(B.dmm.query("*OPC?"))
        if temp_string == 1:
            dataList.insert(k, [V, float(C.dmm.query("READ?"))])
            del temp_string

        I += B.step_size
        k += 1

    B.Output("OFF")


A = DMM.EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")
B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
C = DMM.A34405A("USB0::0x0957::0x0618::TW46260038::0::INSTR")

CurrentMeasurement()
A.rm.close()
B.rm.close()
C.rm.close()
D = Data.datatoCSV(infoList, dataList)
E = Data.datatoGraph(infoList, dataList)

E.plotScatter(0.00035, 0.0015, "Current")
