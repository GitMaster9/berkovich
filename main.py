import pandas
import matplotlib.pyplot as plt
from BerkovichTest import BerkovichTest

excel_file = "AISI316_Berkovich_studenti.xls"

def get_height_in_meters(height_in_nanometers: float):
    return height_in_nanometers * 1e-9

def get_pressure_in_newtons(pressure_in_millinewtons: float):
    return pressure_in_millinewtons * 1e-3

def calculate_height(max_height: float, elastic_height: float):
    return max_height - (elastic_height / 2)

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

# sheet_index: 0-35
def get_sheet(sheet_index: int):
    return pandas.read_excel(excel_file, sheet_name=sheet_index)

def draw_graph(test: BerkovichTest, index: int):
    displacement = test.displacement_load_segment + test.displacement_hold_segment + test.displacement_unload_segment + test.displacement_thermal_hold_segment
    load = test.load_on_sample_load_segment + test.load_on_sample_hold_segment + test.load_on_sample_unload_segment + test.load_on_sample_thermal_hold_segment

    plt.plot(displacement, load)
    plt.xlabel("Displacement (nm)")
    plt.ylabel("Load (mN)")
    plt.title(f"Load-Displacement Curve Test {index + 1}")
    plt.savefig(f"images/test_{index + 1}_load_displacement_curve.png")
    plt.clf()

# Main
def main():
    data = []

    # for i from 35 to 0
    for i in range(35, -1, -1):
        data.append(get_sheet(i))

    for i in range(36):
        test = BerkovichTest(data[i])

        draw_graph(test, i)
        
        print("Sheet " + str(i + 1))
        print("Max height: " + str(test.max_height))
        print("Unload height: " + str(test.unload_height))
        print("Elastic height: " + str(test.elastic_height))
        print("Pressure: " + str(test.pressure))
        print("Stiffness: " + str(test.stiffness))
        print("Modulus: " + str(test.modulus))
        print("Hardness (table): " + str(test.hardness_table))
        print()

main()

# data = get_sheet(0)
# test1 = BerkovichTest(data)

# # draw a plot of the load-displacement curve
# # plt.plot(test1.displacement_load_segment, test1.load_on_sample_load_segment)
# # plt.plot(test1.displacement_hold_segment, test1.load_on_sample_hold_segment)
# # plt.plot(test1.displacement_unload_segment, test1.load_on_sample_unload_segment)
# # plt.plot(test1.displacement_thermal_hold_segment, test1.load_on_sample_thermal_hold_segment)
# displacement = test1.displacement_load_segment + test1.displacement_hold_segment + test1.displacement_unload_segment + test1.displacement_thermal_hold_segment
# load = test1.load_on_sample_load_segment + test1.load_on_sample_hold_segment + test1.load_on_sample_unload_segment + test1.load_on_sample_thermal_hold_segment
# plt.plot(displacement, load)
# plt.xlabel("Displacement (nm)")
# plt.ylabel("Load (mN)")
# plt.title("Load-Displacement Curve")
# plt.show()

# max_height = test1.max_height
# unload_height = test1.unload_height
# elastic_height = test1.elastic_height
# print("max height in nanometers: " + str(max_height))
# print("unload height in nanometers: " + str(unload_height))
# print("elastic height in nanometers: " + str(elastic_height))
# print()

# pressure = test1.pressure
# print("pressure in millinewtons: " + str(pressure))
# pressure = get_pressure_in_newtons(pressure)
# print("pressure in newtons: " + str(pressure))
# print()

# hc = calculate_height(max_height, elastic_height)
# print("hc in nanometers: " + str(hc))
# hc = get_height_in_meters(hc)
# print("hc in meters: " + str(hc))
# print()

# area = calculate_area(hc)
# print("area: " + str(area))
# hardness = calculate_hardness(pressure, area)
# hardness = f'{hardness:e}' # scientific number format
# print("hardness in pascals: " + str(hardness))
# print()

# stiffness = test1.stiffness
# modulus = test1.modulus
# hardness_table = test1.hardness_table
# print("stiffness in newton/meter: " + str(stiffness))
# print("modulus in gigapascals: " + str(modulus))
# print("hardness (table) in gigapascals: " + str(hardness_table))
