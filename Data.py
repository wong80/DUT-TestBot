import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class datatoCSV(object):
    def __init__(self, infoList, dataList):
        self.infoList = infoList
        self.dataList = dataList

        self.Vset = pd.Series(self.infoList)
        self.Vmeasured = pd.Series(self.dataList)
        self.absolute_error = abs(self.Vset - self.Vmeasured)
        self.percent_error = self.absolute_error / self.Vset * 100

        self.VsetF = self.Vset.to_frame(name="Voltage Set")
        self.VmeasuredF = self.Vmeasured.to_frame(name="Voltage Measured")
        self.absolute_errorF = self.absolute_error.to_frame(name="Absolute Error")
        self.percent_errorF = self.percent_error.to_frame(name="Percentage Error (%)")
        self.CSV1 = pd.concat(
            [self.VsetF, self.VmeasuredF, self.absolute_errorF, self.percent_errorF],
            axis=1,
        )

        self.CSV1.to_csv("data.csv")


class datatoGraph(datatoCSV):
    def __init__(self, infoList, dataList):
        super().__init__(infoList, dataList)
        self.data = pd.read_csv("data.csv")

    def plotLine(self):
        self.data.plot(x="Voltage Set", y="Programmable Error (%)")
        plt.show()

    def plotScatter(self, param1, param2):
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
            label="Error Margin (%)",
            color="blue",
            linewidth=1,
        )

        plt.plot(
            self.Vset, a * self.Vset + b, label="results", color="green", linewidth=1
        )
        plt.legend(loc="upper left")
        plt.show()


# A = datatoGraph(infoList, main.dataList)
# A.plotScatter(0.00025, 0.0015)
