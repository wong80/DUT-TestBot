import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import json


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

        self.CSV1.to_csv("csv/data.csv")

    def column(self, matrix, i):
        return [row[i] for row in matrix]


class datatoGraph(datatoCSV):
    def __init__(self, infoList, dataList):
        super().__init__(infoList, dataList)
        self.data = pd.read_csv("csv/data.csv")

    def errorBoundary(self, param1, param2, UNIT, x, Vpercent_error):
        self.param1 = param1
        self.param2 = param2

        my_dict = {"Name": "Voltage", "Gain": [param1], "Offset": [param2]}

        df = pd.DataFrame.from_dict(my_dict)

        df.to_csv("csv/param.csv", index=False)

        if UNIT.upper() == "VOLTAGE":
            # a, b = np.polyfit(self.Vset, self.Vpercent_error, 1)
            upper_error_limit = self.param1 * x + self.param2 * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit
            # upper_error_margin = upper_error_limit * 0.6
            # lower_error_margin = lower_error_limit * 0.6

            condition1 = upper_error_limit < Vpercent_error
            condition2 = lower_error_limit > Vpercent_error

            self.condition = condition1 | condition2
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
            self.colour_condition = np.where(self.z == False, "black", "red")
            self.size_condition = np.where(self.z == False, 6, 12)
            self.alpha_condition = np.where(self.z == False, 0, 1)

            # plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Voltage (V)")
            plt.ylabel("Percentage Error (%)")
            # plt.show()

        elif UNIT.upper() == "CURRENT":
            # a, b = np.polyfit(self.Vset, self.Vpercent_error, 1)
            upper_error_limit = self.param1 * x + self.param2 * 100
            lower_error_limit = -upper_error_limit
            self.upper_error_limit = upper_error_limit
            self.lower_error_limit = lower_error_limit
            # upper_error_margin = upper_error_limit * 0.6
            # lower_error_margin = lower_error_limit * 0.6

            condition1 = upper_error_limit < Vpercent_error
            condition2 = lower_error_limit > Vpercent_error

            self.condition = condition1 | condition2
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
            self.colour_condition = np.where(self.z == False, "white", "red")
            self.size_condition = np.where(self.z == False, 0, 12)
            self.alpha_condition = np.where(self.z == False, 0, 1)

            plt.legend(loc="upper left")
            plt.title(UNIT)
            plt.xlabel("Current (A)")
            plt.ylabel("Percentage Error (%)")

    def scatterCompare(self):
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

            VsetS = Vset.squeeze()
            Vpercent_errorS = Vpercent_error.squeeze()

            self.errorBoundary(0.00025, 0.0015, "Voltage", VsetS, Vpercent_errorS)

            # a, b = np.polyfit(VsetS, Vpercent_errorS, 1)

            upper_error_limitC = pd.concat([upper_error_limitC, self.upper_error_limit])
            lower_error_limitC = pd.concat([lower_error_limitC, self.lower_error_limit])
            conditionC = pd.concat([conditionC, self.condition])

            plt.scatter(
                Vset,
                Vpercent_errorS,
                color=self.colour_condition,
                s=self.size_condition,
                alpha=self.alpha_condition,
            )

            plt.plot(
                Vset,
                Vpercent_errorS,
                label="Current = " + str(Iset.iloc[0]["Current Set"]),
            )

            # plt.plot(Vset, a * Vset + b)

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
                conditionF,
            ],
            axis=1,
        )

        self.CSV2.to_csv("csv/error.csv", index=False)

        plt.legend(loc="lower left")
        plt.savefig("images/Chart.png")
        # plt.show()


class instrumentData:
    def __init__(self, *args):
        instrumentIDN = []
        instrumentVersion = []

        for x in args:
            instrumentIDN.append(x.dmm.query("*IDN?"))
            instrumentVersion.append(x.dmm.query("SYST:VERS?"))

        df1 = pd.DataFrame(instrumentIDN, columns=["Instruments Used: "])
        df2 = pd.DataFrame(instrumentVersion, columns=["SCPI Version"])

        instrument = pd.concat([df1, df2], axis=1)

        instrument.to_csv("csv/instrumentData.csv", index=False)
