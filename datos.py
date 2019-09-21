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

    def __init__(self, temp_id):
        self.temp_id = None

    def nuevo_paciente(self,MainWindow):
        nombre = self.lineEdit_6.text().upper()
        apellido = self.lineEdit_7.text().upper()
        tipoid = self.comboBox_2.currentText()
        id = self.lineEdit_8.text()
        fechaingreso = self.dateEdit.date()
        fechaingreso = datetime.strftime(fechaingreso.toPyDate(), '%d/%m/%y')
        comentarios = self.plainTextEdit_2.toPlainText().upper()
        data_paciente = (nombre, apellido, tipoid, int(id), fechaingreso,comentarios)
        print(data_paciente)

        try:
            con = sqlite3.connect("pacientes")
            cursor = con.cursor()
            print("Creando perfil del paciente con id {}".format(str(id)))
            self.plainTextEdit.appendPlainText("Creando perfil del paciente con id {}".format(str(id)))
            cursor.execute('INSERT INTO pacientes(Nombre, Apellido, TipoId, Id, FechaIngreso,Comentarios) VALUES(?,?,?,?,?,?)', data_paciente)
            con.commit()
            con.close()
            self.plainTextEdit.appendPlainText("Perfil del paciente creado")
            self.stackedWidget.setCurrentIndex(0)
            self.lineEdit_5.clear()
            self.lineEdit_6.clear()
            self.lineEdit_7.clear()
            self.lineEdit_8.clear()
            self.plainTextEdit_2.clear()
            self.list_all(MainWindow)

        except sqlite3.IntegrityError:
            self.plainTextEdit.appendPlainText("Ya existe un perfil con este id")
            print("Ya existe un perfil con este id")

    def buscar(self,MainWindow):
        criterio = self.comboBox.currentText()
        value = self.lineEdit_5.text()
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

            self.treeWidget_2.clear()
            self.treeWidget_2.setEnabled(True)
            if range(len(rows)) == range(0, 0):
                self.treeWidget_2.setDisabled(True)
                self.plainTextEdit.appendPlainText("Ningún perfil encontrado")
                print("Ningún perfil encontrado")

            for i in range(len(rows)):
                item = "item_" + str(i)
                item = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
            for i in range(len(rows)):
                for j in range(5):
                    self.treeWidget_2.topLevelItem(i).setText(j, str(rows[i][j]))
            self.plainTextEdit.appendPlainText("Pacientes listados")
            print("Pacientes listados")

        except TypeError:
            self.plainTextEdit.appendPlainText("Error buscando pacientes")
            print("Error buscando pacientes")


    def ir_a_perfil(self,MainWindow, data):
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
        self.lineEdit_11.setText(nombre)
        self.lineEdit_10.setText(apellido)
        self.lineEdit_9.setText(id)
        self.dateEdit_2.setDateTime(QtCore.QDateTime(date))

        if tipoid == 'Cédula':
            self.comboBox_3.setCurrentIndex(0)

        elif tipoid == 'Tarjeta de identidad':
            self.comboBox_3.setCurrentIndex(1)
        elif tipoid == 'Pasaporte':
            self.comboBox_3.setCurrentIndex(2)

        self.plainTextEdit_3.setPlainText(comentarios)
        self.lineEdit_5.clear()
        self.treeWidget_2.clear()
        self.stackedWidget.setCurrentIndex(2)
        self.temp_id = id

        con = sqlite3.connect('pacientes')
        cursor = con.cursor()
        cursor.execute('SELECT * FROM Programas WHERE IdPaciente = ?', (self.temp_id,))
        data = cursor.fetchall()
        number = len(data)
        for i in range(number):
            item = "item_" + str(i)
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        for i in range(number):
            for j in range(13):
                self.treeWidget.topLevelItem(i).setText(j, str(data[i][j]))


    def list_all(self,MainWindow):
        try:
            con = sqlite3.connect('pacientes')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM pacientes ORDER BY Apellido ASC")
            rows = cursor.fetchall()
            con.commit()
            con.close()

            self.treeWidget_2.clear()
            self.treeWidget_2.setEnabled(True)
            if range(len(rows)) == range(0, 0):
                self.treeWidget_2.setDisabled(True)
                self.plainTextEdit.appendPlainText("Ningún perfil encontrado")
                print("Ningún perfil encontrado")

            for i in range(len(rows)):
                item = "item_" + str(i)
                item = QtWidgets.QTreeWidgetItem(self.treeWidget_2)
            for i in range(len(rows)):
                for j in range(5):
                    self.treeWidget_2.topLevelItem(i).setText(j, str(rows[i][j]))
            self.plainTextEdit.appendPlainText("Pacientes listados")
            print("Pacientes listados")

        except Error:
            self.plainTextEdit.appendPlainText("Error buscando pacientes")
            print("Error buscando pacientes")

    def eliminar_paciente(self,MainWindow):
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
                value = self.lineEdit_9.text()
                cursor.execute('DELETE FROM pacientes WHERE Id=?', (value,))
                con.commit()
                con.close()
                self.list_all(MainWindow)
                self.stackedWidget.setCurrentIndex(0)
                self.lineEdit_9.clear()
                self.lineEdit_10.clear()
                self.lineEdit_11.clear()
                self.plainTextEdit_3.clear()
                self.treeWidget.clear()
                self.plainTextEdit.appendPlainText("Se ha eliminado la entrada satisfactoriamente")
                print("Se ha eliminado la entrada satisfactoriamente")
            except Error:
                self.plainTextEdit.appendPlainText("Error eliminando entrada")
                print("Error eliminando entrada")

        elif returnValue == QMessageBox.No:
            pass

    def modificar_perfil(self,MainWindow):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setText("Esta seguro de modificar la información del paciente?")
        msgBox.setWindowTitle("Modificar entrada")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            nombre = self.lineEdit_11.text().upper()
            apellido = self.lineEdit_10.text().upper()
            id = self.lineEdit_9.text()
            fecha = self.dateEdit_2.date()
            fecha = datetime.strftime(fecha.toPyDate(), '%d/%m/%y')
            tipoid = self.comboBox_3.currentText()
            comentarios = self.plainTextEdit_3.toPlainText().upper()
            try:
                con = sqlite3.connect('pacientes')
                cursor = con.cursor()
                cursor.execute('UPDATE pacientes SET Nombre = ?, Apellido = ?, TipoId = ?, Id = ?, FechaIngreso = ?,Comentarios = ? WHERE id = ?', (nombre, apellido, tipoid, id, fecha, comentarios,self.temp_id))
                con.commit()
                con.close()
                print("Modificando perfil del paciente")

            except sqlite3.IntegrityError:
                self.plainTextEdit.appendPlainText("Error modificando el perfil")
                print("Error modificando el perfil")

