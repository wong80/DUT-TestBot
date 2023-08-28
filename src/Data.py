""" This module contains all of the data processing and visualization tools and functions

    The module mainly uses maltplotlib to plot graphs and pandas to process the data. 

"""

import sys
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)
from IEEEStandard import IDN
from Keysight import System


class datatoCSV_Accuracy(object):
    """This class is used to preprocess the data collected for Voltage/Accuracy test and export CSV Files

    Attributes:
        infoList: List containing information collected from Program
        dataList List containing measured data collected from DUT

    """

    def __init__(self, infoList, dataList):
        """This function initializes the preprocessing of data and generate CSV file

            This function begins by extracting the list provided as an arguement into
            multiple columns. The absolute and percentage error is then calculted using
            the columns, the columns are then converted into dataframes which is then
            all compiled into a csv file.

        Args:
            infoList: List containing all the data that is sent from the program.
            dataList: List containing all the data that is collected from the DUT.
            Vset: Column containing information regarding the Voltage Set.
            Iset: Column containing information regarding the Current Set.
            Key: Column containing key to differentiate different current iterations.
            Vmeasured: Column containing information regarding Voltage Measured.
            Imeasured: Column containing information regarding Current Measured.
            Vabsolute_error: Column containing information regarding absolute error (Voltage).
            Vpercent_error: Column containing information regarding percentage error (Voltage).
            Iabsolute_error: Column containing information regarding absolute error (Current).
            Ipercent_error: Column containing information regarding percentage error (Current).


        """

        Vset = pd.Series(self.column(infoList, 0))
        Iset = pd.Series(self.column(infoList, 1))
        Key = pd.Series(self.column(infoList, 2))
        Vmeasured = pd.Series(self.column(dataList, 0))
        Imeasured = pd.Series(self.column(dataList, 1))

        Vabsolute_error = Vset - Vmeasured
        Vpercent_error = Vabsolute_error / Vset * 100

        Iabsolute_error = Iset - Imeasured
        Ipercent_error = Iabsolute_error / Iset * 100

        VsetF = Vset.to_frame(name="Voltage Set")
        IsetF = Iset.to_frame(name="Current Set")
        keyF = Key.to_frame(name="key")
        VmeasuredF = Vmeasured.to_frame(name="Voltage Measured")
        ImeasuredF = Imeasured.to_frame(name="Current Measured")

        Vabsolute_errorF = Vabsolute_error.to_frame(name="Voltage Absolute Error")
        Vpercent_errorF = Vpercent_error.to_frame(name="Voltage Percentage Error (%)")
        Iabsolute_errorF = Iabsolute_error.to_frame(name="Current Absolute Error")
        Ipercent_errorF = Ipercent_error.to_frame(name="Current Percentage Error (%)")
        CSV1 = pd.concat(
            [
                VsetF,
                IsetF,
                VmeasuredF,
                ImeasuredF,
                keyF,
                Vabsolute_errorF,
                Vpercent_errorF,
                Iabsolute_errorF,
                Ipercent_errorF,
            ],
            axis=1,
        )

        CSV1.to_csv("csv/data.csv", index=False)

    def column(self, matrix, i):
        """Function to convert rows of data from list to a column

        Args:
            matrix: The 2D matrix to store the column data
            i: to iterate through loop
        """
        return [row[i] for row in matrix]


