from openpyxl.chart import LineChart, Reference
import Data
import pandas as pd


# 1. Set up an ExcelWriter
with pd.ExcelWriter("excel_report.xlsx", engine="openpyxl") as writer:
    # 2. Export data

    df1 = pd.read_csv("data.csv")
    df2 = pd.read_csv("error.csv")
    df1.to_excel(writer, sheet_name="Data")
    df2.to_excel(writer, sheet_name="Error")
    # 3. Add a line chart
    # Point to the sheet 'historical_data', where the chart will be added
    wb = writer.book
    ws = wb["Data"]
    # Grab the maximum row number in the sheet
    max_row = ws.max_row
    # Refer to the data of close and close_200ma by the range of rows and cols on the sheet
    Vset = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=max_row)
    Vprog_error = Reference(ws, min_col=8, min_row=1, max_col=8, max_row=max_row)

    chart = LineChart()
    chart.add_data(Vprog_error, titles_from_data=True)

    chart.set_categories(Vset)
    chart.x_axis.number_format = "V"

    chart.x_axis.title = "Voltage"

    # Add title to the chart
    chart.title = "Close prices of S&P 500"
    # Refer to close_ma data, which is with index 1 within the chart, and style it
    s1 = chart.series[1]
    s1.graphicalProperties.line.dashStyle = "sysDot"
    # Add the chart to the cell of G12 on the sheet ws
    ws.add_chart(chart, "G12")
