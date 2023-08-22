""" Module containing all of the test options available in this program. 

    The tests are categorized into different classes.

"""
infoList = []
dataList = []
from xlreport import xlreport
import pyvisa
import sys
import data
from time import sleep

sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)

from IEEEStandard import OPC, WAI, TRG, RST

from Keysight import (
    Read,
    Apply,
    Display,
    Function,
    Output,
    Sense,
    Voltage,
    Current,
    Configure,
    Trigger,
    Initiate,
    Fetch,
    Oscilloscope,
)


class Dimport:
    """Class to control which library will be dynamically imported"""

    def __init__():
        pass

    def getClasses(module_name):
        """Declare the module based on the module name given

        Args:
            module_name: Determines which library will the program import from

        Returns:
            Returns a set of Modules imported from a library
        """

        module = __import__(module_name)
        Read = getattr(module, "Read")
        Apply = getattr(module, "Apply")
        Display = getattr(module, "Display")
        Function = getattr(module, "Function")
        Output = getattr(module, "Output")
        Sense = getattr(module, "Sense")
        Configure = getattr(module, "Configure")
        Delay = getattr(module, "Delay")
        Trigger = getattr(module, "Trigger")
        Sample = getattr(module, "Sample")
        Initiate = getattr(module, "Initiate")
        Fetch = getattr(module, "Fetch")
        Status = getattr(module, "Status")
        Voltage = getattr(module, "Voltage")
        Current = getattr(module, "Current")

        return (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        )


class VisaResourceManager:
    """Manage the VISA Resources

    Attributes:
        args: args should contain one or multiple string containing the Visa Address of an Instrument

    """

    def __init__(self):
        """Initiate the object rm as Resource Manager"""
        rm = pyvisa.ResourceManager()
        self.rm = rm

    def openRM(self, *args):
        """Open the VISA Resources to be used

        The program also initiates and standardize certain specifications such as the baud rate.

            Args:
                *args: to declare single or multiple VISA Resources

            Returns:
                Return a Boolean to the program whether there were any errors encountered.

            Raises:
                VisaIOError: An error occured when opening PyVisa Resources

        """
        try:
            for i in range(len(args)):
                instr = self.rm.open_resource(args[i])
                instr.baud_rate = 9600
                # print(instr.query("*IDN?"))

            return 1, None
        except pyvisa.VisaIOError as e:
            print(e.args)
            return 0, e.args

    def closeRM(self):
        """Closes the Visa Resources when not in used"""
        self.rm.close()


