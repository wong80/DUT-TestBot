import pyvisa
import time
import matplotlib.pyplot as plt

dataList = []


class EDU34450A(object):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        self.rm = rm
        # Visa Address is found under Keysight Connection Expert
        self.dmm = self.rm.open_resource(self.VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        self.dmm.write("*rst")


class N6701C(EDU34450A):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()

        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600
        # '*IDN?' is standard GPIB Message for "what are you?"
        # print(self.dmm.query("*IDN?"))

        # Resets the instrument configuration and synchronizes it before each R/W
        self.dmm.write("*rst")
        self.dmm.query("*opc?")


class A34405A(EDU34450A):
    def __init__(self, VISA_ADDRESS):
        self.VISA_ADDRESS = VISA_ADDRESS
        # ResourceManager Setup
        rm = pyvisa.ResourceManager()
        self.rm = rm
        # Visa Address is found under Keysight Connection Expert
        self.dmm = rm.open_resource(VISA_ADDRESS)
        self.dmm.baud_rate = 9600
