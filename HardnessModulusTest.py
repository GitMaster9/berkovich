import math
from BerkovichData import BerkovichData

class HardnessModulusTest:
    def __init__(self, data: BerkovichData, stiffness_value_percentage: float = 0.5):

        # calculating corrected displacement for hardness calculation
        corrected_displacement_in_nanometers = calculate_corrected_displacement(data.max_displacement, data.elastic_displacement)
        self.corrected_displacement = convert_nanometers_to_meters(corrected_displacement_in_nanometers)
        
        self.area = calculate_area(self.corrected_displacement)

        pressure = convert_millinewtons_to_newtons(data.pressure)
        
        self.hardness = calculate_hardness(pressure, self.area)

        unload_pressure = data.unload_segment[1]
        stiffness_index = int(stiffness_value_percentage * len(unload_pressure))
        
        maximum_unload_pressure = float(unload_pressure[0])
        middle_unload_pressure = float(unload_pressure[stiffness_index])

        unload_displacement = data.unload_segment[0]
        
        maximum_unload_displacement = float(unload_displacement[0])
        middle_unload_displacement = float(unload_displacement[stiffness_index])

        self.stiffness = calculate_stiffness(maximum_unload_pressure, middle_unload_pressure, maximum_unload_displacement, middle_unload_displacement)

        self.elasticity = convert_pascals_to_gigapascals(calculate_elasticity(self.stiffness, self.area))

def calculate_corrected_displacement(max_height: float, elastic_height: float):
    return max_height - (elastic_height / 2)

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_stiffness(maximum_unload_pressure: float, middle_unload_pressure: float, maximum_unload_displacement: float, middle_unload_displacement: float):
    adjusted_pressure_in_millinewtons = maximum_unload_pressure - middle_unload_pressure
    adjusted_displacement_in_nanometers = maximum_unload_displacement - middle_unload_displacement

    adjusted_pressure = convert_millinewtons_to_newtons(adjusted_pressure_in_millinewtons)
    adjusted_displacement = convert_nanometers_to_meters(adjusted_displacement_in_nanometers)

    return adjusted_pressure / adjusted_displacement

def calculate_elasticity(stiffness: float, area: float, beta: float = 1.034):
    return (math.sqrt(math.pi) * stiffness) / (beta * 2 * math.sqrt(area))

def convert_nanometers_to_meters(nanometers: float):
    return nanometers * 1e-9

def convert_millinewtons_to_newtons(millinewtons: float):
    return millinewtons * 1e-3

def convert_pascals_to_gigapascals(pascals: float):
    return pascals * 1e-9