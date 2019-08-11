# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

# from nuevo import Ui_MainWindow
import math, sys, os, time
import sqlite3
from sqlite3 import *
from sqlite3 import Error
from datetime import date, datetime

class Paciente(object):
    def nuevo_paciente(MainWindow):
        nombre = MainWindow.lineEdit_6.text()
        apellido = MainWindow.lineEdit_7.text()
        tipoid = MainWindow.comboBox_2.currentText()
        id = MainWindow.lineEdit_8.text()
        fechaingreso = MainWindow.dateEdit.date()
        fechaingreso = datetime.strftime(fechaingreso.toPyDate(), '%d/%m/%y')
        comentarios = MainWindow.plainTextEdit_2.toPlainText()


        data_paciente = (nombre, apellido, tipoid, int(id), fechaingreso,comentarios)
        print(data_paciente)

        # con = sqlite3.connect("pacientes")
        # cursor = con.cursor()
        # print("Creando perfil del paciente con id {}".format(str(id)))
        # MainWindow.plainTextEdit.appendPlainText("Creando perfil del paciente con id {}".format(str(id)))
        # cursor.execute('INSERT INTO pacientes(Nombre, Apellido, TipoId, Id, FechaIngreso,Comentarios) VALUES(?,?,?,?,?,?)', data_paciente)
        # con.commit()
        # con.close()
        # MainWindow.plainTextEdit.appendPlainText("Perfil del paciente creado")

        try:
            con = sqlite3.connect("pacientes")
            cursor = con.cursor()
            print("Creando perfil del paciente con id {}".format(str(id)))
            MainWindow.plainTextEdit.appendPlainText("Creando perfil del paciente con id {}".format(str(id)))
            cursor.execute('INSERT INTO pacientes(Nombre, Apellido, TipoId, Id, FechaIngreso,Comentarios) VALUES(?,?,?,?,?,?)', data_paciente)
            con.commit()
            con.close()
            MainWindow.plainTextEdit.appendPlainText("Perfil del paciente creado")



        except sqlite3.IntegrityError:
            MainWindow.plainTextEdit.appendPlainText("Ya existe un perfil con este id")
            print("Ya existe un perfil con este id")
