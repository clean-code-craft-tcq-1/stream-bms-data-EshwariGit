import bms_output_handler as out


def is_input_empty(input_bms_reading):
    if len(input_bms_reading) != 0:
        return 'BMS_INPUT_NOT_EMPTY'
    else:
        return 'BMS_INPUT_EMPTY'


def is_input_valid(bms_parameters_with_range, formatted_bms_reading):
    result = None
    for bms_parameter, bms_value in formatted_bms_reading.items():
        if (bms_value > bms_parameters_with_range[bms_parameter]['min']) and \
                (bms_value < bms_parameters_with_range[bms_parameter]['max']):
            result = 'VALID_BMS_READING'
        else:
            result = 'INVALID_BMS_READING'
            break
    return result


def format_custom_bms_input(input_bms_reading):
    try:
        formatted_bms_readings = dict((temperature.strip(), float(SOC.strip())) for temperature, SOC in
                                      (member.split(" value is ") for member in input_bms_reading.split("and")))
        return formatted_bms_readings
    except (TypeError, ValueError, AttributeError) as e:
        out.print_to_console(e)


format_bms_input = {
    'custom': format_custom_bms_input
}


def process_bms_input(bms_parameters_with_range, input_bms_reading, format_type):
    formatted_bms_reading = None
    if is_input_empty(input_bms_reading) == 'BMS_INPUT_NOT_EMPTY':
        formatted_bms_reading = format_bms_input[format_type](str(input_bms_reading))
        result = is_input_valid(bms_parameters_with_range, formatted_bms_reading)
    else:
        result = 'BMS_INPUT_EMPTY'
    return result, formatted_bms_reading

