ITERATION_NUMBER = 0
SMA_WINDOW = 5

temp_list = []
soc_list = []

saved_bms_readings = {'Temperature': temp_list,
                      'StateOfCharge': soc_list}

bms_statistics = {'Temperature': {'min': 0, 'max': 0, 'sma': 0},
                  'StateOfCharge': {'min': 0, 'max': 0, 'sma': 0}}


def compute_max_value(saved_max_value, bms_reading):
    return max(saved_max_value, bms_reading)


def compute_min_value(saved_min_value, bms_reading):
    return min(saved_min_value, bms_reading)


def compute_simple_moving_average(bms_parameter):
    simple_moving_average = sum(saved_bms_readings[bms_parameter]) / SMA_WINDOW
    return simple_moving_average


def store_bms_reading(bms_parameter, bms_value):
    saved_bms_readings[bms_parameter].append(bms_value)


def set_initial_bms_reading(formatted_bms_reading):
    for bms_parameter, bms_value in formatted_bms_reading.items():
        bms_statistics[bms_parameter]['min'] = bms_value
        bms_statistics[bms_parameter]['max'] = bms_value
        store_bms_reading(bms_parameter, bms_value)


def update_bms_reading(bms_parameter, bms_value):
    bms_statistics[bms_parameter]['max'] = compute_max_value(bms_statistics[bms_parameter]['max'], bms_value)
    bms_statistics[bms_parameter]['min'] = compute_min_value(bms_statistics[bms_parameter]['min'], bms_value)
    bms_statistics[bms_parameter]['sma'] = compute_simple_moving_average(bms_parameter)


def calculate_bms_statistics(formatted_bms_reading):
    for bms_parameter, bms_value in formatted_bms_reading.items():
        if len(saved_bms_readings[bms_parameter]) == SMA_WINDOW:
            saved_bms_readings[bms_parameter].pop(0)
        store_bms_reading(bms_parameter, bms_value)
        update_bms_reading(bms_parameter, bms_value)
    return bms_statistics
