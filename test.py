# import pyvisa
# import DMM
# import PSU

# A = DMM.EDU34450A("USB0::0x2A8D::0x8E01::CN60440004::0::INSTR")
# B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")

import pyvisa

rm = pyvisa.ResourceManager("/path/to/my/libvisa.so.7")
lib = rm.visalib
