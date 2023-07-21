import openpyxl
from openpyxl.styles import Alignment, PatternFill, Font
from openpyxl.formatting.rule import FormulaRule
import pandas as pd
import datetime


class xlreport(object):
    def __init__(self):
        self.red_font = Font(size=14, bold=True, color="ffffff")
        self.red_fill = PatternFill(
            start_color="ffcccc", end_color="ffcccc", fill_type="solid"
        )
        self.green_font = Font(size=14, bold=True, color="013220")
        self.green_fill = PatternFill(
            start_color="FFAAFF00", end_color="FFAAFF00", fill_type="solid"
        )
        self.path = (
            r"C:\Users\zhiywong\OneDrive - Keysight Technologies\Documents\GitHub\PyVisa\Excel Files\\"
            + datetime.datetime.now().strftime("%Y-%m-%d--%H-%M-%S")
            + ".xlsx"
        )

        print(self.path)

    def adjustcolumnWidth(self, worksheet, value):
        for x in ["A", "B", "C", "D", "E", "F", "G", "H", "I"]:
            worksheet.column_dimensions[x].width = value

    def alignCell(self, worksheet, row_number, column_number, style):
        currentCell = worksheet.cell(row=row_number, column=column_number)
        currentCell.alignment = Alignment(horizontal=style)

    def run(self):
        with pd.ExcelWriter(self.path, engine="openpyxl") as writer:
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
                    fill=self.green_fill,
                    font=self.green_font,
                ),
            )
            ws.conditional_formatting.add(
                cellref,
                FormulaRule(
                    formula=[f'NOT(ISERROR(SEARCH("FAIL",{cellref})))'],
                    stopIfTrue=True,
                    fill=self.red_fill,
                    font=self.red_font,
                ),
            )

            self.adjustcolumnWidth(ws, 20)
            self.adjustcolumnWidth(ws, 20)
            self.alignCell(ws, 1, 1, "left")
            self.alignCell(ws, 2, 1, "left")
            self.alignCell(ws, 3, 1, "left")
            self.alignCell(ws, 4, 1, "left")

            ws.cell(row=7, column=2).value = "Time Generated: "
            ws.cell(row=7, column=3).value = datetime.datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            img = openpyxl.drawing.image.Image("images/Chart.png")
            img.anchor = "R1"
            ws.add_image(img)

            wb.save(self.path)
