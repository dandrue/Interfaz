#!/usr/bin/env python3.6

import odrive
from interfaz import Ui_MainWindow

class Functionalities(object):
    def config(self, MainWindow):
        user_current = MainWindow.lineEdit_2.text()
        user_vel = MainWindow.lineEdit.text()
        print(user_current)
