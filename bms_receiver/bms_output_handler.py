def display_bms_statistics(bms_statistics):
    formatted_bms_statistics = '\n'.join("{}:\t {}".format(bms_parameter, bms_value) for bms_parameter, bms_value in bms_statistics.items())
    print_to_console(formatted_bms_statistics)
    return formatted_bms_statistics


def print_to_console(console_message):
    print(console_message)


output_bms_data = {
    'console': display_bms_statistics
}
