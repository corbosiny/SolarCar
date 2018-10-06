// ADC.c
/**
 * ADC for reading current.
 * @authors Katie Anderson
 * @lastRevised 9/29/2018
 */
 
 #include "ADC.h"
 #include <stdlib.h>
 #include "STM32F4XX.h"
 
// Initializes ADC ports
// inputs: none
// outputs: int to mark successful intiialization
void ADC_Initialize() {
	ADC_InitializeLowPrecision();
	ADC_InitializeHighPrecision();
}

// Initializes PA2 for use as ADC for low precision current reading
// Uses ADC1 on channel 2
// inputs:  none
// outputs: none
void ADC_InitializeHighPrecision() {
	// Enable clock for  ADC1
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1, ENABLE);
	
	// Initialize GPIOA for ADC
	GPIO_InitTypeDef GPIO_InitStruct;
	GPIO_InitStruct.GPIO_Mode = GPIO_Mode_AN;
	GPIO_InitStruct.GPIO_Pin = GPIO_Pin_2;
	GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
	GPIO_Init(GPIOA, &GPIO_InitStruct);
	
	// Init ADC 2
	ADC_InitTypeDef ADC_InitStruct;
	ADC_InitStruct.ADC_ContinuousConvMode = DISABLE;
	ADC_InitStruct.ADC_DataAlign = ADC_DataAlign_Right;
	// TODO: hange External Trig Conv?
	ADC_InitStruct.ADC_ExternalTrigConv = DISABLE;
	ADC_InitStruct.ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_None;
	ADC_InitStruct.ADC_NbrOfConversion = 1;
	ADC_InitStruct.ADC_Resolution = ADC_Resolution_12b;
	ADC_InitStruct.ADC_ScanConvMode = DISABLE;
	ADC_Init(ADC1, &ADC_InitStruct);
	ADC_Cmd(ADC1, ENABLE);
	
	// Adjust cycle reading to be faster? Currently every 84 cycles.
	ADC_RegularChannelConfig(ADC1, ADC_Channel_2, 1, ADC_SampleTime_84Cycles);
}
 

// Reads the high precision input from current board
// inputs: none
// outputs: digitial value of high precision current
uint16_t ADC_ReadHighPrecision() {
	// Start ADC conversion
	ADC_SoftwareStartConv(ADC1);
	// Wait until conversion is finished
	while (!ADC_GetFlagStatus(ADC1, ADC_FLAG_EOC));
	return ADC_GetConversionValue(ADC1);
}

// Initializes PA3 for use as ADC for low precision current reading
// Uses ADC2 on channel 3
// inputs:  none
// outputs: none
void ADC_InitializeLowPrecision() {
	// Enable clock for  ADC2
	RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC2, ENABLE);
	
	// Initialize GPIOA for ADC
	GPIO_InitTypeDef GPIO_InitStruct;
	GPIO_InitStruct.GPIO_Mode = GPIO_Mode_AN;
	GPIO_InitStruct.GPIO_Pin = GPIO_Pin_3;
	GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_NOPULL;
	GPIO_Init(GPIOA, &GPIO_InitStruct);
	
	// Init ADC 2
	ADC_InitTypeDef ADC_InitStruct;
	ADC_InitStruct.ADC_ContinuousConvMode = DISABLE;
	ADC_InitStruct.ADC_DataAlign = ADC_DataAlign_Right;
	// TODO: hange External Trig Conv?
	ADC_InitStruct.ADC_ExternalTrigConv = DISABLE;
	ADC_InitStruct.ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_None;
	ADC_InitStruct.ADC_NbrOfConversion = 1;
	ADC_InitStruct.ADC_Resolution = ADC_Resolution_12b;
	ADC_InitStruct.ADC_ScanConvMode = DISABLE;
	ADC_Init(ADC2, &ADC_InitStruct);
	ADC_Cmd(ADC2, ENABLE);
	
	// Adjust cycle reading to be faster? Currently every 84 cycles.
	ADC_RegularChannelConfig(ADC2,ADC_Channel_3, 1, ADC_SampleTime_84Cycles);
}
 
 

// Reads the low precision input from current board
// inputs: none
// outputs: digital value of low precision current
uint16_t ADC_ReadLowPrecision() {
	// Start ADC conversion
	ADC_SoftwareStartConv(ADC2);
	// Wait until conversion is finished
	while (!ADC_GetFlagStatus(ADC2, ADC_FLAG_EOC));
	return ADC_GetConversionValue(ADC2);
}
