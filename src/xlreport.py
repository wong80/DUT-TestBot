import openpyxl
from openpyxl.styles import Alignment, PatternFill, Font
from openpyxl.formatting.rule import FormulaRule
import pandas as pd
import datetime


red_font = Font(size=14, bold=True, color="ffffff")
red_fill = PatternFill(start_color="ffcccc", end_color="ffcccc", fill_type="solid")
green_font = Font(size=14, bold=True, color="013220")
green_fill = PatternFill(
    start_color="FFAAFF00", end_color="FFAAFF00", fill_type="solid"
)


def adjustcolumnWidth(worksheet, value):
    for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
        worksheet.column_dimensions[x].width = value


def alignCell(worksheet, row_number, column_number, style):
    currentCell = worksheet.cell(row=row_number, column=column_number)
    currentCell.alignment = Alignment(horizontal=style)


with pd.ExcelWriter("excel_report.xlsx", engine="openpyxl") as writer:
    df1 = pd.read_csv("csv/error.csv", index_col=False)
    df2 = pd.read_csv(
        "csv/instrumentData.csv",
        index_col=False,
    )

    df3 = pd.read_csv("csv/param.csv", index_col=False)

    df1.to_excel(writer, sheet_name="Data", index=False, startrow=7, startcol=1)
    df2.to_excel(writer, sheet_name="Data", index=False)
    df3.to_excel(writer, sheet_name="Data", index=False, startcol=5)

    wb = writer.book
    ws = wb["Data"]
    cellref = "L9:L" + str(ws.max_row)

    ws.conditional_formatting.add(
        cellref,
        FormulaRule(
            formula=[f'NOT(ISERROR(SEARCH("PASS",{cellref})))'],
            stopIfTrue=True,
            fill=green_fill,
            font=green_font,
        ),
    )
    ws.conditional_formatting.add(
        cellref,
        FormulaRule(
            formula=[f'NOT(ISERROR(SEARCH("FAIL",{cellref})))'],
            stopIfTrue=True,
            fill=red_fill,
            font=red_font,
        ),
    )

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
