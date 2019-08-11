# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

import odrive
# from nuevo import Ui_MainWindow
from odrive.enums import *
from odrive import shell
import math
import time

class Configuration(object):
    def set_vel(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        get_vel = MainWindow.lineEdit.text()
        my_drive.axis0.controller.config.vel_limit = int(get_vel)
        print("Velocidad cambiada a {}".format(get_vel))
        MainWindow.plainTextEdit.appendPlainText("Velocidad cambiada a :{} [RPM]".format(get_vel))

    def set_current(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        get_current = MainWindow.lineEdit_2.text()
        my_drive.axis0.motor.config.current_lim = int(get_current)
        print("Corriente cambiada a: {} [A]".format(str(get_current)))
        MainWindow.plainTextEdit.appendPlainText("Corriente cambiada a : {} [A]".format(get_current))

    def set_calibration_current(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        get_calibration_current = MainWindow.lineEdit_4.text()
        my_drive.axis0.motor.config.calibration_current = int(get_calibration_current)
        print("Corriente de calibración cambiada a: {} [A]".format(str(get_calibration_current)))
        MainWindow.plainTextEdit.appendPlainText("Corriente de calibración cambiada a : {} [A]".format(get_calibration_current))

    def initial_calibration(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        print("Iniciando calibración inicial del sistema")
        MainWindow.plainTextEdit.appendPlainText("Iniciando calibración inicial del sistema")
        my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    def closed_loop(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        MainWindow.plainTextEdit.appendPlainText("Iniciando control de lazo cerrado")
        my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        MainWindow.plainTextEdit.appendPlainText("Cargando set point = 0")
        my_drive.axis0.controller.pos_setpoint = 0

    def set_point(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        set_point = int(MainWindow.lineEdit_3.text())
        print("Buscando set_point = {}".format(str(set_point)))
        MainWindow.plainTextEdit.appendPlainText("Buscando set_point = {}".format(str(set_point)))
        my_drive.axis0.controller.pos_setpoint = set_point

    def vel_control(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        value = MainWindow.Counter.value()
        print(value)
        my_drive.axis0.controller.config.vel_limit = value

    def errors(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        errores = shell.dump_errors(my_drive)
        print(errores)
        shell.dump_errors(my_drive,True)
        MainWindow.plainTextEdit.appendPlainText(str(errores))

    def save_config(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        my_drive.save_configuration()

    def reboot(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        my_drive.reboot()
