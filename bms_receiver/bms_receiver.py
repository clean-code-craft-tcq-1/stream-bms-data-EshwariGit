import bms_statistics_calculator as calc
import bms_input_handler as bms_input
import bms_output_handler as out


"""
 bms_receiver is made to process only user defined max_bms_inputs (15) for testing purposes in GITHUB
"""


def bms_receiver(bms_parameters_with_range, max_bms_inputs, bms_output, input_format_type):
    for iteration in range(max_bms_inputs):
        input_bms_reading = input()
        bms_input_result, formatted_bms_reading = bms_input.process_bms_input(bms_parameters_with_range,
                                                                              input_bms_reading, input_format_type)
        if bms_input_result == 'VALID_BMS_READING':
            if iteration == calc.ITERATION_NUMBER:
                calc.set_initial_bms_reading(formatted_bms_reading)
            else:
                out.print_to_console('\nDisplaying BMS Statistics')
                out.output_bms_data[bms_output](calc.calculate_bms_statistics(formatted_bms_reading))
        else:
            out.print_to_console("\nInvalid/Empty Input, Skipping BMS Statistics Calculations")
    out.print_to_console('\nBMS RECEIVING COMPLETE')


if __name__ == '__main__':
    bms_receiver({'Temperature': {'min': 0, 'max': 45}, 'StateOfCharge': {'min': 20, 'max': 80}}, 15, 'console', 'custom')