class datatoCSV_Regulation(object):
    """This class is used to preprocess the data collected for Load Regulation Tests and export CSV Files"""

    def __init__(self, infoList, dataList, V_rating, param1, param2, V_NL):
        """This function initializes the preprocessing of data and generate CSV file

            The function begins by extracting the data from the list passed as an arguement
            into different columns labeled. The Voltage Regulation is then calculated using
            these information.

            A plot is then made using the dataframes collected above. A scatter of the Voltage
            Regulation is plotted with a horizontal line of a y axis of the voltage regulation
            determined by the desired specifications. Condition is provided that if the voltage
            regulation at the point is lower than the voltage regulation boundary, the scatter
            point will be visibilly larger and red.

        Args:
            infoList: List containing all the data that is sent from the program.
            dataList: List containing all the data that is collected from the DUT.
            V_NL: List containing the nominal value when voltage is measured during no load.
            V_FL: Float containing the nominal value when voltage is measured during full load.
            Current_Programmed: Column containing the nominal value to program the output current of DUT.
            Voltage_Programmed: Column containing the nominal value to program the output voltage of DUT.
            Load_Measured: Float containing the nominal value of total Load of DUT.
            Voltage_Error: Column containing the calculated voltage error.
            Voltage_Regulation: Column containing the calculated voltage regulation.

        """
        self.infoList = infoList
        self.dataList = dataList
        self.V_NL = V_NL
        self.Current_Programmed = pd.Series(self.column(infoList, 0))
        self.Load_Programmed = pd.Series(self.column(infoList, 1))
        self.Voltage_Measured = pd.Series(self.column(dataList, 0))
        self.Load_Measured = pd.Series(self.column(dataList, 1))

        self.Voltage_Error = V_NL - self.Voltage_Measured
        self.Voltage_Regulation = ((V_NL - self.Voltage_Error) / self.V_NL) * 100
        self.Voltage_Regulation_ErrorBoundary = (V_rating * param1) + param2
        self.Voltage_Regulation_Boundary = (
            (V_rating - self.Voltage_Regulation_ErrorBoundary) / self.V_NL
        ) * 100

        self.condition = self.Voltage_Regulation > self.Voltage_Regulation_Boundary

        self.Current_ProgrammedF = self.Current_Programmed.to_frame(name="Current Set")
        self.Load_ProgrammedF = self.Load_Programmed.to_frame(name="Load Set")
        self.Voltage_MeasuredF = self.Voltage_Measured.to_frame(name="Voltage Measured")
        self.Load_MeasuredF = self.Load_Measured.to_frame(name="Load Measured")

        self.Voltage_ErrorF = self.Voltage_Error.to_frame(name="Voltage Absolute Error")
        self.Voltage_RegulationF = self.Voltage_Regulation.to_frame(
            name="Voltage Regulation(%)"
        )
        print(self.Voltage_Regulation_Boundary)
        self.conditionF = self.condition.to_frame(name="Condition")

        self.z = self.condition.to_numpy()
        self.colour_condition = np.where(self.z == True, "black", "red")
        self.size_condition = np.where(self.z == True, 6, 12)
        self.alpha_condition = np.where(self.z == True, 0, 1)

        self.CSV1 = pd.concat(
            [
                self.Current_ProgrammedF,
                self.Load_ProgrammedF,
                self.Voltage_MeasuredF,
                self.Load_MeasuredF,
                self.Voltage_ErrorF,
                self.Voltage_RegulationF,
                self.conditionF,
            ],
            axis=1,
        )

        self.CSV1.to_csv("csv/data.csv", index=False)

        plt.scatter(
            self.Current_Programmed,
            self.Voltage_Regulation,
            color=self.colour_condition,
            s=self.size_condition,
            alpha=self.alpha_condition,
        )
        plt.axhline(
            y=self.Voltage_Regulation_Boundary,
            color="r",
            linestyle="-",
            label="Boundary",
        )

        plt.plot(
            self.Current_Programmed,
            self.Voltage_Regulation,
            label="Voltage Regulation(%)",
            color="blue",
            linewidth=1,
        )
        plt.legend(loc="lower left")
        plt.show()

    def column(self, matrix, i):
        """Function to convert rows of data from list to a column

        Args:
            matrix: The 2D matrix to store the column data
            i: to iterate through loop
        """
        return [row[i] for row in matrix]


