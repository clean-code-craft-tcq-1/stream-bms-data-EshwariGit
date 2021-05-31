/*
 **********************************************************************************************************************
 * Includes and Definition Section
 **********************************************************************************************************************
*/

#define BMS_DATA 50

/*
 **********************************************************************************************************************
 * TypeDef handling Section
 **********************************************************************************************************************
*/


typedef struct {
float min;
float max;
}bms_data;

typedef enum
{
	FAIL,
	PASS
}Bms_result;

typedef enum{
	printtoconsole
}BMS_outputtype;

typedef enum{
	FileInputType

}BMS_inputtype;

/*
 **********************************************************************************************************************
 * TypeDef handling Section
 **********************************************************************************************************************
*/

Bms_result dataread(float Temperature[],float StateOfCharge[]);
Bms_result outputtoconsole(float Temperature[],float StateOfCharge[]);
Bms_result inputvalue(BMS_inputtype inputvaluefetch);
Bms_result outputvalue(BMS_outputtype outputvalue);


/*
 **********************************************************************************************************************
 *Extern Declarations
 **********************************************************************************************************************
*/

extern float Temperature[BMS_DATA];
extern float StateOfCharge[BMS_DATA];
