import pandas

class BerkovichTest:
    def __init__(self, data_frame: pandas.DataFrame):
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
    return displacement, load_on_sample, time_on_sample