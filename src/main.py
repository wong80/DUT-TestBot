import src.DMM as DMM
import src.PSU as PSU
import src.ELoad as Eload
import src.Data as Data

infoList = []
dataList = []


def VoltageMeasurement():
    C.Sense("Voltage", "RES FAST")
    A.display("Channel 3")
    A.function("Current", 3)
    A.currentSetup(1, 2, 3, 1)
    B.Voltage_Sweep(0.5, 5, 4, "CH1", 1)
    i = 0
    j = 0
    k = 0
    I1 = A.minCurrent
    V = B.minVoltage
    I = B.Current

    A.Output("ON", 3)
    B.Output("ON")

    while i < A.iterations:
        A.setCurrent(I1 - 0.001 * I1, 3)
        j = 0
        V = B.minVoltage
        while j < B.iterations:
            B.apply(V, I)
            print("Voltage:", V, " Current:", I1)
            infoList.insert(k, [V, I1, i])

            temp_string = float(B.dmm.query("*OPC?"))
            if temp_string == 1:
                dataList.insert(k, [float(C.dmm.query("READ?")), I1])
                del temp_string

            V += B.step_size
            j += 1
            k += 1

        I1 += A.step_size
        i += 1

    B.Output("OFF")
    A.Output("OFF", 3)


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


A = Eload.N6701C("USB0::0x2A8D::0x0102::MY56000223::0::INSTR")
B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
C = DMM.EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")

VoltageMeasurement()

F = Data.instrumentData(A, B, C)


A.rm.close()
B.rm.close()
C.rm.close()
D = Data.datatoCSV(infoList, dataList)
E = Data.datatoGraph(infoList, dataList)
E.scatterCompare()
