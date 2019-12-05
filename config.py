# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

import odrive
from odrive.enums import *
from PyQt5 import QtCore, QtGui, QtWidgets
from odrive import shell
import math
import time

class Configuration(object):
    def set_vel(self,MainWindow, my_drive):
        get_vel = self.lineEdit.text()
        vel_counts = float(get_vel) * (2400/60)
        my_drive.axis0.controller.config.vel_limit = int(vel_counts)
        print("Velocidad cambiada a {}".format(vel_counts))
        self.plainTextEdit.appendPlainText("Velocidad cambiada a :{} [RPM]".format(get_vel))

    def set_current(self,MainWindow, my_drive):
        get_current = self.lineEdit_2.text()
        my_drive.axis0.motor.config.current_lim = float(get_current)
        print("Corriente cambiada a: {} [A]".format(str(get_current)))
        self.plainTextEdit.appendPlainText("Corriente cambiada a : {} [A]".format(get_current))

    def set_calibration_current(self,MainWindow, my_drive):

        get_calibration_current = self.lineEdit_4.text()
        my_drive.axis0.motor.config.calibration_current = int(get_calibration_current)
        print("Corriente de calibración cambiada a: {} [A]".format(str(get_calibration_current)))
        self.plainTextEdit.appendPlainText("Corriente de calibración cambiada a : {} [A]".format(get_calibration_current))

    def initial_calibration(self,MainWindow, my_drive):
        self.errors(my_drive)
        self.set_vel(my_drive)
        self.set_current(my_drive)
        self.set_calibration_current(my_drive)
        my_drive.config.brake_resistance = 0.5
        my_drive.axis0.motor.config.pole_pairs = 7
        my_drive.axis0.encoder.config.cpr = 2400
        print("Iniciando calibración inicial del sistema")
        self.plainTextEdit.appendPlainText("Iniciando calibración inicial del sistema")
        my_drive.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE

    def closed_loop(self,MainWindow, my_drive):
        self.errors(my_drive)
        self.plainTextEdit.appendPlainText("Iniciando control de lazo cerrado")
        my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
        # self.plainTextEdit.appendPlainText("Cargando set point = 0")
        # my_drive.axis0.controller.pos_setpoint = 0

    def set_point(self,MainWindow, my_drive):
        # Angulo deseado
        self.errors(my_drive)
        set_point = float(self.lineEdit_3.text())
        print(set_point)
        if 80.0<set_point and set_point<80.0:
            print("Dentro del if")
            self.plainTextEdit.appendPlainText("Valor fuera de los parámetros del sistema")
        # Counts_degree es el equivalente en pulsos de 1°
        else:
            counts_degree = 66.67
            # Set_point para el control de lazo cerrado en pulsos
            set_point = set_point * counts_degree
            print("Buscando set_point = {}".format(str(round(set_point,0))))
            self.plainTextEdit.appendPlainText("Buscando set_point = {}".format(str(set_point)))
            #my_drive.axis0.trap_traj.config.vel_limit = <Float>
            #my_drive.axis0.trap_traj.config.accel_limit = <Float>
            #my_drive.axis0.trap_traj.config.decel_limit = <Float>
            #my_drive.axis0.trap_traj.config.A_per_css = <Float>

            my_drive.axis0.controller.move_to_pos(set_point)


    def vel_control(self,MainWindow, my_drive):

        value = self.Counter.value()
        print(value)
        my_drive.axis0.controller.config.vel_limit = value

    def errors(self,MainWindow, my_drive):
        errores = shell.dump_errors(my_drive)

        self.plainTextEdit.appendPlainText(shell.dump_errors(my_drive))
        print(type(errores))
        shell.dump_errors(my_drive,True)


    def save_config(self,MainWindow, my_drive):
        my_drive.save_configuration()

    def reboot(self,MainWindow, my_drive):
        my_drive.reboot()
