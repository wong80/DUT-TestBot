import DMM
import PSU
import Data
from threading import Thread


def Test1():
    A = DMM.EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")


def Test2():
    B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")


def Test3():
    C = Data.datatoCSV()


thread1 = Thread(target=Test1)
thread2 = Thread(target=Test2)
thread3 = Thread(target=Test3)

thread1.start()
thread2.start()
thread1.join()
thread2.join()
thread3.start()
