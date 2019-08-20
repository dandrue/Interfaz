# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

# from nuevo import Ui_MainWindow
import math, sys, os, time
import sqlite3
from sqlite3 import *
from sqlite3 import Error
from datetime import date, datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

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
            MainWindow.stackedWidget.setCurrentIndex(0)
            MainWindow.lineEdit_5.clear()
            MainWindow.lineEdit_6.clear()
            MainWindow.lineEdit_7.clear()
            MainWindow.lineEdit_8.clear()
            MainWindow.plainTextEdit_2.clear()
            self.list_all()

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


    def ir_a_perfil(MainWindow):
        item = MainWindow.treeWidget_2.selectedItems()[0]
        index = MainWindow.treeWidget_2.indexFromItem(item).row()
        data = MainWindow.treeWidget_2.topLevelItem(index).text(3)

        con = sqlite3.connect('pacientes')
        cursor = con.cursor()
        cursor.execute('SELECT * FROM pacientes WHERE Id = ?', (data,))
        row = cursor.fetchone()
        nombre = row[0]
        apellido = row[1]
        tipoid = row[2]
        id = data
        fechaingreso = row[4]
        comentarios = row[5]
        date = datetime.strptime(fechaingreso, '%d/%m/%y')
        MainWindow.lineEdit_11.setText(nombre)
        MainWindow.lineEdit_10.setText(apellido)
        MainWindow.lineEdit_9.setText(id)
        MainWindow.dateEdit_2.setDateTime(QtCore.QDateTime(date))

        if tipoid == 'Cédula':
            MainWindow.comboBox_3.setCurrentIndex(0)

        elif tipoid == 'Tarjeta de identidad':
            MainWindow.comboBox_3.setCurrentIndex(1)
        elif tipoid == 'Pasaporte':
            MainWindow.comboBox_3.setCurrentIndex(2)

        MainWindow.plainTextEdit_3.setPlainText(comentarios)
        MainWindow.lineEdit_5.clear()
        MainWindow.treeWidget_2.clear()
        MainWindow.stackedWidget.setCurrentIndex(2)

    def list_all(MainWindow):
        try:
            con = sqlite3.connect('pacientes')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM pacientes ORDER BY Apellido ASC")
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

    def eliminar_paciente(MainWindow):
        print('Eliminar paciente')
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Esta seguro de eliminar este registro")
        msgBox.setWindowTitle("Eliminar regsitro del paciente")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            try:
                con = sqlite3.connect('pacientes')
                cursor = con.cursor()
                value = MainWindow.lineEdit_9.text()
                cursor.execute('DELETE FROM pacientes WHERE Id=?', (value,))
                con.commit()
                con.close()
                MainWindow.list_all()
                MainWindow.stackedWidget.setCurrentIndex(0)
                MainWindow.lineEdit_9.clear()
                MainWindow.lineEdit_10.clear()
                MainWindow.lineEdit_11.clear()
                MainWindow.plainTextEdit_3.clear()
                MainWindow.treeWidget.clear()
                MainWindow.plainTextEdit.appendPlainText("Se ha eliminado la entrada satisfactoriamente")
                print("Se ha eliminado la entrada satisfactoriamente")
            except Error:
                MainWindow.plainTextEdit.appendPlainText("Error eliminando entrada")
                print("Error eliminando entrada")

        elif returnValue == QMessageBox.No:
            pass
