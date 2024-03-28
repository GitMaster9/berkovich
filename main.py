import pandas
import matplotlib.pyplot as plt
from BerkovichData import BerkovichData
from HardnessModulusTest import HardnessModulusTest

excel_file = "AISI316_Berkovich_studenti.xls"

# sheet_index: 0-35
def get_sheet(sheet_index: int):
    return pandas.read_excel(excel_file, sheet_name=sheet_index)

def draw_graph(data: BerkovichData, index: int):
    plt.plot(data.displacement, data.load_on_sample)
    plt.xlabel("Displacement (nm)")
    plt.ylabel("Load (mN)")
    plt.title(f"Load-Displacement Curve Test {index}")
    plt.savefig(f"images/test_{index}_load_displacement_curve.png")
    plt.clf()

for i in range(36):
    sheet_data = get_sheet(i)
    berkovich_data = BerkovichData(sheet_data, i)

    draw_graph(berkovich_data, 36 - i)
    
    test = HardnessModulusTest(berkovich_data)

    print(test)