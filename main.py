import pandas
from BerkovichTest import BerkovichTest

excel_file = "AISI316_Berkovich_studenti.xls"

def get_height_in_meters(height_in_nanometers: float):
    return height_in_nanometers * 1e-9

def get_pressure_in_newtons(pressure_in_millinewtons: float):
    return pressure_in_millinewtons * 1e-3

def calculate_height(displacement: float, elastic_height: float = 0.5):
    hc = displacement - (displacement * elastic_height) / 2
    return hc

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

# sheet_index: 0-35
def get_sheet(sheet_index: int):
    return pandas.read_excel(excel_file, sheet_name=sheet_index)

data = get_sheet(0)
test1 = BerkovichTest(data)

displacement = test1.displacement_load_segment[-1] # 2996.05952193434 nm
pressure = test1.load_on_sample_load_segment[-1] # 551.591314351262 mN

hc = calculate_height(displacement)
print("hc in nanometers: " + str(hc))
hc = get_height_in_meters(hc)
print("hc in meters: " + str(hc))

print("pressure in millinewtons: " + str(pressure))
pressure = get_pressure_in_newtons(pressure)
print("pressure in newtons: " + str(pressure))

area = calculate_area(hc)
print("area: " + str(area))
hardness = calculate_hardness(pressure, area)
hardness = f'{hardness:e}' # scientific number format
print("hardness in pascals: " + str(hardness))