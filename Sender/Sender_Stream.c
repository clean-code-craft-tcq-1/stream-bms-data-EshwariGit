#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#include "Sender_Stream.h"

float Temperature[BMS_DATA] = {};
float StateOfCharge[BMS_DATA] = {};
int filevalue = 0;

Bms_result (*BMSDataRead[])(float Temperature[],float StateOfCharge[])={dataread};
Bms_result(*BMSoutput[])(float Temperature[],float StateOfCharge[])={outputtoconsole};

Bms_result dataread(float Temperature[],float StateOfCharge[])
{
    float TemperatureTemp,StateOfChargeVal;
    Bms_result Status= FAIL;
    int filevalue = 0;
    FILE * file= fopen("./Sender/Sender_Text.txt","r");  
    if (file) {
        for(int iterate_counter=0;fscanf(file, "%f\t\t%f\n", &TemperatureTemp,&StateOfChargeVal)!=EOF ;iterate_counter++)
        {
            filevalue=filevalue+1;
            Temperature[iterate_counter]=TemperatureTemp;
            StateOfCharge[iterate_counter]=StateOfChargeVal;
        }

        Status= PASS;
    }
    fclose(file);
    return Status;

}


Bms_result inputvalue(BMS_inputtype inputvaluefetch)
{

    Bms_result FileRead = FAIL;
    FileRead=(*BMSDataRead[inputvaluefetch])(Temperature,StateOfCharge);
    return FileRead;


}

Bms_result outputvalue(BMS_outputtype outputvaluefetch)
{

    Bms_result Status = FAIL;
    Status=(*BMSoutput[outputvaluefetch])(Temperature,StateOfCharge);
    return Status;

}

Bms_result outputtoconsole(float Temperature[],float StateOfCharge[])
{
    for(int i=0;i<20;i++)
    {
        printf("Temperature value is %f and StateOfCharge value is %f\n",Temperature[i],StateOfCharge[i]);
    }
    return PASS;


}

