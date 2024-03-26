import pandas
import matplotlib.pyplot as plt
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

def draw_graph(test: BerkovichTest, index: int):
    displacement = test.displacement_load_segment + test.displacement_hold_segment + test.displacement_unload_segment + test.displacement_thermal_hold_segment
    load = test.load_on_sample_load_segment + test.load_on_sample_hold_segment + test.load_on_sample_unload_segment + test.load_on_sample_thermal_hold_segment

    plt.plot(displacement, load)
    plt.xlabel("Displacement (nm)")
    plt.ylabel("Load (mN)")
    plt.title(f"Load-Displacement Curve Test {index}")
    plt.savefig(f"images/test_{index}_load_displacement_curve.png")
    plt.clf()

# Main
def main():
    data = []

    # for i from 35 to 0
    for i in range(36):
        data.append(get_sheet(i))

    for i in range(36):
        test = BerkovichTest(data[i], i)

        draw_graph(test, 36 - i)
        
        print(test)

main()
