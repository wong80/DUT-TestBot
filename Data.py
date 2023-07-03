import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class datatoCSV(object):
    def __init__(self, infoList, dataList):
        self.infoList = infoList
        self.dataList = dataList

        self.Vset = pd.Series(self.column(infoList, 0))
        self.Iset = pd.Series(self.column(infoList, 1))
        self.Vmeasured = pd.Series(self.column(dataList, 0))
        self.Imeasured = pd.Series(self.column(dataList, 1))

        self.Vabsolute_error = self.Vset - self.Vmeasured
        self.Vpercent_error = self.Vabsolute_error / self.Vset * 100

        self.Iabsolute_error = self.Iset - self.Imeasured
        self.Ipercent_error = self.Iabsolute_error / self.Iset * 100

        self.VsetF = self.Vset.to_frame(name="Voltage Set")
        self.IsetF = self.Iset.to_frame(name="Current Set")
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

    def plotScatter(self, param1, param2, UNIT):
        self.param1 = param1
        self.param2 = param2

        if UNIT.upper() == "VOLTAGE":
            a, b = np.polyfit(self.Vset, self.Vpercent_error, 1)
            self.upper_error_limit = self.param1 * self.Vset + self.param2 * 100
            self.lower_error_limit = -self.upper_error_limit
            self.upper_error_margin = self.upper_error_limit * 0.6
            self.lower_error_margin = self.lower_error_limit * 0.6

            self.condition1 = self.lower_error_margin < self.Vpercent_error
            self.condition2 = self.upper_error_margin > self.Vpercent_error

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
            self.conditionF = self.condition.to_frame(name="Condition ?")

            self.CSV2 = pd.concat(
                [
                    self.data,
                    self.upper_error_limitF,
                    self.lower_error_limitF,
                    self.conditionF,
                ],
                axis=1,
            )
            self.CSV2.to_csv("graph.csv")

            z = self.condition.to_numpy()

            colour_condition = np.where(z == True, "k", "red")
            size_condition = np.where(z == True, 6, 12)

            plt.scatter(
                self.Vset, self.Vpercent_error, color=colour_condition, s=size_condition
            )
            plt.plot(
                self.Vset,
                self.upper_error_limit,
                label="Upper Bound",
                color="red",
                linewidth=1,
            )
            plt.plot(
                self.Vset,
                self.lower_error_limit,
                label="Lower Bound",
                color="red",
                linewidth=1,
            )
            plt.plot(
                self.Vset,
                self.upper_error_margin,
                label="Upper Margin",
                color="blue",
                linewidth=1,
            )
            plt.plot(
                self.Vset,
                self.lower_error_margin,
                label="Lower Margin",
                color="blue",
                linewidth=1,
            )

            plt.plot(
                self.Vset,
                a * self.Vset + b,
                label="Measured",
                color="green",
                linewidth=1,
            )

            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Percentage Error (%)")
            plt.show()

        elif UNIT.upper() == "CURRENT":
            a, b = np.polyfit(self.Iset, self.Ipercent_error, 1)
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
            self.conditionF = self.condition.to_frame(name="Condition ?")

            self.CSV2 = pd.concat(
                [
                    self.data,
                    self.upper_error_limitF,
                    self.lower_error_limitF,
                    self.conditionF,
                ],
                axis=1,
            )
            self.CSV2.to_csv("graph.csv")

            z = self.condition.to_numpy()

            colour_condition = np.where(z == True, "k", "red")
            size_condition = np.where(z == True, 6, 12)

            plt.scatter(
                self.Iset, self.Ipercent_error, color=colour_condition, s=size_condition
            )

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

            plt.plot(
                self.Iset,
                a * self.Iset + b,
                label="Measured",
                color="green",
                linewidth=1,
            )
            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Current (I)")
            plt.ylabel("Percentage Error (%)")
            plt.show()

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


# A = datatoGraph(infoList, main.dataList)
# A.plotScatter(0.00025, 0.0015)
