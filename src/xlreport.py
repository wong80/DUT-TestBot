import openpyxl
import src.Data as Data
import pandas as pd


# 1. Set up an ExcelWriter
with pd.ExcelWriter("excel_report.xlsx", engine="openpyxl") as writer:
    # 2. Export data

    df1 = pd.read_csv("data.csv")
    df2 = pd.read_csv("error.csv")
    df1.to_excel(writer, sheet_name="Data")
    df2.to_excel(writer, sheet_name="Error")

    wb = writer.book
    ws = wb["Data"]
    img = openpyxl.drawing.image.Image("Chart.png")
    img.anchor = "N1"
    ws.add_image(img)
    wb.save("excel_report.xlsx")

    # # 3. Add a line chart
    # # Point to the sheet 'historical_data', where the chart will be added
    # wb = writer.book
    # ws = wb["Data"]
    # # Grab the maximum row number in the sheet
    # max_row = ws.max_row
    # # Refer to the data of close and close_200ma by the range of rows and cols on the sheet
    # Vset = Reference(ws, min_col=2, min_row=1, max_col=2, max_row=max_row)
    # Vprog_error = Reference(ws, min_col=8, min_row=1, max_col=8, max_row=max_row)

    # chart = LineChart()
    # chart.add_data(Vprog_error, titles_from_data=True)

    # chart.set_categories(Vset)
    # chart.x_axis.number_format = "V"
    # chart.x_axis.title = "Voltage"

    # # Add title to the chart
    # chart.title = "Programmable Error of Voltage"
    # # Refer to close_ma data, which is with index 1 within the chart, and style it
    # s1 = chart.series[0]
    # s1.graphicalProperties.line.dashStyle = "sysDot"
    # # Add the chart to the cell of G12 on the sheet ws
    # ws.add_chart(chart, "G12")

    # we = wb["Error"]
    # # Grab the maximum row number in the sheet
    # max_row = we.max_row
    # # Refer to the data of close and close_200ma by the range of rows and cols on the sheet
    # upper_boundary = Reference(we, min_col=12, min_row=1, max_col=12, max_row=max_row)
    # lower_boundary = Reference(we, min_col=13, min_row=1, max_col=13, max_row=max_row)
    # Vset = Reference(we, min_col=3, min_row=1, max_col=3, max_row=max_row)
    # testchart = LineChart()
    # testchart.add_data(upper_boundary, titles_from_data=True)
    # testchart.add_data(lower_boundary, titles_from_data=True)
    # testchart.add_data(Vset, titles_from_data=True)

    # testchart.set_categories(Vset)
    # testchart.x_axis.number_format = "V"
    # testchart.x_axis.title = "Voltage"

    # # Add title to the chart
    # testchart.title = "Programmable Error of Voltage"
    # # Refer to close_ma data, which is with index 1 within the chart, and style it
    # s1 = testchart.series[1]
    # s1.graphicalProperties.line.dashStyle = "sysDot"
    # # Add the chart to the cell of G12 on the sheet ws
    # we.add_chart(testchart, "G12")
