import DMM
import PSU


if __name__ == "__main__":
    A = DMM.N6701C("USB0::0x2A8D::0x0102::MY56000223::0::INSTR")
    B = PSU.E36731A("USB0::0x2A8D::0x5C02::MY62100050::0::INSTR")
