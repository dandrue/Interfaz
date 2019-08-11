# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

# from nuevo import Ui_MainWindow
import math, sys, os, time
import sqlite3
from sqlite3 import *
from sqlite3 import Error
from datetime import date, datetime
from PyQt5 import QtCore, QtGui, QtWidgets

class Paciente(object):
    def nuevo_paciente(MainWindow):
        nombre = MainWindow.lineEdit_6.text().upper()
        apellido = MainWindow.lineEdit_7.text().upper()
        tipoid = MainWindow.comboBox_2.currentText()
        id = MainWindow.lineEdit_8.text()
        fechaingreso = MainWindow.dateEdit.date()
        fechaingreso = datetime.strftime(fechaingreso.toPyDate(), '%d/%m/%y')
        comentarios = MainWindow.plainTextEdit_2.toPlainText().upper()


        data_paciente = (nombre, apellido, tipoid, int(id), fechaingreso,comentarios)
        print(data_paciente)

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

    def buscar(MainWindow):
        criterio = MainWindow.comboBox.currentText()
        value = MainWindow.lineEdit_5.text()

        try:
            con = sqlite3.connect("pacientes")
            cursor = con.cursor()
            if criterio == "Nombre":
                value = value.upper()
                cursor.execute('SELECT * FROM pacientes WHERE Nombre=?', (value,))
                rows = cursor.fetchall()

            elif criterio == "Apellido":
                value = value.upper()
                cursor.execute('SELECT * FROM pacientes WHERE Apellido=?', (value,))
                rows = cursor.fetchall()

            elif criterio == "Id":
                value = int(value)
                cursor.execute('SELECT * FROM pacientes WHERE Id=?', (value,))
                rows = cursor.fetchall()

            con.commit()
            con.close()

            MainWindow.treeWidget_2.clear()
            MainWindow.treeWidget_2.setEnabled(True)
            if range(len(rows)) == range(0, 0):
                MainWindow.treeWidget_2.setDisabled(True)
                MainWindow.plainTextEdit.appendPlainText("Ningún perfil encontrado")
                print("Ningún perfil encontrado")

            for i in range(len(rows)):
                item = "item_" + str(i)
                item = QtWidgets.QTreeWidgetItem(MainWindow.treeWidget_2)
            for i in range(len(rows)):
                for j in range(5):
                    MainWindow.treeWidget_2.topLevelItem(i).setText(j, str(rows[i][j]))
            MainWindow.plainTextEdit.appendPlainText("Pacientes listados")
            print("Pacientes listados")

        except Error:
            MainWindow.plainTextEdit.appendPlainText("Error buscando pacientes")
            print("Error buscando pacientes")
