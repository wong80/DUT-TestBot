import pandas as pd
from matplotlib import pyplot as plt
import numpy as np


class datatoCSV(object):
    def __init__(self, infoList, dataList):
        self.infoList = infoList
        self.dataList = dataList

        self.sf1 = pd.Series(self.infoList)
        self.sf2 = pd.Series(self.dataList)
        self.sf3 = (self.sf1 - self.sf2) / self.sf1 * 100
        self.sf4 = self.sf1 - self.sf2

        self.df1 = self.sf1.to_frame(name="Voltage Set")
        self.df2 = self.sf2.to_frame(name="Voltage Measured")
        self.df3 = self.sf3.to_frame(name="Programmable Error (%)")
        # self.df4 = self.sf4.to_frame(name="error")
        self.df5 = pd.concat([self.df1, self.df2, self.df3], axis=1)

        self.df5.to_csv("data.csv")
        # print(self.df4.to_string)


class datatoGraph:
    def __init__(self):
        self.data = pd.read_csv("data.csv")

    def plotLine(self):
        self.data.plot(x="Voltage Set", y="Programmable Error (%)")
        plt.show()

    def plotScatter(self, param1, param2):
        self.param1 = param1
        self.param2 = param2

        x = self.data["Voltage Set"].to_numpy()
        y = self.data["Voltage Measured"].to_numpy()
        a, b = np.polyfit(x, y, 1)
        # IDEAL_M = 0.00025  # 0.25%
        # IDEAL_C = 0.0015  # 1.5mV
        upper_bound = x + (self.param1 * x + self.param2)
        lower_bound = x - (self.param1 * x - self.param2)
        self.sf6 = pd.Series(upper_bound)
        self.sf7 = pd.Series(lower_bound)
        self.df6 = self.sf6.to_frame(name="Upper Boundary")
        self.df7 = self.sf7.to_frame(name="Lower Boundary")

        self.df8 = pd.concat([self.data, self.df6, self.df7], axis=1)

        self.df8.to_csv("graph.csv")

        plt.scatter(x, y, color="red", s=2)

        plt.plot(
            x,
            upper_bound,
            label="Upper Bound",
            color="blue",
            linewidth=1,
        )
        plt.plot(
            x,
            lower_bound,
            label="Lower Bound",
            color="blue",
            linewidth=1,
        )
        plt.plot(x, a * x + b, label="results", color="red", linewidth=1)
        plt.legend(loc="upper left")
        plt.show()


A = datatoGraph()
A.plotScatter(0.00025, 0.0015)
