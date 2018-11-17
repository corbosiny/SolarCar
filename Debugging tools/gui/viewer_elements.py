#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QComboBox

import gui.viewer_constants as vc

def get_var_combobox():
	var_combo = QComboBox()
	var_combo.addItem(vc.voltage_in['label'])
	var_combo.addItem(vc.voltage_out['label'])
	var_combo.addItem(vc.current_in['label'])
	var_combo.addItem(vc.current_out['label'])
	var_combo.addItem(vc.power_in['label'])
	var_combo.addItem(vc.power_out['label'])
	var_combo.addItem(vc.duty_cycle['label'])
	return var_combo

def get_alg_combobox():
	alg_combo = QComboBox()
	alg_combo.addItem(vc.P_AND_O)
	alg_combo.addItem(vc.INC_COND)
	alg_combo.addItem(vc.FUZ_LOGIC)
	return alg_combo