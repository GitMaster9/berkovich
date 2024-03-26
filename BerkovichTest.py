import pandas

class BerkovichTest:
    def __init__(self, data_frame: pandas.DataFrame, index: int):
        self.index = index
        all_values = get_all_values_from_sheet(data_frame)
        
        displacement = all_values[0]
        self.displacement_load_segment = displacement[0]
        self.displacement_hold_segment = displacement[1]
        self.displacement_unload_segment = displacement[2]
        self.displacement_thermal_hold_segment = displacement[3]

        load_on_sample = all_values[1]
        self.load_on_sample_load_segment = load_on_sample[0]
        self.load_on_sample_hold_segment = load_on_sample[1]
        self.load_on_sample_unload_segment = load_on_sample[2]
        self.load_on_sample_thermal_hold_segment = load_on_sample[3]

        time_on_sample = all_values[2]
        self.time_on_sample_load_segment = time_on_sample[0]
        self.time_on_sample_hold_segment = time_on_sample[1]
        self.time_on_sample_unload_segment = time_on_sample[2]
        self.time_on_sample_thermal_hold_segment = time_on_sample[3]

        self.max_height = all_values[3]
        self.unload_height = all_values[4]
        self.elastic_height = all_values[5]
        self.pressure = all_values[6]

        self.stiffness = all_values[7]
        self.modulus = all_values[8]
        self.hardness_table = all_values[9]

        self.h_c = calculate_height(nm_to_m(self.max_height), nm_to_m(self.elastic_height))
        self.area = calculate_area(self.h_c)
        self.hardness = Pa_to_GPA(calculate_hardness(mN_to_N(self.pressure), self.area))

    def __str__(self):
        test_index = 36 - self.index
        output = f"Test{test_index}\n"
        output += f"h_max = {round(self.max_height, 3)} nm\n"
        output += f"h_unload = {round(self.unload_height, 3)} nm\n"
        output += f"h_el = {round(self.elastic_height, 3)} nm\n"
        output += f"pressure = {round(self.pressure, 3)} mN\n"
        
        #output += f"h_c = {self.h_c} m\n"
        #output += f"area = {self.area} m2\n"
        output += f"hardness = {round(self.hardness, 3)} GPa\n"

        return output

def get_segment_indexes(data_frame: pandas.DataFrame):
    column_segment = data_frame.iloc[:, 0].to_list()
    step_1 = 0
    step_2 = 0
    step_3 = 0
    step_4 = 0
    for i in range(len(column_segment)):
        if column_segment[i] == "Load Segment Type":
            step_1 = i
            continue

        if column_segment[i] == "Hold Segment Type":
            step_2 = i
            continue

        if column_segment[i] == "Unload From Peak Segment Type":
            step_3 = i
            continue

        if column_segment[i] == "Thermal Drift Hold Segment Type":
            step_4 = i
            continue

    return step_1, step_2, step_3, step_4

def get_list_values_from_indexes(column_data: list, load_segment_index: int, hold_segment_index: int, unload_segment_index: int, thermal_hold_segment_index: int):
    load_segment = column_data[load_segment_index:hold_segment_index]
    hold_segment = column_data[hold_segment_index:unload_segment_index]
    unload_segment = column_data[unload_segment_index:thermal_hold_segment_index]
    thermal_hold_segment = column_data[thermal_hold_segment_index:-1]

    return load_segment, hold_segment, unload_segment, thermal_hold_segment

def get_column_value_by_row_index(data_frame: pandas.DataFrame, column_index: int, row_index: int):
    data = data_frame.iloc[:, column_index].to_list()
    return data[row_index]

def get_column_values(data_frame: pandas.DataFrame, column_index: int, load_segment_index: int, hold_segment_index: int, unload_segment_index: int, thermal_hold_segment_index: int):
    data = data_frame.iloc[:, column_index].to_list()
    load_segment, hold_segment, unload_segment, thermal_hold_segment = get_list_values_from_indexes(data, load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index)
    return load_segment, hold_segment, unload_segment, thermal_hold_segment

def get_all_values_from_sheet(data_frame: pandas.DataFrame):
    load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index = get_segment_indexes(data_frame)
    
    displacement1, displacement2, displacement3, displacement4 = get_column_values(data_frame, 1, load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index)
    load_on_sample1, load_on_sample2, load_on_sample3, load_on_sample4 = get_column_values(data_frame, 2, load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index)
    time_on_sample1, time_on_sample2, time_on_sample3, time_on_sample4 = get_column_values(data_frame, 3, load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index)

    displacement = [displacement1, displacement2, displacement3, displacement4]
    load_on_sample = [load_on_sample1, load_on_sample2, load_on_sample3, load_on_sample4]
    time_on_sample = [time_on_sample1, time_on_sample2, time_on_sample3, time_on_sample4]

    max_height = get_column_value_by_row_index(data_frame, 1, unload_segment_index - 1)
    unload_height = displacement4[-1]
    elastic_height = max_height - unload_height
    pressure = load_on_sample3[-1]

    stiffness = get_column_value_by_row_index(data_frame, 4, unload_segment_index)
    modulus = get_column_value_by_row_index(data_frame, 5, unload_segment_index)
    hardness = get_column_value_by_row_index(data_frame, 6, unload_segment_index)

    return displacement, load_on_sample, time_on_sample, max_height, unload_height, elastic_height, pressure, stiffness, modulus, hardness

def calculate_height(max_height: float, elastic_height: float):
    return max_height - (elastic_height / 2)

def calculate_hardness(pressure: float, area: float):
    return pressure / area

def calculate_area(hc: float):
    return 24.5 * (hc ** 2)

def nm_to_m(nanometers: float):
    return nanometers * 1e-9

def mN_to_N(millinewtons: float):
    return millinewtons * 1e-3

def Pa_to_GPA(pascals: float):
    return pascals * 1e-9
