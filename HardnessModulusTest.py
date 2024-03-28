import math
from BerkovichData import BerkovichData

class HardnessModulusTest:
    def __init__(self, data: BerkovichData, stiffness_value_percentage: float = 0.5):
        self.data = data

        # calculating corrected displacement for hardness calculation
        corrected_displacement_in_nanometers = calculate_corrected_displacement(self.data.max_displacement, self.data.elastic_displacement)
        self.corrected_displacement = convert_nanometers_to_meters(corrected_displacement_in_nanometers)
        """
        Corrected displacement (hc) [m]
        """
        
        self.area = calculate_area(self.corrected_displacement)
        """
        Area calculated from the formula: A = 24.5*(hc*hc) [m*m]
        """

        pressure = convert_millinewtons_to_newtons(self.data.pressure)
        
        self.hardness = calculate_hardness(pressure, self.area)
        """
        Hardness calculated from the formula: H = P/A [Pa]
        """

        unload_pressure = self.data.unload_segment[1]
        stiffness_index = int(stiffness_value_percentage * len(unload_pressure))
        
        maximum_unload_pressure = float(unload_pressure[0])
        middle_unload_pressure = float(unload_pressure[stiffness_index])

        unload_displacement = self.data.unload_segment[0]
        
        maximum_unload_displacement = float(unload_displacement[0])
        middle_unload_displacement = float(unload_displacement[stiffness_index])

        self.stiffness = calculate_stiffness(maximum_unload_pressure, middle_unload_pressure, maximum_unload_displacement, middle_unload_displacement)
        """
        Stiffness calculated from the data [N/m]
        """

        self.modulus = convert_pascals_to_gigapascals(calculate_modulus(self.stiffness, self.area))
        """
        Modulus calculated from the data [GPa]
        """

        self.hardness_string = f"{round(self.hardness * 1e-9, 3)} GPa"
        """
        Hardness formatted as a string for printing [GPa]
        """

        self.stiffness_string = f"{round(self.stiffness * 1e-6, 3)} MN/m"
        """
        Stiffness formatted as a string for printing [MN/m]
        """

        self.modulus_string = f"{round(self.modulus, 3)} GPa"
        """
        Modulus formatted as a string for printing [GPa]
        """

    def __str__(self):
        test_index = 36 - self.data.test_number
        output = f"Test0{test_index}\n"
        
        output += f"Hardness = {self.hardness_string}\n"
        output += f"Stiffness = {self.stiffness_string}\n"
        output += f"Modulus = {self.modulus_string}\n"

        return output

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

def calculate_modulus(stiffness: float, area: float, beta: float = 1.034):
    return (math.sqrt(math.pi) * stiffness) / (beta * 2 * math.sqrt(area))

def convert_nanometers_to_meters(nanometers: float):
    return nanometers * 1e-9

def convert_millinewtons_to_newtons(millinewtons: float):
    return millinewtons * 1e-3

def convert_pascals_to_gigapascals(pascals: float):
    return pascals * 1e-9