import PSU
import pandas as pd


class datatoCSV(object):
    df = pd.DataFrame(PSU.dataList, columns=["Voltage", "Current"])
    df.to_csv("data.csv")
