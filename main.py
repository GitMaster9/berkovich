import pandas
from BerkovichTest import BerkovichTest

excel_file = "AISI316_Berkovich_studenti.xls"

def get_height_in_meters(height_in_nanometers: float):
    return height_in_nanometers * 1e-9

def get_pressure_in_newtons(pressure_in_millinewtons: float):
    return pressure_in_millinewtons * 1e-3

def get_hardness_in_gigapascals(hardness_in_pascals: float):
    return hardness_in_pascals * 1e-9

def calculate_height(max_height: float, elastic_height: float):
    return max_height - (elastic_height / 2)

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

# sheet_index: 0-35
def get_sheet(sheet_index: int):
    return pandas.read_excel(excel_file, sheet_name=sheet_index)

test_index = 0
data = get_sheet(test_index)
test1 = BerkovichTest(data, test_index)

print(test1)