import sys
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

sys.path.insert(
    1,
    r"C://Users//zhiywong//OneDrive - Keysight Technologies//Documents//GitHub//PyVisa//library",
)
from IEEEStandard import IDN
from Subsystems import System


class datatoCSV_Accuracy(object):
    def __init__(self, infoList, dataList):
        self.infoList = infoList
        self.dataList = dataList

        self.Vset = pd.Series(self.column(infoList, 0))
        self.Iset = pd.Series(self.column(infoList, 1))
        self.key = pd.Series(self.column(infoList, 2))
        self.Vmeasured = pd.Series(self.column(dataList, 0))
        self.Imeasured = pd.Series(self.column(dataList, 1))

        self.Vabsolute_error = self.Vset - self.Vmeasured
        self.Vpercent_error = self.Vabsolute_error / self.Vset * 100

        self.Iabsolute_error = self.Iset - self.Imeasured
        self.Ipercent_error = self.Iabsolute_error / self.Iset * 100

        self.VsetF = self.Vset.to_frame(name="Voltage Set")
        self.IsetF = self.Iset.to_frame(name="Current Set")
        self.keyF = self.key.to_frame(name="key")
        self.VmeasuredF = self.Vmeasured.to_frame(name="Voltage Measured")
        self.ImeasuredF = self.Imeasured.to_frame(name="Current Measured")

        self.Vabsolute_errorF = self.Vabsolute_error.to_frame(
            name="Voltage Absolute Error"
        )
        self.Vpercent_errorF = self.Vpercent_error.to_frame(
            name="Voltage Percentage Error (%)"
        )
        self.Iabsolute_errorF = self.Iabsolute_error.to_frame(
            name="Current Absolute Error"
        )
        self.Ipercent_errorF = self.Ipercent_error.to_frame(
            name="Current Percentage Error (%)"
        )
        self.CSV1 = pd.concat(
            [
                self.VsetF,
                self.IsetF,
                self.VmeasuredF,
                self.ImeasuredF,
                self.keyF,
                self.Vabsolute_errorF,
                self.Vpercent_errorF,
                self.Iabsolute_errorF,
                self.Ipercent_errorF,
            ],
            axis=1,
        )

        self.CSV1.to_csv("csv/data.csv", index=False)

    def column(self, matrix, i):
        return [row[i] for row in matrix]


class datatoCSV_Regulation(object):
    def __init__(self, infoList, dataList, V_rating, param1, param2):
        self.infoList = infoList
        self.dataList = dataList

        self.Current_Programmed = pd.Series(self.column(infoList, 0))
        self.Load_Programmed = pd.Series(self.column(infoList, 1))
        self.Voltage_Measured = pd.Series(self.column(dataList, 0))
        self.Load_Measured = pd.Series(self.column(dataList, 1))

        self.Voltage_Error = V_rating - self.Voltage_Measured
        self.Voltage_Regulation = ((V_rating - self.Voltage_Error) / V_rating) * 100
        self.Voltage_Regulation_ErrorBoundary = (V_rating * param1) + param2
        self.Voltage_Regulation_Boundary = (
            (V_rating - self.Voltage_Regulation_ErrorBoundary) / V_rating
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
        return [row[i] for row in matrix]


class datatoGraph(datatoCSV_Accuracy):
    def __init__(self, infoList, dataList):
        super().__init__(infoList, dataList)
        self.data = pd.read_csv("csv/data.csv")

    def errorBoundary(self, param1, param2, UNIT, x, x_err, y):
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
            upper_error_limit = self.param1 * x + self.param2 * 100
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

    def scatterCompare(self, Mode, param1, param2):
        self.Mode = Mode
        ungrouped_df = pd.read_csv("csv/data.csv")
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
            IsetS = Iset.squeeze()
            Ipercent_errorS = Ipercent_error.squeeze()

            if self.Mode.upper() == "VOLTAGE":
                self.errorBoundary(
                    param1, param2, self.Mode, VsetS, Vpercent_errorS, Iset
                )
            elif self.Mode.upper() == "CURRENT":
                self.errorBoundary(
                    param1, param2, self.Mode, IsetS, Ipercent_errorS, Vset
                )

            upper_error_limitC = pd.concat([upper_error_limitC, self.upper_error_limit])
            lower_error_limitC = pd.concat([lower_error_limitC, self.lower_error_limit])
            conditionC = pd.concat([conditionC, self.condition_series])

        if self.Mode.upper() == "VOLTAGE":
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
        elif self.Mode.upper() == "CURRENT":
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

        self.CSV2 = pd.concat(
            [
                self.VsetF,
                self.IsetF,
                self.VmeasuredF,
                self.ImeasuredF,
                self.Vabsolute_errorF,
                self.Vpercent_errorF,
                self.Iabsolute_errorF,
                self.Ipercent_errorF,
                upper_error_limitF,
                lower_error_limitF,
                conditionFF,
            ],
            axis=1,
        )

        self.CSV2.to_csv("csv/error.csv", index=False)

        plt.legend(loc="lower left")
        plt.savefig("images/Chart.png")

    def scatterCompareVoltage(self, param1, param2):
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


class instrumentData:
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