class Programa(object):
    def nuevo_programa(self, MainWindow):
        items = self.treeWidget.topLevelItemCount()
        programa = "Programa_" + str(items + 1)

        try:
            con = sqlite3.connect('pacientes')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM programas')
            total_programas = cursor.fetchall()
            id_programa = len(total_programas) + 1
        except sqlite3.IntegrityError:
            print("Sucedio un error")
        # id_programa = int(0000) + items + 1
        self.lineEdit_12.setText(programa)
        self.lineEdit_49.setDisabled(True)
        self.lineEdit_49.setText(str(id_programa))
        self.lineEdit_50.setText(str(self.temp_id))

    def guardar_nuevo_programa(self, MainWindow):
        nombreprograma = self.lineEdit_12.text()
        id_programa = self.lineEdit_49.text()
        sesiones = self.lineEdit_13.text()
        inicio = self.dateEdit_3.date()
        inicio = datetime.strftime(inicio.toPyDate(), '%d/%m/%y')
        fin = self.dateEdit_4.date()
        fin = datetime.strftime(fin.toPyDate(), '%d/%m/%y')
        comentarios = self.plainTextEdit_4.toPlainText().upper()
        pron_init_angle = str(Programa.get_pron_init())
        pron_actual_angle = str(30)
        pron_fin_angle = pron_actual_angle
        sup_init_angle = str(Programa.get_sup_init())
        sup_actual_angle = str(25)
        sup_fin_angle = sup_actual_angle
        status = 'Activo'
        data_programa = [id_programa, self.temp_id, nombreprograma, status, inicio, fin, sesiones, pron_init_angle, pron_actual_angle, pron_fin_angle, sup_init_angle, sup_actual_angle, sup_fin_angle]

        try:
            con = sqlite3.connect('pacientes')
            cursor = con.cursor()
            cursor.execute('INSERT INTO Programas(IdPrograma, IdPaciente, NombrePrograma, status, FechaInicio,FechaFin, NumeroSesiones, AngPronInicial, AngPronActual, AngPronFinal, AngSupInicial, AngSupActual, AngSupFinal) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', data_programa)
            con.commit()
            con.close()

        except sqlite3.IntegrityError:
            self.plainTextEdit.appendPlainText("Error al generar nuevo programa, programa ya existe")
            print("Error al generar nuevo programa")

        Paciente.ir_a_perfil(self, MainWindow,self.temp_id)
        self.lineEdit_12.clear()
        self.lineEdit_49.clear()
        self.lineEdit_13.clear()
        # self.dateEdit_3.clear()
        # self.dateEdit_4.clear()
        self.plainTextEdit_4.clear()

    def get_pron_init():
        pron_init_angle = 25
        return pron_init_angle

    def get_sup_init():
        sup_init_angle = 14
        return sup_init_angle

    def ver_detalles(self, MainWindow, IdProgram):
        try:
            con = sqlite3.connect('pacientes')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM programas WHERE IdPrograma = ?', (IdProgram,))
            data = cursor.fetchall()
            print(data)


        except sqlite3.IntegrityError:
            print("Ocurrió un error")

        self.lineEdit_20.setText(data[0][2])
        self.lineEdit_21.setText(str(IdProgram))
        self.lineEdit_51.setText(str(data[0][6]))
