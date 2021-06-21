# BMS Receiver  

## Quality Parameters

- Cyclomatic Complexity CCN = 4  
- Duplication = --min-lines 3 --min-tokens 35 --threshold 0  
- coverage = 99%  

## Design

During the development of BMS Receiver, the following aspects are considered  

- Loose couplings between different objects/components  
- Open Close Principle: BMS Sender can easily extend different input/output types  
  with the least modifications in the existing code  
- Makes the code reusable: Functions are split & separated to promote re-usability  
- Flexibility - Plug in and Plug out the components at ease  
- Single Responsibility Principle  

## Test Specifications  


| Functionality            | Input        | Output                      | Faked/mocked part
|--------------------------|--------------|-----------------------------|---
BMS Receiver               | BMS Stream  from Console  | BMS Statistics            | Mock/Fake Read Input and printing to console
Null Check BMS Stream      | BMS Stream   | Empty/Non Empty             | None - it's a pure function
Validate BMS input         | Internal data-structure    | valid / invalid             | None - it's a pure function
Format   BMS input         | Internal data-structure    | Formatted BMS Readings            |  Mock Print method only to test Exception for invalid input
Find minimum,maximum,SMA   | Valid Internal data-structure  | Minimum/maximum/SMA values              | None- Pure Function 
Display BMS statistics     | BMS statistics (Min/Max/SMA) | Console Output, Formatted BMS statistics for logging purposes             | Mock/Fake printing to console