class VoltageMeasurement:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, Instrument, param1, param2):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Configure(self.DMM).write("VOLT")
        Sense(self.DMM).setVoltageResDC("FAST")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Voltage(self.DMM).setNPLC(10)
        Sense(self.DMM).setVoltageRangeDC(10)
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

    def Advanced_Settings(self, Range, Aperture, AutoZero, InputZ):
        self.Range = Range
        self.Aperture = Aperture
        self.AutoZero = AutoZero
        self.InputZ = InputZ

    def executeOLD(self):
        self.settings(0.00025, 0.0015)
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)
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
        data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV_Accuracy(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Voltage", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeNEW(self):
        self.settings(0.00035, 0.0015)
        self.Current_Sweep(1, 2, 1)
        self.Voltage_Sweep(1, 10, 1)
        i = 0
        j = 0
        k = 0
        I_fixed = self.minCurrent
        V = self.minVoltage
        I = self.maxCurrent + 1
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Output(self.PSU).setOutputState("ON")

        while i < self.current_iter:
            Current(self.ELoad).setOutputVoltage(
                I_fixed - 0.001 * I_fixed, self.ELoad_Channel
            )
            j = 0
            I = self.minVoltage
            while j < self.voltage_iter:
                Apply(self.PSU).write(self.PSU_Channel, V, I)
                print("Voltage: ", V, "Current: ", I_fixed)
                infoList.insert(k, [V, I_fixed, i])
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                V += self.voltage_step_size
                j += 1
                k += 1

            I_fixed += self.current_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeVoltageMeasurementA(
        self,
        Instrument,
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
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        """Execution of Voltage Measurement for Programm / Readback Accuracy using Status Event Registry to synchronize Instruments

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all instruments
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of instruments here is done by reading the status of the event registry.
        The status determined from the instrument can let the program determine if the instrument is
        measuring. The program will only proceed to tell the instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.


        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setVoltage_Sense: String determining the Voltage Sense that will be used.
            setVoltage_Res: String determining the Voltage Resoltion that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []

        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instrument Initialization
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)
        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)
        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.param1 = Error_Gain
        self.param2 = Error_Offset

        # Test Loop Begins
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
                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                        break

                Delay(self.PSU).write(DownTime)
                V += float(voltage_stepsize)
                j += 1
                k += 1

            I_fixed += float(current_stepsize)
            i += 1

        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList

    def executeVoltageMeasurementB(
        self,
        Instrument,
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
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        """Execution of Voltage Measurement for Programm / Readback Accuracy using WAI and OPC to synchronize Instruments

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all instruments
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the instruments, since it is under the IEEE Standard Library, most instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.


        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setVoltage_Sense: String determining the Voltage Sense that will be used.
            setVoltage_Res: String determining the Voltage Resoltion that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []

        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instrument Initialization
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC(setVoltage_Res)
        Display(self.ELoad).displayState(ELoad_Channel)
        Function(self.ELoad).setMode(setMode, ELoad_Channel)
        Voltage(self.PSU).setSenseMode(setVoltage_Sense, PSU_Channel)

        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.param1 = Error_Gain
        self.param2 = Error_Offset

        # Test Loop
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
                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                TRG(self.DMM)

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [float(Fetch(self.DMM).query()), I_fixed])
                    del temp_string

                Delay(self.PSU).write(DownTime)
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

    def settings(self, Instrument, param1, param2):
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        Sense(self.DMM).setCurrentResDC("FAST")
        Configure(self.DMM).write("Current")
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
                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                I += self.current_step_size
                j += 1
                k += 1

            V_fixed += self.voltage_step_size
            i += 1
        Output(self.PSU).setOutputState("OFF")
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        F = data.instrumentData(self.PSU, self.DMM, self.ELoad)
        D = data.datatoCSV(infoList, dataList)
        E = data.datatoGraph(infoList, dataList)
        E.scatterCompare("Current", self.param1, self.param2)

        G = xlreport()
        G.run()

    def executeCurrentMeasurementA(
        self,
        Instrument,
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
        setCurrent_Sense,
        setCurrent_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
    ):
        """Execution of Current Measurement for Programm / Readback Accuracy using Status Event Registry to synchronize Instruments

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all instruments
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of instruments here is done by reading the status of the event registry.
        The status determined from the instrument can let the program determine if the instrument is
        measuring. The program will only proceed to tell the instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.


        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setCurrent_Sense: String determining the Current Sense that will be used.
            setCurrent_Res: String determining the Current Resolution that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []
        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instruments Initialization
        Configure(self.DMM).write("Current")
        Trigger(self.DMM).setSource("BUS")
        Sense(DMM).setCurrentResDC(setCurrent_Res)
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)

        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()
        else:
            Sense(self.DMM).setCurrentRangeDC(Range)
        self.param1 = Error_Gain
        self.param2 = Error_Offset

        # Test Loop
        i = 0
        j = 0
        k = 0
        V_fixed = float(minVoltage)
        V = float(maxVoltage) + 1
        I = float(minCurrent)
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < voltage_iter:
            Voltage(ELoad).setOutputVoltage(V_fixed - 0.001 * V_fixed, ELoad_Channel)
            j = 0
            I = float(minCurrent)
            while j < current_iter:
                Apply(PSU).write(PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])

                WAI(self.PSU)
                Initiate(self.DMM).initiate()
                status = float(Status(self.DMM).operationCondition())
                TRG(self.DMM)

                while 1:
                    status = float(Status(self.DMM).operationCondition())

                    if status == 8704.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break

                    elif status == 512.0:
                        dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                        break
                I += float(current_stepsize)
                j += 1
                k += 1

            V_fixed += float(voltage_stepsize)
            i += 1
        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList

    def executeCurrentMeasurementB(
        self,
        Instrument,
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
        setCurrent_Sense,
        setCurrent_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        """Execution of Current Measurement for Programm / Readback Accuracy using WAI and OPC to synchronize Instruments

        The function first declares two lists, datalist & infolist that will be used to collect data.
        It then dynamically imports the library to be used. Next, the settings for all instruments
        are initialized. The test loop begins where Voltage and Current Sweep is conducted and collect
        measured data.

        The synchronization of instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the instruments, since it is under the IEEE Standard Library, most instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.


        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Readback Voltage Specification.
            Error_Offset: Float determining the error offset of the Readback Voltage Specification.
            minCurrent: Float determining the start current for Current Sweep.
            maxCurrent: Float determining the stop current for Current Sweep.
            current_stepsize: Float determining the step size during Current Sweep.
            minVoltage: Float determining the start voltage for Voltage Sweep.
            maxVoltage: Float determining the stop voltage for Voltage Sweep.
            voltage_stepsize: Float determining the step_size for Voltage_Sweep.
            PSU: String containing the VISA Address of the PSU used.
            DMM: String containing the VISA Address of the DMM used.
            ELoad: String containing the VISA Address of the ELoad used.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            setCurrent_Sense: String determining the Current Sense that will be used.
            setCurrent_Res: String determining the Current Resolution that will be used.
            setMode: String determining the Priority mode of the ELoad.
            Range: String determining the measuring range of the DMM should be Auto or a specific range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """
        dataList = []
        infoList = []

        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        Configure(self.DMM).write("Current")
        Trigger(self.DMM).setSource("BUS")
        Sense(DMM).setCurrentResDC(setCurrent_Res)
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)

        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()
        else:
            Sense(self.DMM).setCurrentRangeDC(Range)
        self.param1 = Error_Gain
        self.param2 = Error_Offset

        # Test Loop
        i = 0
        j = 0
        k = 0
        V_fixed = float(minVoltage)
        V = float(maxVoltage) + 1
        I = float(minCurrent)
        current_iter = (
            (float(maxCurrent) - float(minCurrent)) / float(current_stepsize)
        ) + 1
        voltage_iter = (
            (float(maxVoltage) - float(minVoltage)) / float(voltage_stepsize)
        ) + 1
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Output(PSU).setOutputState("ON")

        while i < voltage_iter:
            Voltage(ELoad).setOutputVoltage(V_fixed - 0.001 * V_fixed, ELoad_Channel)
            j = 0
            I = float(minCurrent)
            while j < current_iter:
                Apply(PSU).write(PSU_Channel, V, I)
                print("Voltage: ", V_fixed, "Current: ", I)
                infoList.insert(k, [V_fixed, I, i])

                WAI(self.PSU)
                Delay(self.PSU).write(UpTime)
                Initiate(self.DMM).initiate()
                TRG(self.DMM)

                temp_string = float(OPC(self.PSU).query())

                if temp_string == 1:
                    dataList.insert(k, [V_fixed, float(Fetch(self.DMM).query())])
                    del temp_string

                Delay(self.PSU).write(DownTime)
                I += float(current_stepsize)
                j += 1
                k += 1

            V_fixed += float(voltage_stepsize)
            i += 1
        Output(PSU).setOutputState("OFF")
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        return dataList, infoList


class LoadRegulation:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.DMM = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def settings(self, param1, param2):
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Sense(self.DMM).setVoltageResDC("FAST")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        self.param1 = param1
        self.param2 = param2

    def specifications(self, V_rating, I_rating, P_rating):
        self.V_rating = V_rating
        self.I_rating = I_rating
        self.P_rating = P_rating
        self.V_max = self.P_rating / self.I_rating

    def Current_Sweep(self, minCurrent, maxCurrent, step_size):
        self.minCurrent = minCurrent
        self.maxCurrent = maxCurrent
        self.current_step_size = step_size
        self.current_iter = ((maxCurrent - minCurrent) / step_size) + 1

    def execute(self):
        # Fixed Settings
        Configure(self.DMM).write("Voltage")
        Trigger(self.DMM).setSource("BUS")
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        V_Rating = 30
        I_Rating = 20
        P_Rating = 200

        I_Max = P_Rating / V_Rating
        Apply(self.PSU).write(self.PSU_Channel, V_Rating, I_Rating)
        Output(self.PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(self.PSU)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        V_NL = float(Fetch(self.DMM).query())

        Current(self.ELoad).setOutputCurrent(I_Max, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)
        Initiate(self.DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            V_FL = float(Fetch(self.DMM).query())
            del temp_string

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        print(V_NL, V_FL)

        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        print(30 * 0.0001 + 0.002)
        print(Voltage_Regulation)

    def executeCV_LoadRegulationA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        """Test for determining the Load Regulation of DUT under Constant Voltage (CV) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CV condition.

        The synchronization of instruments here is done by reading the status of the event registry.
        The status determined from the instrument can let the program determine if the instrument is
        measuring. The program will only proceed to tell the instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setVoltage_Res: String determining the Voltage Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.


        """
        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instrument Initializations
        Configure(DMM).write("Voltage")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltage_Sense, 1)
        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        I_Max = self.P_Rating / self.V_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        TRG(DMM)
        Delay(self.PSU).write(UpTime)
        V_NL = float(Fetch(DMM).query())
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(I_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Initiate(DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        Delay(self.PSU).write(UpTime)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            V_FL = float(Fetch(self.DMM).query())
            del temp_string

        Delay(self.PSU).write(DownTime)
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Voltage Regulation (CV): (%)", Desired_Voltage_Regulation)
        print("Calculated Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4))

    def executeCV_LoadRegulationB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setVoltage_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        InputZ,
        UpTime,
        DownTime,
    ):
        """Test for determining the Load Regulation of DUT under Constant Voltage (CV) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CV condition.

        The synchronization of instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the instruments, since it is under the IEEE Standard Library, most instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setVoltage_Res: String determining the Voltage Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.


        """
        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instruments Initialization
        Configure(DMM).write("Voltage")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltage_Sense, 1)
        Voltage(self.DMM).setNPLC(Aperture)
        Voltage(self.DMM).setAutoZeroMode(AutoZero)
        Voltage(self.DMM).setAutoImpedanceMode(InputZ)

        if Range == "Auto":
            Sense(self.DMM).setVoltageRangeDCAuto()

        else:
            Sense(self.DMM).setVoltageRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        I_Max = self.P_Rating / self.V_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                V_NL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                V_NL = float(Fetch(self.DMM).query())
                break
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(I_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)

        WAI(self.ELoad)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        Delay(self.PSU).write(UpTime)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                V_FL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                V_FL = float(Fetch(self.DMM).query())
                break

        Delay(self.PSU).write(DownTime)
        print("V_NL: ", V_NL, "V_FL: ", V_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((V_NL - V_FL) / V_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation (CV): (%)", Desired_Voltage_Regulation)
        print(
            "Calculated Load Voltage Regulation (CV): (%)", round(Voltage_Regulation, 4)
        )

    def executeCC_LoadRegulationA(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        """Test for determining the Load Regulation of DUT under Constant Current (CC) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CC condition.

        The synchronization of instruments here is done by reading the status of the event registry.
        The status determined from the instrument can let the program determine if the instrument is
        measuring. The program will only proceed to tell the instrument to query the measured value
        after it is determined that the measurement has been completed. This method is suitable for
        operations that require a longer time (e.g. 100 NPLC). However the implementation is slighty
        more complicated than other methods. This method only can be implemented that have the specific
        commands that are used.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setCurrent_Res: String determining the Current Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.

        """
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)
        # Fixed Settings
        Configure(DMM).write("Current")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)
        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()

        else:
            Sense(self.DMM).setCurrentRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        V_Max = self.P_Rating / self.I_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        TRG(DMM)
        Delay(self.PSU).write(UpTime)
        I_NL = float(Fetch(DMM).query())
        Delay(self.PSU).write(DownTime)
        Voltage(ELoad).setOutputVoltage(V_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)
        Initiate(DMM).initiate()
        TRG(self.DMM)
        WAI(self.ELoad)
        Delay(self.PSU).write(UpTime)
        temp_string = float(OPC(self.ELoad).query())
        if temp_string == 1:
            I_FL = float(Fetch(self.DMM).query())
            del temp_string

        Delay(self.PSU).write(DownTime)
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation(CC): (%)", Desired_Voltage_Regulation)
        print("Calculated Load Regulation(CC): (%)", round(Voltage_Regulation, 4))

    def executeCC_LoadRegulationB(
        self,
        Instrument,
        Error_Gain,
        Error_Offset,
        V_Rating,
        I_Rating,
        P_Rating,
        PSU,
        DMM,
        ELoad,
        ELoad_Channel,
        PSU_Channel,
        setCurrent_Sense,
        setVoltage_Res,
        setMode,
        Range,
        Aperture,
        AutoZero,
        Terminal,
        UpTime,
        DownTime,
    ):
        """Test for determining the Load Regulation of DUT under Constant Current (CC) Mode.

        The function first dynamically imports the library to be used. Next, settings for the
        instruments will be initialized. The test begins by measuring the No Load Voltage when
        the PSU is turned on at max nominal settings but ELoad is turned off. Then, the ELoad is
        turned on to drive the DUT to full load, while measuring the V_FullLoad, Calculations
        are then done to check the load regulation under CC condition.

        The synchronization of instruments here is done by using IEEE Commands OPC and WAI. The command OPC
        queries the instrument the status of the commands. 1 will be returned if all commands given have
        been executed. Hence, this makes as a simple and efficient way to synchronize the measurement timing
        of the instruments, since it is under the IEEE Standard Library, most instruments are synchronized
        using this way. However, this method only works for commands with a short execution time.

        Args:
            Instrument: String determining which library to be used.
            Error_Gain: Float determining the error gain of the Load Regulation Specifications.
            Error_Offset: Float determining the error offset of the Load Regulation Specifications.
            V_Rating: Float containing the Rated Voltage of the DUT.
            I_Rating: Float containing the Rated Current of the DUT.
            P_Rating: Float containing the Rated Power of the DUT.
            PSU: String containing the VISA Address of PSU used.
            DMM: String containing the VISA Address of DMM used.
            ELoad: String containing the VISA Address of ELoad used.
            PSU_Channel: Integer containing the channel number that the PSU is using.
            ELoad_Channel: Integer containing the channel number that the ELoad is using.
            setVoltage_Sense: String determining the Voltage Sense that is used.
            setCurrent_Res: String determining the Current Resolution that is used.
            setMode: String determining the Priority Mode of the ELoad.
            Range: String determining the measuring range of DMM should be Auto or specified range.
            Apreture: String determining the NPLC to be used by DMM when measuring.
            AutoZero: String determining if AutoZero Mode on DMM should be enabled/disabled.
            InputZ: String determining the Input Impedance Mode of DMM.
            UpTime: Float containing details regarding the uptime delay.
            DownTime: Float containing details regarding the downtime delay.

        Returns:
            Returns two list, DataList & InfoList. Each containing the programmed & measured data individually.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.

        """
        # Dynamic Library Import
        (
            Read,
            Apply,
            Display,
            Function,
            Output,
            Sense,
            Configure,
            Delay,
            Trigger,
            Sample,
            Initiate,
            Fetch,
            Status,
            Voltage,
            Current,
        ) = Dimport.getClasses(Instrument)

        # Instrument Initialization
        Configure(DMM).write("Current")
        Trigger(DMM).setSource("BUS")
        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setCurrent_Sense, PSU_Channel)
        Current(self.DMM).setNPLC(Aperture)
        Current(self.DMM).setAutoZeroMode(AutoZero)
        Current(self.DMM).setTerminal(Terminal)

        if Range == "Auto":
            Sense(self.DMM).setCurrentRangeDCAuto()

        else:
            Sense(self.DMM).setCurrentRangeDC(Range)

        self.V_Rating = float(V_Rating)
        self.I_Rating = float(I_Rating)
        self.P_Rating = float(P_Rating)
        self.param1 = float(Error_Gain)
        self.param2 = float(Error_Offset)

        V_Max = self.P_Rating / self.I_Rating
        Apply(PSU).write(self.PSU_Channel, self.V_Rating, self.I_Rating)
        Output(PSU).setOutputState("ON")

        # Reading for No Load Voltage

        WAI(PSU)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                I_NL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                I_NL = float(Fetch(self.DMM).query())
                break
        Delay(self.PSU).write(DownTime)
        Current(ELoad).setOutputCurrent(V_Max, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)

        WAI(self.ELoad)
        Initiate(DMM).initiate()
        status = float(Status(self.DMM).operationCondition())
        TRG(self.DMM)
        Delay(self.PSU).write(UpTime)
        while 1:
            status = float(Status(self.DMM).operationCondition())

            if status == 8704.0:
                I_FL = float(Fetch(self.DMM).query())
                break

            elif status == 512.0:
                I_FL = float(Fetch(self.DMM).query())
                break

        Delay(self.PSU).write(DownTime)
        print("I_NL: ", I_NL, "I_FL: ", I_FL)
        Output(self.ELoad).setOutputStateC("OFF", ELoad_Channel)
        Output(self.PSU).setOutputState("OFF")
        Voltage_Regulation = ((I_NL - I_FL) / I_FL) * 100
        Desired_Voltage_Regulation = 30 * self.param1 + self.param2
        print("Desired Load Regulation (CC): (%)", Desired_Voltage_Regulation)
        print("Calculated Load Regulation (CC): (%)", round(Voltage_Regulation, 4))


class RiseFallTime:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.OSC = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def test(self):
        RST(self.OSC)
        Oscilloscope(self.OSC).setChannelCoupling(1, "AC")
        Oscilloscope(self.OSC).setTriggerMode("EDGE")
        Oscilloscope(self.OSC).setTriggerCoupling("AC")
        Oscilloscope(self.OSC).setTriggerSweepMode("NORM")
        Oscilloscope(self.OSC).setTriggerSlope("RISE")
        Oscilloscope(self.OSC).setTriggerSource("1")
        Oscilloscope(self.OSC).setTimeScale("10e-6")
        Oscilloscope(self.OSC).setVerticalScale(1, 1)
        Oscilloscope(self.OSC).setTriggerEdgeLevel(1)
        Oscilloscope(self.OSC).setTriggerHFReject(1)
        Oscilloscope(self.OSC).setTriggerNoiseReject(1)
        Display(self.ELoad).displayState(self.ELoad_Channel)
        Function(self.ELoad).setMode("Current", self.ELoad_Channel)
        Voltage(self.PSU).setSenseMode("EXT", 1)
        Apply(self.PSU).write(self.PSU_Channel, 30, 20)
        Output(self.PSU).setOutputState("ON")
        Current(self.ELoad).setOutputCurrent(6.66, self.ELoad_Channel)
        Output(self.ELoad).setOutputStateC("ON", self.ELoad_Channel)

        Oscilloscope(self.OSC).setSingleMode()
        WAI(self.OSC)
        sleep(1)
        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)
        WAI(self.OSC)
        V_max = float(Oscilloscope(self.OSC).getMaximumVoltage())
        Oscilloscope(self.OSC).setThresholdMode("Voltage")
        Oscilloscope(self.OSC).setUpperLimit(0.99 * V_max)
        Oscilloscope(self.OSC).setLowerLimit(0)
        rise_time = float(Oscilloscope(self.OSC).getRiseTime(1))

        Oscilloscope(self.OSC).setLowerLimit("15e-3")
        fall_time = float(Oscilloscope(self.OSC).getFallTime(1))

        print(
            f"Total Transient Time with Voltage Settling Band of 15mV, {rise_time+fall_time}s"
        )

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)

        Output(self.PSU).setOutputState("OFF")

    def execute(
        self,
        ELoad,
        PSU,
        OSC,
        ELoad_Channel,
        PSU_Channel,
        OSC_Channel,
        setMode,
        setVoltageSense,
        V_rating,
        I_rating,
        Channel_CouplingMode,
        Trigger_Mode,
        Trigger_CouplingMode,
        Trigger_SweepMode,
        Trigger_SlopeMode,
        TimeScale,
        VerticalScale,
        I_Step,
        V_settling_band,
    ):
        """Test for determining the Transient Recovery Time of DUT

        The test begins by initializing all the settings for Oscilloscope and other instruments.
        The PSU is then set to output full load followed by activating single mode on the oscilloscope.
        The Eload is then turned off, which would trigger the oscilloscope to show a transient wave. The
        transient wave is then measured using the built in functions. The transient time is caluclated by
        totalling the rise and fall time where the threshold is set manually depending on the voltage
        settling band.

        Args:
            ELoad: String determining the VISA Address of ELoad.
            PSU: String determining the VISA Address of PSU.
            OSC: String determining the VISA Address of Oscilloscope.
            ELoad_Channel: Integer containing the Channel Number used for ELoad.
            PSU_Channel: Integer containing the Channel Number used for PSU.
            OSC_Channel: Integer containing the Channel Number used for Oscilloscope.
            setMode: String determining the Priority Mode of the ELoad.
            setVoltageSense: String determining the Voltage Sense of the PSU.
            V_rating: Float containing the Voltage Rating of the PSU.
            I_rating: Float containing the Current Rating of the PSU.
            Channel_CouplingMode: String determining the Channel Coupling Mode.
            Trigger_Mode: String determining the Trigger Mode.
            Trigger_CouplingMode: String determining the Trigger Coupling Mode.
            Trigger_SweepMode: String determining the Trigger Sweep Mode.
            Trigger_SlopeMode: String determining the Trigger Slope Mode.
            TimeScale: Float determining the time scale of the oscilloscope display.
            VerticalScale: Float determining the vertical scale of the oscilloscope display.
            I_Step: Float determining the value of current step.
            V_settling_band: Float determining the desired voltage settling band.

        Raises:
            VisaIOError: An error occured when opening PyVisa Resources.
        """

        # Instruments Settings
        Oscilloscope(OSC).setChannelCoupling(OSC_Channel, Channel_CouplingMode)
        Oscilloscope(OSC).setTriggerMode(Trigger_Mode)
        Oscilloscope(OSC).setTriggerCoupling(Trigger_CouplingMode)
        Oscilloscope(OSC).setTriggerSweepMode(Trigger_SweepMode)
        Oscilloscope(OSC).setTriggerSlope(Trigger_SlopeMode)
        Oscilloscope(OSC).setTimeScale(TimeScale)
        Oscilloscope(self.OSC).setTriggerSource(OSC_Channel)
        Oscilloscope(OSC).setVerticalScale(VerticalScale, OSC_Channel)
        Oscilloscope(self.OSC).setTriggerEdgeLevel(OSC_Channel)
        Oscilloscope(self.OSC).setTriggerHFReject(1)
        Oscilloscope(self.OSC).setTriggerNoiseReject(1)

        Display(ELoad).displayState(ELoad_Channel)
        Function(ELoad).setMode(setMode, ELoad_Channel)
        Voltage(PSU).setSenseMode(setVoltageSense, PSU_Channel)
        Apply(PSU).write(PSU_Channel, V_rating, I_rating)
        Output(PSU).setOutputState("ON")
        Current(ELoad).setOutputCurrent(I_Step, ELoad_Channel)
        Output(ELoad).setOutputStateC("ON", ELoad_Channel)

        Oscilloscope(OSC).setSingleMode()
        WAI(OSC)
        sleep(1)
        Output(ELoad).setOutputStateC("OFF", ELoad_Channel)
        WAI(self.OSC)

        V_max = float(Oscilloscope(OSC).getMaximumVoltage())
        Oscilloscope(self.OSC).setThresholdMode("Voltage")
        Oscilloscope(self.OSC).setUpperLimit(0.99 * V_max)
        Oscilloscope(self.OSC).setLowerLimit(0)
        rise_time = float(Oscilloscope(OSC).getRiseTime(1))

        Oscilloscope(self.OSC).setLowerLimit(V_settling_band)
        fall_time = float(Oscilloscope(OSC).getFallTime(1))

        print(
            f"Total Transient Time with Voltage Settling Band of 15mV, {rise_time+fall_time}s"
        )

        Output(self.ELoad).setOutputStateC("OFF", self.ELoad_Channel)

        Output(self.PSU).setOutputState("OFF")


class ProgrammingSpeedTest:
    def __init__(self, ADDR1, ADDR2, ADDR3, ELoad_Channel, PSU_Channel):
        self.ELoad = ADDR1
        self.PSU = ADDR2
        self.OSC = ADDR3
        self.ELoad_Channel = ELoad_Channel
        self.PSU_Channel = PSU_Channel

    def test(self):
        RST(self.OSC)
        Oscilloscope(self.OSC).setVerticalScale(5, 1)
        Oscilloscope(self.OSC).setTriggerEdgeLevel(19, 1)
        Oscilloscope(self.OSC).setTriggerMode("EDGE")
        Oscilloscope(self.OSC).setTriggerCoupling("DC")
        Oscilloscope(self.OSC).setTriggerSweepMode("NORM")
        Oscilloscope(self.OSC).setTriggerSlope("EITHER")
        Oscilloscope(self.OSC).setTriggerSource("1")
        Oscilloscope(self.OSC).setTimeScale("10e-3")
        Oscilloscope(self.OSC).setVerticalOffset(15, 1)
        Oscilloscope(self.OSC).setThresholdMode("Voltage")
        Oscilloscope(self.OSC).setUpperLimit(29)
        Oscilloscope(self.OSC).setLowerLimit(1)

        Voltage(self.PSU).setSenseMode("EXT", 1)
        Apply(self.PSU).write(self.PSU_Channel, 1, 2)
        Output(self.PSU).setOutputState("ON")
        Oscilloscope(self.OSC).setSingleMode()
        WAI(self.OSC)
        sleep(1)

        Apply(self.PSU).write(self.PSU_Channel, 30, 2)
        sleep(1)
        print(Oscilloscope(self.OSC).getRiseTime(1))
        sleep(1)
        Oscilloscope(self.OSC).setSingleMode()
        sleep(1)
        Apply(self.PSU).write(self.PSU_Channel, 1, 2)
        sleep(1)
        print(Oscilloscope(self.OSC).getFallTime(1))
        Output(self.PSU).setOutputState("OFF")

    def execute(
        self,
        PSU,
        OSC,
        PSU_Channel,
        OSC_Channel,
        setVoltageSense,
        V_Lower,
        V_Upper,
        Trigger_Mode,
        Trigger_CouplingMode,
        Trigger_SweepMode,
        Trigger_SlopeMode,
        Upper_Bound,
        Lower_Bound,
    ):
        RST(OSC)
        Oscilloscope(OSC).setVerticalScale(5, OSC_Channel)
        Oscilloscope(OSC).setTriggerEdgeLevel(float(V_Upper) - 1, OSC_Channel)
        Oscilloscope(OSC).setTriggerMode(Trigger_Mode)
        Oscilloscope(OSC).setTriggerCoupling(Trigger_CouplingMode)
        Oscilloscope(OSC).setTriggerSweepMode(Trigger_SweepMode)
        Oscilloscope(OSC).setTriggerSlope(Trigger_SlopeMode)
        Oscilloscope(OSC).setTriggerSource(OSC_Channel)
        Oscilloscope(OSC).setTimeScale(10e-3)
        Oscilloscope(OSC).setVerticalOffset(15, OSC_Channel)
        Oscilloscope(OSC).setThresholdMode("Voltage")
        Upper_Threshold = (float(Upper_Bound) / 100) * float(V_Upper)
        Lower_Threshold = (1 + float(Lower_Bound) / 100) * float(V_Lower)
        Oscilloscope(OSC).setUpperLimit(round(Upper_Threshold, 1))
        Oscilloscope(OSC).setLowerLimit(round(Lower_Threshold, 1))

        Voltage(PSU).setSenseMode(setVoltageSense, PSU_Channel)
        Apply(PSU).write(PSU_Channel, V_Lower, 2)
        Output(PSU).setOutputState("ON")
        Oscilloscope(OSC).setSingleMode()
        WAI(OSC)
        sleep(1)

        Apply(PSU).write(PSU_Channel, V_Upper, 2)
        sleep(1)
        Rise_Time = float(Oscilloscope(OSC).getRiseTime(OSC_Channel))
        print(f"Rise Time from{Lower_Bound}% to {Upper_Bound}%: {Rise_Time} s")
        sleep(1)
        Oscilloscope(OSC).setSingleMode()
        sleep(1)
        Apply(PSU).write(PSU_Channel, V_Lower, 2)
        sleep(1)
        Fall_Time = float(Oscilloscope(OSC).getFallTime(OSC_Channel))

        print(f"Fall Time from {Upper_Bound}% to {Lower_Bound}%: {Fall_Time} s")
        WAI(OSC)
        Output(PSU).setOutputState("OFF")
