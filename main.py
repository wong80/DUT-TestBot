import DMM
import PSU
import Data

A = DMM.EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")
B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")

A.config("Primary", "Voltage")
B.testSetup(1, 30, 3, "CH1", 0.25)
k = 0
V = B.minVoltage
I = B.Current
infoList = []
dataList = []

B.Output("ON")
while k < B.iterations:
    B.apply(V, I)
    print("Voltage:", V, " Current:", I)
    infoList.insert(k, V)

    temp_string = float(B.dmm.query("*OPC?"))
    if temp_string == 1:
        dataList.append(float(A.dmm.query("READ?")))
        del temp_string

    V += B.step_size
    k += 1

B.Output("OFF")
A.rm.close()
B.rm.close()
D = Data.datatoCSV(infoList, dataList)
E = Data.datatoGraph()
E.plotScatter()
