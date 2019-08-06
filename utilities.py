# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

import odrive
from interfaz_pyqt5 import Ui_MainWindow
from odrive.enums import *
from odrive import shell
import time
import math

class Functionalities(object):

    def user_vel(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        user_vel = MainWindow.lineEdit.text()
        my_drive.axis0.controller.config.vel_limit = int(user_vel)
        print("Velocidad cambiada a {}".format(str(user_vel)))
        MainWindow.plainTextEdit.appendPlainText("Velocidad = {}".format(user_vel))

    def user_current(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        user_current = MainWindow.lineEdit_2.text()
        my_drive.axis0.motor.config.current_lim = int(user_current)
        print("Corriente cambiada a {}".format(str(user_current)))
        MainWindow.plainTextEdit.appendPlainText("Corriente = {}".format(user_current))

    def calibration(MainWindow, my_drive):
        # Find a connected ODrive (this will block until you connect one)
        my_drive = MainWindow.my_drive


        #MainWindow.plainTextEdit.appendPlainText("...finding an odrive...")
        #MainWindow.plainTextEdit.appendPlainText(my_drive)

        print("starting calibration...")
        MainWindow.plainTextEdit.appendPlainText("Iniciando calibración")

        my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
        MainWindow.plainTextEdit.appendPlainText("Calibración terminada")
        print("Ending calibration...")

    def closed_loop(MainWindow, my_drive):
        print("Closed loop...")
        my_drive = MainWindow.my_drive
        MainWindow.plainTextEdit.appendPlainText("Iniciando control de lazo cerrado")
        my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        #MainWindow.plainTextEdit.appendPlainText("...Cargando set point = 0 ...")
        my_drive.axis0.controller.pos_setpoint = 0


    def set_point(MainWindow, my_drive):
        print("Seteando set point")
        my_drive = MainWindow.my_drive
        set_point = int(MainWindow.lineEdit_3.text())
        print(set_point)
        my_drive.axis0.controller.pos_setpoint = set_point
        #MainWindow.plainTextEdit.appendPlainText("...Seteando nuevo set point =  "+ str(set_point) +"...")

    def errors(MainWindow, my_drive):
        my_drive = MainWindow.my_drive
        errores = shell.dump_errors(my_drive)
        shell.dump_errors(my_drive,True)
        MainWindow.plainTextEdit.appendPlainText(str(errores))
