import pandas
from BerkovichTest import BerkovichTest

excel_file = "AISI316_Berkovich_studenti.xls"

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

# sheet_index: 0-35
def get_sheet(sheet_index: int):
    return pandas.read_excel(excel_file, sheet_name=sheet_index)

data = get_sheet(0)

test1 = BerkovichTest(data)
values_first = test1.displacement_load_segment[0]
values_last = test1.displacement_load_segment[-1]
print(values_first)
print(values_last)