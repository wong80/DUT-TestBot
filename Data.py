import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class datatoCSV(object):
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
            name="Current Percentage Error(%)"
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

        self.CSV1.to_csv("data.csv")

    def column(self, matrix, i):
        return [row[i] for row in matrix]


class datatoGraph(datatoCSV):
    def __init__(self, infoList, dataList):
        super().__init__(infoList, dataList)
        self.data = pd.read_csv("data.csv")

    def plotLine(self):
        self.data.plot(x="Voltage Set", y="Programmable Error (%)")
        plt.show()

    def errorBoundary(self, param1, param2, UNIT, Vset, Vpercent_error):
        self.param1 = param1
        self.param2 = param2

        if UNIT.upper() == "VOLTAGE":
            # a, b = np.polyfit(self.Vset, self.Vpercent_error, 1)
            upper_error_limit = self.param1 * Vset + self.param2 * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit
            upper_error_margin = upper_error_limit * 0.6
            lower_error_margin = lower_error_limit * 0.6

            self.condition1 = upper_error_limit < Vpercent_error
            self.condition2 = lower_error_limit > Vpercent_error

            self.condition = self.condition1 & self.condition2
            self.upper_error_limitF = upper_error_limit.to_frame(
                name="Upper Error Boundary (" + UNIT + " )"
            )
            self.lower_error_limitF = lower_error_limit.to_frame(
                name="Lower Error Boundary (" + UNIT + " )"
            )
            # self.upper_error_marginF = self.upper_error_margin.to_frame(
            #     name="Upper Error Margin" + UNIT
            # )
            # self.lower_error_marginF = self.lower_error_margin.to_frame(
            #     name="Lower Error Margin" + UNIT
            # )
            # # self.error_marginF = self.error_margin.to_frame(name="Error Margin")
            self.conditionF = self.condition.to_frame(name="Condition ?")

            self.z = self.condition.to_numpy()
            self.colour_condition = np.where(self.z == False, "k", "red")
            self.size_condition = np.where(self.z == False, 6, 12)

            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Percentage Error (%)")
            # plt.show()

        elif UNIT.upper() == "CURRENT":
            # a, b = np.polyfit(self.Iset, self.Ipercent_error, 1)
            self.upper_error_limit = self.param1 * self.Iset + self.param2 * 100
            self.lower_error_limit = -self.upper_error_limit
            self.upper_error_margin = self.upper_error_limit * 0.6
            self.lower_error_margin = self.lower_error_limit * 0.6

            self.condition1 = self.lower_error_margin < self.Ipercent_error
            self.condition2 = self.upper_error_margin > self.Ipercent_error

            self.condition = self.condition1 & self.condition2
            self.upper_error_limitF = self.upper_error_limit.to_frame(
                name="Upper Error Boundary" + UNIT
            )
            self.lower_error_limitF = self.lower_error_limit.to_frame(
                name="Lower Error Boundary" + UNIT
            )
            self.upper_error_marginF = self.upper_error_margin.to_frame(
                name="Upper Error Margin" + UNIT
            )
            self.lower_error_marginF = self.lower_error_margin.to_frame(
                name="Lower Error Margin" + UNIT
            )
            # self.error_marginF = self.error_margin.to_frame(name="Error Margin")
            # self.conditionF = self.condition.to_frame(name="Condition ?")

            # self.CSV2 = pd.concat(
            #     [
            #         self.data,
            #         self.upper_error_limitF,
            #         self.lower_error_limitF,
            #         self.conditionF,
            #     ],
            #     axis=1,
            # )
            # self.CSV2.to_csv("graph.csv")

            # z = self.condition.to_numpy()

            # colour_condition = np.where(z == True, "k", "red")
            # size_condition = np.where(z == True, 6, 12)

            # plt.scatter(
            #     self.Iset, self.Ipercent_error, color=colour_condition, s=size_condition
            # )

            plt.plot(
                self.Iset,
                self.upper_error_limit,
                label="Upper Bound",
                color="red",
                linewidth=1,
            )
            plt.plot(
                self.Iset,
                self.lower_error_limit,
                label="Lower Bound",
                color="red",
                linewidth=1,
            )
            plt.plot(
                self.Iset,
                self.upper_error_margin,
                label="Upper Margin",
                color="blue",
                linewidth=1,
            )
            plt.plot(
                self.Iset,
                self.lower_error_margin,
                label="Lower Margin",
                color="blue",
                linewidth=1,
            )

            # plt.plot(
            #     self.Iset,
            #     a * self.Iset + b,
            #     label="Measured",
            #     color="green",
            #     linewidth=1,
            # )
            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Current (I)")
            plt.ylabel("Percentage Error (%)")
            # plt.show()

    def plotAbsScatter(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

        a, b = np.polyfit(self.Vset, self.percent_error, 1)
        self.error_limit = self.param1 * self.Vset + self.param2 * 100
        self.error_margin = self.error_limit * 0.6
        self.condition = self.error_margin < self.percent_error

        self.error_limitF = self.error_limit.to_frame(name="Error Limit")
        # self.error_marginF = self.error_margin.to_frame(name="Error Margin")
        self.conditionF = self.condition.to_frame(name="Condition ?")

        self.CSV2 = pd.concat([self.data, self.error_limitF, self.conditionF], axis=1)
        self.CSV2.to_csv("graph.csv")

        z = self.condition.to_numpy()

        colour_condition = np.where(z == False, "k", "red")
        size_condition = np.where(z == False, 6, 12)
        plt.scatter(
            self.Vset, self.percent_error, color=colour_condition, s=size_condition
        )

        plt.plot(
            self.Vset,
            self.error_limit,
            label="Error Rate (%)",
            color="red",
            linewidth=1,
        )
        plt.plot(
            self.Vset,
            self.error_margin,
            label="Error Margin (&)",
            color="blue",
            linewidth=1,
        )

        plt.plot(
            self.Vset, a * self.Vset + b, label="results", color="green", linewidth=1
        )
        plt.legend(loc="upper left")
        plt.xlabel("Voltage (V)")
        plt.ylabel("Percentage Error (%)")
        plt.show()

    def plotCorr(self):
        self.powerSet = self.Vset * self.Iset
        self.powerCalc = self.Vmeasured * self.Imeasured

        self.powerSetF = self.powerSet.to_frame(name="Power Set")
        self.powerCalcF = self.powerCalc.to_frame(name="Power Measured")

        self.CSV3 = pd.concat(
            [
                self.VsetF,
                self.IsetF,
                self.powerSetF,
                self.powerCalcF,
                self.VmeasuredF,
                self.ImeasuredF,
                self.Vabsolute_errorF,
                self.Vpercent_errorF,
                self.Iabsolute_errorF,
                self.Ipercent_errorF,
            ],
            axis=1,
        )

        plt.scatter(self.Vset, self.powerCalc, color="red")
        # a, b = np.polyfit(self.Vset, self.powerSet, 1)
        # c, d = np.polyfit(self.Vset, self.powerCalc, 1)

        self.CSV3.to_csv("power.csv")

        # plt.plot(self.Vset, self.Iset, label="Ideal Power", color="blue", linewidth=1)
        # plt.plot(
        #     self.Vset, self.powerCalc, label="Actual Power", color="red", linewidth=1
        # )
        plt.xlabel("Voltage")
        plt.ylabel("Power")
        plt.legend(loc="upper left")

        plt.show()

    def scatterCompare(self):
        ungrouped_df = pd.read_csv("data.csv")
        grouped_df = ungrouped_df.groupby(["key"])
        [grouped_df.get_group(x) for x in grouped_df.groups]

        upper_error_limitC = pd.Series()
        lower_error_limitC = pd.Series()
        conditionC = pd.Series()
        for x in range(len(grouped_df)):
            Vset = grouped_df.get_group(x)[["Voltage Set"]]
            Iset = grouped_df.get_group(x)[["Current Set"]]
            Vpercent_error = grouped_df.get_group(x)[["Voltage Percentage Error (%)"]]

            VsetS = Vset.squeeze()
            Vpercent_errorS = Vpercent_error.squeeze()

            # self.errorBoundary(0.00025, 0.0015, "Voltage", VsetS, Vpercent_errorS)
            self.param1 = 0.00025
            self.param2 = 0.0015
            upper_error_limit = self.param1 * VsetS + self.param2 * 100
            lower_error_limit = -upper_error_limit

            a, b = np.polyfit(VsetS, Vpercent_errorS, 1)

            condition1 = upper_error_limit < Vpercent_errorS
            condition2 = lower_error_limit > Vpercent_errorS

            condition = condition1 | condition2

            upper_error_limitC = pd.concat([upper_error_limitC, upper_error_limit])
            lower_error_limitC = pd.concat([lower_error_limitC, lower_error_limit])
            conditionC = pd.concat([conditionC, condition])

            z = condition.to_numpy()
            colour_condition = np.where(z == False, "k", "red")
            size_condition = np.where(z == False, 6, 12)

            plt.scatter(
                Vset,
                Vpercent_errorS,
                label="Current = " + str(Iset.iloc[0]["Current Set"]),
                color=colour_condition,
                s=size_condition,
            )

            plt.plot(Vset, a * Vset + b)

        plt.plot(
            Vset,
            upper_error_limit,
            label="Upper Bound",
            color="red",
            linewidth=1,
        )
        plt.plot(
            Vset,
            lower_error_limit,
            label="Lower Bound",
            color="red",
            linewidth=1,
        )

        conditionF = conditionC.to_frame(name="Condition ?")
        upper_error_limitF = pd.DataFrame(
            upper_error_limitC, columns=["Upper Error Boundary"]
        )
        lower_error_limitF = pd.DataFrame(
            lower_error_limitC, columns=["Lower Error Boundary"]
        )

        CSV2 = pd.concat(
            [
                ungrouped_df,
                upper_error_limitF,
                lower_error_limitF,
                conditionF,
            ],
            axis=1,
        )

        CSV2.to_csv("error.csv")

        plt.legend(loc="upper left")
        plt.show()
