import unittest
from io import StringIO
from mock import patch
import bms_statistics_calculator as calc
import bms_input_handler as bms_input
import bms_output_handler as out
import bms_receiver


class BMSReceiverTest(unittest.TestCase):
    def setUp(self):
        temp_list = []
        soc_list = []
        calc.saved_bms_readings = {'Temperature': temp_list,
                                   'StateOfCharge': soc_list}
        calc.bms_statistics = {'Temperature': {'min': 0, 'max': 0, 'sma': 0},
                               'StateOfCharge': {'min': 0, 'max': 0, 'sma': 0}}

    def tearDown(self):
        temp_list = []
        soc_list = []
        calc.saved_bms_readings = {'Temperature': temp_list,
                                   'StateOfCharge': soc_list}
        calc.bms_statistics = {'Temperature': {'min': 0, 'max': 0, 'sma': 0},
                               'StateOfCharge': {'min': 0, 'max': 0, 'sma': 0}}

    bms_parameters_with_range = {'Temperature': {'min': 0, 'max': 45}, 'StateOfCharge': {'min': 20, 'max': 80}}

    """
    ******************************************************
                    File: bms_input_handler
    ******************************************************
    """

    def test_is_input_empty(self):
        bms_input_readings = ['', 'Temperature value is 24.000000 and StateOfCharge value is 90.000000',
                              'Temperature value is 25.000000']
        expected_bms_outputs = ["BMS_INPUT_EMPTY", "BMS_INPUT_NOT_EMPTY", "BMS_INPUT_NOT_EMPTY"]

        for i in range(3):
            self.assertEqual(bms_input.is_input_empty(bms_input_readings[i]), expected_bms_outputs[i])

    def test_is_input_valid(self):
        bms_invalid_inputs = [{'Temperature': -20.0, 'StateOfCharge': 71.0}, {'Temperature': 30.0, 'StateOfCharge': 100.0},
                              {'Temperature': 10.0, 'StateOfCharge': 10.0}, {'Temperature': 70.0, 'StateOfCharge': 25.0},
                              {'Temperature': 0, 'StateOfCharge': 20}, {'Temperature': -50.0, 'StateOfCharge': -21.0},
                              {'Temperature': 45.0, 'StateOfCharge': 80.0}]
        bms_valid_input = {'Temperature': 20.0, 'StateOfCharge': 61.0}

        for i in range(6):
            self.assertEqual(bms_input.is_input_valid(self.bms_parameters_with_range, bms_invalid_inputs[i]), 'INVALID_BMS_READING')
        self.assertEqual(bms_input.is_input_valid(self.bms_parameters_with_range, bms_valid_input), 'VALID_BMS_READING')

    def test_format_custom_bms_input_to_rx_bms_data(self):
        input_bms_readings = ['Temperature value is 24.000000 and StateOfCharge value is 88.000000',
                              'Temperature value is 40.000000', 'StateOfCharge value is 72.000000''']
        expected_bms_outputs = [{'Temperature': 24.0, 'StateOfCharge': 88.0}, {'Temperature': 40.0}, {'StateOfCharge': 72.0}]

        for i in range(3):
            self.assertEqual(bms_input.format_custom_bms_input(input_bms_readings[i]), expected_bms_outputs[i])

    def test_process_bms_input(self):
        bms_input_readings = ['Temperature value is 34.000000 and StateOfCharge value is 90.000000', '']
        expected_bms_outputs = [('INVALID_BMS_READING', {'Temperature': 34.0, 'StateOfCharge': 90.0}),
                                ('BMS_INPUT_EMPTY', None)]

        for i in range(2):
            self.assertEqual(bms_input.process_bms_input(self.bms_parameters_with_range, bms_input_readings[i],
                                                         'custom'), expected_bms_outputs[i])

    """
     *******************************************************
                    File: bms_output_handler
     *******************************************************
    """

    def test_print_to_console_using_mock_stdout(self):
        bms_statistics = "Temperature:	 {'min': 12.0, 'max': 31.0, 'sma': 20.4}	" \
                           "StateOfCharge:	 {'min': 56.0, 'max': 78.0, 'sma': 67.4}"
        expected_bms_statistics = "Temperature:	 {'min': 12.0, 'max': 31.0, 'sma': 20.4}	" \
                                  "StateOfCharge:	 {'min': 56.0, 'max': 78.0, 'sma': 67.4}"

        with patch('sys.stdout', new=StringIO()) as fake_print:
            out.print_to_console(bms_statistics)
        self.assertEqual(fake_print.getvalue().strip(), expected_bms_statistics)

    def test_display_bms_statistics_using_mock_console_print(self):
        bms_statistics = {'Temperature': {'min': 12.0, 'max': 31.0, 'sma': 20.4},
                          'StateOfCharge': {'min': 56.0, 'max': 78.0, 'sma': 67.4}}
        expected_bms_statistics = "Temperature:	 {'min': 12.0, 'max': 31.0, 'sma': 20.4}\nStateOfCharge:	 {'min': 56.0, 'max': 78.0, 'sma': 67.4}"

        with patch('bms_output_handler.print_to_console') as fake_print:
            formatted_bms_data = out.display_bms_statistics(bms_statistics)
            fake_print.assert_called_once()
        self.assertEqual(formatted_bms_data, expected_bms_statistics)


    """
     *******************************************************
                    File: bms_statistics_calculator
     *******************************************************
    """

    def test_calculate_bms_statistics(self):
        bms_readings = [{'Temperature': 24.0, 'StateOfCharge': 15.0}, {'Temperature': 20.0, 'StateOfCharge': 21.0},
                        {'Temperature': 3.0, 'StateOfCharge': 59.0}, {'Temperature': 28.0, 'StateOfCharge': 45.0},
                        {'Temperature': 43.0, 'StateOfCharge': 78.0}, {'Temperature': 41.0, 'StateOfCharge': 79.0}]
        expected_bms_statistics = {'Temperature': {'min': 3.0, 'max': 43.0, 'sma': 27.0},
                                   'StateOfCharge': {'min': 15.0, 'max': 79.0, 'sma': 56.4}}
        for i in range(6):
            if i == 0:
                calc.set_initial_bms_reading(bms_readings[i])
            else:
                calc.calculate_bms_statistics(bms_readings[i])
        self.assertEqual(calc.bms_statistics, expected_bms_statistics)

    """
     *******************************************************
     Receiver Functionality Test with Mock Sender
     *******************************************************
    """

    def test_bms_receiver_with_mock_sender(self):
        print(calc.bms_statistics)
        output_type = 'console'
        max_sender_input = 7
        format_type = 'custom'
        with patch('builtins.input', side_effect=['Temperature value is 20.000000 and StateOfCharge value is 51.000000',
                                                  'Temperature value is 35.000000 and StateOfCharge value is 31.000000',
                                                  'Temperature value is 31.000000 and StateOfCharge value is 65.000000',
                                                  'Temperature value is -12.000000 and StateOfCharge value is 75.000000',
                                                  'Temperature value is 41.000000 and StateOfCharge value is 48.000000',
                                                  'Temperature value is 5.000000 and StateOfCharge value is 25.000000',
                                                  'Temperature value is 7.000000 and StateOfCharge value is 45.000000']):
            bms_receiver.bms_receiver(self.bms_parameters_with_range,
                                      max_sender_input, output_type, format_type)


if __name__ == '__main__':
    unittest.main()
