import Data
import Test

infoList = []
dataList = []


ADDR1 = "GPIB0::5::INSTR"
ADDR2 = "USB0::0x2A8D::0x5C02::MY62100050::0::INSTR"
# ADDR3 = "USB0::0x0957::0x0618::TW46260038::0::INSTR"
ADDR3 = "USB0::0x2A8D::0x8E01::CN60440004::0::INSTR"


A = Test
A.VisaResourceManager(ADDR1, ADDR2, ADDR3)
B = Test.VoltageMeasurement(ADDR1, ADDR2, ADDR3, 3, 1)
infoList, dataList = B.execute()


F = Data.instrumentData(ADDR1, ADDR2, ADDR3)

D = Data.datatoCSV(infoList, dataList)
E = Data.datatoGraph(infoList, dataList)
E.scatterCompare("Current")
