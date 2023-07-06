import openpyxl
from openpyxl.styles import Alignment
import pandas as pd
import datetime
from Data import datatoGraph
import json


def adjustcolumnWidth(worksheet, value):
    for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        worksheet.column_dimensions[x].width = value


def alignCell(worksheet, row_number, column_number, style):
    currentCell = worksheet.cell(row=row_number, column=column_number)
    currentCell.alignment = Alignment(horizontal=style)


with pd.ExcelWriter("excel_report.xlsx", engine="openpyxl") as writer:
    df1 = pd.read_csv("csv/error.csv", index_col=[1])
    df2 = pd.read_csv("csv/instrumentData.csv", index_col=[1])

    df1.to_excel(writer, sheet_name="Data", startrow=7, startcol=1)
    df2.to_excel(writer, sheet_name="Data")
    wb = writer.book
    ws = wb["Data"]

    df = pd.read_json("param.json")
    df = df.reset_index(drop=True)
    df.to_excel(writer, sheet_name="Data", startcol=5)

    adjustcolumnWidth(ws, 20)
    adjustcolumnWidth(ws, 20)
    alignCell(ws, 1, 1, "left")
    alignCell(ws, 2, 1, "left")
    alignCell(ws, 3, 1, "left")
    alignCell(ws, 4, 1, "left")

    ws.cell(row=7, column=2).value = "Time Generated: "
    ws.cell(row=7, column=3).value = datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    img = openpyxl.drawing.image.Image("images/Chart.png")
    img.anchor = "R1"
    ws.add_image(img)
    wb.save("excel_report.xlsx")
