#!/usr/bin/python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QGridLayout, QPushButton, QTextEdit
from PyQt5.QtGui import QTextCursor

import viewer_constants

def get_var_combobox():
	var_combo = QComboBox()
	var_combo.addItem(voltage_in['label'])
	var_combo.addItem(voltage_out['label'])
	var_combo.addItem(current_in['label'])
	var_combo.addItem(current_out['label'])
	var_combo.addItem(power_in['label'])
	var_combo.addItem(power_out['label'])
	var_combo.addItem(duty_cycle['label'])
	return var_combo

def get_alg_combobox():
	alg_combo = QComboBox()
	alg_combo.addItem(P_AND_O)
	alg_combo.addItem(INC_COND)
	alg_combo.addItem(FUZ_LOGIC)
	return alg_combo