class datatoGraph(datatoCSV_Accuracy):
    """Child class of datatoCSV_Accuracy to plot the graph"""

    def __init__(self, infoList, dataList):
        super().__init__(infoList, dataList)
        self.data = pd.read_csv("csv/data.csv")

    def errorBoundary(self, param1, param2, UNIT, x, x_err, y):
        """Function is used to determine and plot the error boundaries of voltage/current accuracy

            The function begins by defining certain parameters, it also extracts data from method
            ScatterCompare() that has determined which points have passed or failed the given condition.

            The valyes given will change how the points are plotted on the scatter plot.
            A scatter plot is then plotted on the same plane with the error boundary lines.
            For scatter points that do not meet the condition will appear visibly red and larger.

            The function is divided into two different sections depending on the condition, condition
            whether we are comparing programming accuracy of voltage or current.

        Args:
            upper_error_limit: float value of the upper error boundary determined from specification.
            lower_error_limit: float value of the lower error boundary determined from specification.
            condition1: Boolean which indicates if the absolute error is higher than upper error limit.
            condition2: Boolean which indicates if the absolute error is lower than lower error limit.
            boolList: List containing all the conditions of each point whether they passed or failed.

        """
        boolList = []

        if UNIT.upper() == "VOLTAGE":
            upper_error_limit = (param1 * x + param2) * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit

            condition1 = upper_error_limit < x_err
            condition2 = lower_error_limit > x_err

            for i in range(condition1.count()):
                if condition1.iloc[i] | condition2.iloc[i]:
                    self.condition = "FAIL"
                    boolList.append(self.condition)
                else:
                    self.condition = "PASS"
                    boolList.append(self.condition)

            self.condition_series = pd.Series(boolList)

            self.upper_error_limitF = upper_error_limit.to_frame(
                name="Upper Error Boundary (" + UNIT + " )"
            )
            self.lower_error_limitF = lower_error_limit.to_frame(
                name="Lower Error Boundary (" + UNIT + " )"
            )

            self.conditionF = self.condition_series.to_frame(name="Condition ?")

            self.z = self.condition_series.to_numpy()
            self.colour_condition = np.where(self.z == "PASS", "black", "red")
            self.size_condition = np.where(self.z == "PASS", 6, 12)
            self.alpha_condition = np.where(self.z == "PASS", 0, 1)

            plt.scatter(
                x,
                x_err,
                color=self.colour_condition,
                s=self.size_condition,
                alpha=self.alpha_condition,
            )

            plt.plot(
                x,
                x_err,
                label="Current = " + str(y.iloc[0]["Current Set"]),
            )

            plt.title(UNIT)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Percentage Error (%)")

        elif UNIT.upper() == "CURRENT":
            upper_error_limit = param1 * x + param2 * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit

            condition1 = upper_error_limit < x_err
            condition2 = lower_error_limit > x_err

            for i in range(condition1.count()):
                if condition1.iloc[i] | condition2.iloc[i]:
                    self.condition = "FAIL"
                    boolList.append(self.condition)
                else:
                    self.condition = "PASS"
                    boolList.append(self.condition)

            self.condition_series = pd.Series(boolList)

            self.upper_error_limitF = upper_error_limit.to_frame(
                name="Upper Error Boundary (" + UNIT + " )"
            )
            self.lower_error_limitF = lower_error_limit.to_frame(
                name="Lower Error Boundary (" + UNIT + " )"
            )

            self.conditionF = self.condition_series.to_frame(name="Condition ?")

            self.z = self.condition_series.to_numpy()
            self.colour_condition = np.where(self.z == "PASS", "black", "red")
            self.size_condition = np.where(self.z == "PASS", 6, 12)
            self.alpha_condition = np.where(self.z == "PASS", 0, 1)

            plt.scatter(
                x,
                x_err,
                color=self.colour_condition,
                s=self.size_condition,
                alpha=self.alpha_condition,
            )

            plt.plot(
                x,
                x_err,
                label="Voltage = " + str(y.iloc[0]["Voltage Set"]),
            )
            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Current (A)")
            plt.ylabel("Percentage Error (%)")

    def scatterCompareVoltage(self, param1, param2):
        """Function is used to determine and plot the error boundaries of voltage accuracy

            The function begins by computing the error boundaries based on specifications.
            The error boundaries are then compared using data extracted from parent class.
            The boolList will collect information whether the accuracy at certain point has
            been reached. The boolList will append a "PASS" if it does, else "FAIL".
            A scatter plot is then plotted on the same plane with the error boundary lines.
            For scatter points that do not meet the condition will appear visibly red and larger.



        Args:
            upper_error_limit: float value of the upper error boundary determined from specification
            lower_error_limit: float value of the lower error boundary determined from specification
            condition1: Boolean which indicates if the absolute error is higher than upper error limit.
            condition2: Boolean which indicates if the absolute error is lower than lower error limit.
            boolList: List containing all the conditions of each point whether they passed or failed.


        """
        ungrouped_df = pd.read_csv("csv/data.csv", index_col=False)
        grouped_df = ungrouped_df.groupby(["key"])
        [grouped_df.get_group(x) for x in grouped_df.groups]

        upper_error_limitC = pd.Series()
        lower_error_limitC = pd.Series()
        conditionC = pd.Series()

        for x in range(len(grouped_df)):
            Vset = grouped_df.get_group(x)[["Voltage Set"]]
            Iset = grouped_df.get_group(x)[["Current Set"]]
            Vpercent_error = grouped_df.get_group(x)[["Voltage Percentage Error (%)"]]
            Ipercent_error = grouped_df.get_group(x)[["Current Percentage Error (%)"]]

            VsetS = Vset.squeeze()
            Vpercent_errorS = Vpercent_error.squeeze()

            boolList = []

            upper_error_limit = (param1 * VsetS + param2) * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit

            condition1 = upper_error_limit < Vpercent_errorS
            condition2 = lower_error_limit > Vpercent_errorS

            for i in range(condition1.count()):
                if condition1.iloc[i] | condition2.iloc[i]:
                    self.condition = "FAIL"
                    boolList.append(self.condition)
                else:
                    self.condition = "PASS"
                    boolList.append(self.condition)

            self.condition_series = pd.Series(boolList)

            self.upper_error_limitF = upper_error_limit.to_frame(
                name="Upper Error Boundary ( Voltage )"
            )
            self.lower_error_limitF = lower_error_limit.to_frame(
                name="Lower Error Boundary ( Voltage )"
            )

            self.conditionF = self.condition_series.to_frame(name="Condition ?")

            self.z = self.condition_series.to_numpy()
            self.colour_condition = np.where(self.z == "PASS", "black", "red")
            self.size_condition = np.where(self.z == "PASS", 6, 12)
            self.alpha_condition = np.where(self.z == "PASS", 0, 1)

            plt.scatter(
                VsetS,
                Vpercent_errorS,
                color=self.colour_condition,
                s=self.size_condition,
                alpha=self.alpha_condition,
            )

            plt.plot(
                VsetS,
                Vpercent_errorS,
                label="Current = " + str(Iset.iloc[0]["Current Set"]),
            )

            plt.title("Voltage")
            plt.xlabel("Voltage (V)")
            plt.ylabel("Percentage Error (%)")

            upper_error_limitC = pd.concat([upper_error_limitC, self.upper_error_limit])
            lower_error_limitC = pd.concat([lower_error_limitC, self.lower_error_limit])
            conditionC = pd.concat([conditionC, self.condition_series])

        plt.plot(
            Vset,
            self.upper_error_limit,
            label="Upper Bound",
            color="red",
            linewidth=1,
        )
        plt.plot(
            Vset,
            self.lower_error_limit,
            label="Lower Bound",
            color="red",
            linewidth=1,
        )

        conditionF = conditionC.to_frame(name="Condition ?")
        conditionFF = conditionF.reset_index(drop=True)

        upper_error_limitF = pd.DataFrame(
            upper_error_limitC, columns=["Upper Error Boundary"]
        )
        lower_error_limitF = pd.DataFrame(
            lower_error_limitC, columns=["Lower Error Boundary"]
        )

        ungrouped_df.drop(columns=["key"], inplace=True)
        self.CSV2 = pd.concat(
            [
                ungrouped_df,
                upper_error_limitF,
                lower_error_limitF,
                conditionFF,
            ],
            axis=1,
        )

        self.CSV2.to_csv("csv/error.csv", index=False)

        plt.legend(loc="lower left")
        plt.savefig("images/Chart.png")

    def scatterCompareCurrent(self, param1, param2):
        """Function is used to determine and plot the error boundaries of current accuracy

            The function begins by computing the error boundaries based on specifications.
            The error boundaries are then compared using data extracted from parent class.
            The boolList will collect information whether the accuracy at certain point has
            been reached. The boolList will append a "PASS" if it does, else "FAIL".
            A scatter plot is then plotted on the same plane with the error boundary lines.
            For scatter points that do not meet the condition will appear visibly red and larger.



        Args:
            upper_error_limit: float value of the upper error boundary determined from specification
            lower_error_limit: float value of the lower error boundary determined from specification
            condition1: Boolean which indicates if the absolute error is higher than upper error limit.
            condition2: Boolean which indicates if the absolute error is lower than lower error limit.
            boolList: List containing all the conditions of each point whether they passed or failed.


        """
        ungrouped_df = pd.read_csv("csv/data.csv", index_col=False)
        grouped_df = ungrouped_df.groupby(["key"])
        [grouped_df.get_group(x) for x in grouped_df.groups]

        upper_error_limitC = pd.Series()
        lower_error_limitC = pd.Series()
        conditionC = pd.Series()

        for x in range(len(grouped_df)):
            Vset = grouped_df.get_group(x)[["Voltage Set"]]
            Iset = grouped_df.get_group(x)[["Current Set"]]
            Vpercent_error = grouped_df.get_group(x)[["Voltage Percentage Error (%)"]]
            Ipercent_error = grouped_df.get_group(x)[["Current Percentage Error (%)"]]

            IsetS = Iset.squeeze()
            Ipercent_errorS = Ipercent_error.squeeze()

            boolList = []

            upper_error_limit = (param1 * IsetS + param2) * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit

            condition1 = upper_error_limit < Ipercent_errorS
            condition2 = lower_error_limit > Ipercent_errorS

            for i in range(condition1.count()):
                if condition1.iloc[i] | condition2.iloc[i]:
                    self.condition = "FAIL"
                    boolList.append(self.condition)
                else:
                    self.condition = "PASS"
                    boolList.append(self.condition)

            self.condition_series = pd.Series(boolList)

            self.upper_error_limitF = upper_error_limit.to_frame(
                name="Upper Error Boundary ( Voltage )"
            )
            self.lower_error_limitF = lower_error_limit.to_frame(
                name="Lower Error Boundary ( Voltage )"
            )

            self.conditionF = self.condition_series.to_frame(name="Condition ?")

            self.z = self.condition_series.to_numpy()
            self.colour_condition = np.where(self.z == "PASS", "black", "red")
            self.size_condition = np.where(self.z == "PASS", 6, 12)
            self.alpha_condition = np.where(self.z == "PASS", 0, 1)

            plt.scatter(
                IsetS,
                Ipercent_errorS,
                color=self.colour_condition,
                s=self.size_condition,
                alpha=self.alpha_condition,
            )

            plt.plot(
                IsetS,
                Ipercent_errorS,
                label="Voltage = " + str(Vset.iloc[0]["Voltage Set"]),
            )

            plt.title("Current")
            plt.xlabel("Current (A)")
            plt.ylabel("Percentage Error (%)")

            upper_error_limitC = pd.concat([upper_error_limitC, self.upper_error_limit])
            lower_error_limitC = pd.concat([lower_error_limitC, self.lower_error_limit])
            conditionC = pd.concat([conditionC, self.condition_series])

        plt.plot(
            Iset,
            self.upper_error_limit,
            label="Upper Bound",
            color="red",
            linewidth=1,
        )
        plt.plot(
            Iset,
            self.lower_error_limit,
            label="Lower Bound",
            color="red",
            linewidth=1,
        )

        conditionF = conditionC.to_frame(name="Condition ?")
        conditionFF = conditionF.reset_index(drop=True)

        upper_error_limitF = pd.DataFrame(
            upper_error_limitC, columns=["Upper Error Boundary"]
        )
        lower_error_limitF = pd.DataFrame(
            lower_error_limitC, columns=["Lower Error Boundary"]
        )

        ungrouped_df.drop(columns=["key"], inplace=True)
        self.CSV2 = pd.concat(
            [
                ungrouped_df,
                upper_error_limitF,
                lower_error_limitF,
                conditionFF,
            ],
            axis=1,
        )

        self.CSV2.to_csv("csv/error.csv", index=False)

        plt.legend(loc="lower left")
        plt.savefig("images/Chart.png")


class instrumentData(object):
    """This class stores and facilitates the collection of Instrument Data to be placed in Excel Report

    Attributes:
        *args: arguements should contain strings of VISA Addresses of instruments used.
        instrumentIDN: List containing the Identification Name of the Instruments
        instrumentVersion: List containing the SCPI Version of the Instruments

    """

    def __init__(self, *args):
        instrumentIDN = []
        instrumentVersion = []

        for x in args:
            instrumentIDN.append(IDN(x).query())
            instrumentVersion.append(System(x).version())

        df1 = pd.DataFrame(instrumentIDN, columns=["Instruments Used: "])
        df2 = pd.DataFrame(instrumentVersion, columns=["SCPI Version"])

        instrument = pd.concat([df1, df2], axis=1)

        instrument.to_csv("csv/instrumentData.csv", index=False)


class dictGenerator(object):
    def __init__():
        pass

    def input(**kwargs):
        return kwargs
