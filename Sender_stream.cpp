// Test driven Development. -> Define the testcase before implementation.
#define CATCH_CONFIG_MAIN 

#include "testsender/catch.hpp"
#include "Sender/Sender_Stream.h"

TEST_CASE("Testcase to check input data from file") 
{
 inputvalue inputvalue= FileInputType;
 REQUIRE(Read_Input_Data(inputvalue) == PASS);
}

TEST_CASE("Testcase to check if the console print is happening periodically") 
{
inputvalue inputvalue = FileInputType;
REQUIRE(Read_Input_Data(inputvalue) == PASS);
}



// Shall choose BMS parameter : Temperature and State of charge as two input parameter for implementation.
