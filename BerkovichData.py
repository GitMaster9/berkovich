import pandas

class BerkovichData:
    """
    Class for getting the data from the DataFrame needed for further calculations.
    """
    def __init__(self, data_frame: pandas.DataFrame, test_number: int = 1):
        """
        Initialization function which sets all the fields.
        """
        self.data_frame = data_frame
        self.test_number = test_number

        # getting array indexes
        load_segment_index, hold_segment_index, unload_segment_index, thermal_hold_segment_index = get_segment_indexes(self.data_frame)

        # getting data from the DataFrame as lists
        displacement_all = data_frame.iloc[:, 1].to_list()
        load_on_sample_all = data_frame.iloc[:, 2].to_list()
        time_on_sample_all = data_frame.iloc[:, 3].to_list()
        
        # getting data only from the Load segment
        displacement_load_segment = displacement_all[load_segment_index:hold_segment_index]
        load_on_sample_load_segment = load_on_sample_all[load_segment_index:hold_segment_index]
        time_on_sample_load_segment = time_on_sample_all[load_segment_index:hold_segment_index]

        self.load_segment = [displacement_load_segment, load_on_sample_load_segment, time_on_sample_load_segment]
        """
        Contains displacement, load on sample and time on sample from the Load Segment of the testing.
        
        Fetch individual lists by using:
        [0] - displacement,
        [1] - load on sample,
        [2] - time on sample
        """

        # getting data only from the Hold segment
        displacement_hold_segment = displacement_all[hold_segment_index:unload_segment_index]
        load_on_sample_hold_segment = load_on_sample_all[hold_segment_index:unload_segment_index]
        time_on_sample_hold_segment = time_on_sample_all[hold_segment_index:unload_segment_index]

        self.hold_segment = [displacement_hold_segment, load_on_sample_hold_segment, time_on_sample_hold_segment]
        """
        Contains displacement, load on sample and time on sample from the Hold Segment of the testing.
        
        Fetch individual lists by using:
        [0] - displacement,
        [1] - load on sample,
        [2] - time on sample
        """

        # getting data only from the Unload segment
        displacement_unload_segment = displacement_all[unload_segment_index:thermal_hold_segment_index]
        load_on_sample_unload_segment = load_on_sample_all[unload_segment_index:thermal_hold_segment_index]
        time_on_sample_unload_segment = time_on_sample_all[unload_segment_index:thermal_hold_segment_index]

        self.unload_segment = [displacement_unload_segment, load_on_sample_unload_segment, time_on_sample_unload_segment]
        """
        Contains displacement, load on sample and time on sample from the Unload From Peak Segment of the testing.
        
        Fetch individual lists by using:
        [0] - displacement,
        [1] - load on sample,
        [2] - time on sample
        """

        # getting data only from the Thermal Drift Hold segment
        displacement_thermal_hold_segment = displacement_all[thermal_hold_segment_index:-1]
        load_on_sample_thermal_hold_segment = load_on_sample_all[thermal_hold_segment_index:-1]
        time_on_sample_thermal_hold_segment = time_on_sample_all[thermal_hold_segment_index:-1]

        self.thermal_drift_hold_segment = [displacement_thermal_hold_segment, load_on_sample_thermal_hold_segment, time_on_sample_thermal_hold_segment]
        """
        Contains displacement, load on sample and time on sample from the Thermal Drift Hold Segment of the testing.
        
        Fetch individual lists by using:
        [0] - displacement,
        [1] - load on sample,
        [2] - time on sample
        """

        # getting data from the Hold segment
        self.stiffness_table = float(data_frame.iloc[:, 4].to_list()[unload_segment_index])
        """
        Stiffness generated by the indenter software in the Excel table [N/m]
        """

        self.modulus_table = float(data_frame.iloc[:, 5].to_list()[unload_segment_index])
        """
        Modulus generated by the indenter software in the Excel table [GPa]
        """

        self.hardness_table = float(data_frame.iloc[:, 6].to_list()[unload_segment_index])
        """
        Hardness generated by the indenter software in the Excel table [GPa]
        """

        # getting maximum pressure value for further calculations
        self.pressure = float(load_on_sample_load_segment[-1])
        """
        Maximum (theoretical) pressure used in the test (last value in the Load segment) [mN]
        """

        # getting displacement values for further calculations
        self.max_displacement = float(displacement_hold_segment[-1])
        """
        Maximum (theoretical) displacement used in the test (last value in the Hold segment) [nm]
        """

        # used to calculate elastic displacement
        unload_displacement = float(displacement_unload_segment[-1])
        
        self.elastic_displacement = self.max_displacement - unload_displacement
        """
        Elastic displacement (h_el = h_max - h_pl) [nm]
        """

def get_segment_indexes(data_frame: pandas.DataFrame):
    """
    A function that reads array indexes for all segments written in the Excel file (Load, Hold, Unload From Peak and Thermal Drift Hold).

    Returns 4 segment indexes as a tuple.
    """
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