#!/usr/bin/python3
# -*- coding: utf-8 -*-
def get_label_cmd(label, cmd, unit):
	return dict({
		'label': label,
		'cmd':	 cmd,
		'unit':  unit
	})

def get_output_mapping():
	return dict({
		VOLTAGE_IN:  voltage_in['label'],
		VOLTAGE_OUT: voltage_out['label'],
		CURRENT_IN:  current_in['label'],
		CURRENT_OUT: current_out['label'],
		POWER_IN: 	 power_in['label'],
		POWER_OUT: 	 power_out['label'],
		DUTY_CYCLE:  duty_cycle['label']
	})

def get_command_mapping():
	return dict({
		voltage_in['label']: 	voltage_in['cmd'],
		voltage_out['label']: voltage_out['cmd'],
		current_in['label']: 	current_in['cmd'],
		current_out['label']: current_out['cmd'],
		power_in['label']: 		power_out['cmd'],
		power_out['label']: 	power_out['cmd'],
		duty_cycle['label']: 	duty_cycle['cmd'],

		CUR_ALGO:  "CurrentAlgo\n",
		P_AND_O:   "PandO\n",
		INC_COND:  "IncrementalConductance\n",
		FUZ_LOGIC: "FuzzyLogic\n"
	})

def get_var_tracker(title, ylabel):
	return dict({
		'monitorActive': False,
		'plotActive': False,
		'time': [],
		'vals': [],
		'title': title,
		'y-label': ylabel,
	})

VOLTAGE_IN 	= "Voltage In"
voltage_in 	=  get_label_cmd("Get Input Voltage", "VoltageIn\n", "Voltage (V)")

VOLTAGE_OUT = "Voltage Out"
voltage_out = get_label_cmd("Get Output Voltage", "VoltageOut\n", "Voltage (V)")

CURRENT_IN 	= "Current In"
current_in 	= get_label_cmd("Get Input Current", "CurrentIn\n", "Current (A)")

CURRENT_OUT = "Current Out"
current_out = get_label_cmd("Get Output Current", "CurrentOut\n", "Current (A)")

POWER_IN 		= "Power In"
power_in 		= get_label_cmd("Get Input Power", "PowerIn\n", "Power (W)")

POWER_OUT 	= "Power Out"
power_out 	= get_label_cmd("Get Output Power", "PowerOut\n", "Power (W)")

DUTY_CYCLE 	= "Duty Cycle"
duty_cycle 	= get_label_cmd("Get Duty Cycle", "DutyCycle\n", "Percentage (%)")

CUR_ALGO		= "Current Algorithm"
P_AND_O			= "Perturb and Observe"
INC_COND    = "Incremental Conductance"
FUZ_LOGIC 	= "Fuzzy Logic"
