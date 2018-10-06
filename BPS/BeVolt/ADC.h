// ADC.h
/**
 * ADC class for reading current
 * @authors Katie Anderson
 * @lastRevised 9/29/18
 */
 
#ifndef ADC_H__
#define ADC_H__
 
#include <stdint.h>
 
// Initializes ADC ports
// inputs: none
// outputs: int to mark successful intiialization
void ADC_Initialize();

// TODO: Make two specific inits private?
void ADC_InitializeLowPrecision();

void ADC_InitializeHighPrecision();

// Reads the low precision input from current board
// inputs: none
// outputs: digital value of low precision current
uint16_t ADC_ReadLowPrecision();

// Reads the high precision input from current board
// inputs: none
// outputs: digitial value of high precision current
uint16_t ADC_ReadHighPrecision();

#endif
