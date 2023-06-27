import PSU
import DMM
import pandas as pd


class datatoCSV(object):
    def __init__(self, infoList, dataList):
        self.infoList = infoList
        self.dataList = dataList
        self.df1 = pd.DataFrame(self.infoList, columns=["setVoltage", "Current"])
        self.df2 = pd.DataFrame(self.dataList, columns=["Measured Voltage"])
        self.df3 = pd.concat([self.df1, self.df2], axis=1)
        self.df3.to_csv("data.csv")
        print(self.df3.to_string)
