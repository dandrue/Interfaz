# -*- coding: utf-8 -*-
#!/usr/bin/env python3.6

import math, sys, os, time
import sqlite3
from sqlite3 import *
from sqlite3 import Error
from datetime import date, datetime
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import odrive
from odrive.enums import *
from odrive import shell
from config import *

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
            con = sqlite3.connect("pacientes.db")
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
            con = sqlite3.connect("pacientes.db")
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
        con = sqlite3.connect('pacientes.db')
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
        self.lineEdit_9.setText(str(id))
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

        con = sqlite3.connect('pacientes.db')
        cursor = con.cursor()
        cursor.execute('SELECT * FROM Programas WHERE IdPaciente = ?', (self.temp_id,))
        data = cursor.fetchall()
        number = len(data)
        for i in range(number):
            item = "item_" + str(i)
            item = QtWidgets.QTreeWidgetItem(self.treeWidget)
        for i in range(number):
            for j in range(15):
                self.treeWidget.topLevelItem(i).setText(j, str(data[i][j]))
                self.treeWidget.topLevelItem(i).setTextAlignment(j, QtCore.Qt.AlignCenter)


    def list_all(self,MainWindow):
        try:
            con = sqlite3.connect('pacientes.db')
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
                    self.treeWidget_2.topLevelItem(i).setTextAlignment(j, QtCore.Qt.AlignCenter)
            self.plainTextEdit.appendPlainText("Pacientes listados")
            print("Pacientes listados")

        except Error:
            self.plainTextEdit.appendPlainText("Error buscando pacientes")
            print("Error buscando pacientes")

    def eliminar_paciente(self,MainWindow):
        print('Eliminar paciente')
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QtGui.QIcon("icons/prosthetic.png"))
        msgBox.setText("Esta seguro de eliminar este registro")
        msgBox.setWindowTitle("Eliminar regsitro del paciente")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            try:
                con = sqlite3.connect('pacientes.db')
                cursor = con.cursor()
                value = self.lineEdit_9.text()
                cursor.execute('DELETE FROM pacientes WHERE Id=?', (value,))
                con.commit()
                self.list_all(MainWindow)
                self.stackedWidget.setCurrentIndex(0)
                self.lineEdit_9.clear()
                self.lineEdit_10.clear()
                self.lineEdit_11.clear()
                self.plainTextEdit_3.clear()
                self.treeWidget.clear()
                cursor.execute('SELECT IdPrograma FROM Programas WHERE IdPaciente = ?' , (self.temp_id,))
                idProgramas = cursor.fetchall()

                cursor.execute('DELETE FROM Programas WHERE IdPaciente = ?', (self.temp_id,))
                if len(idProgramas) >0:
                    if idProgramas[0] != None:
                        for i in idProgramas[0]:
                            cursor.execute('DELETE FROM Sesiones WHERE IDPrograma = ?' , (i,))
                    else:
                        print('No existen sesiones vinculadas al paciente')
                self.plainTextEdit.appendPlainText("Se ha eliminado la entrada satisfactoriamente")
                print("Se ha eliminado la entrada satisfactoriamente")
                con.commit()
                con.close()
            except Error:
                self.plainTextEdit.appendPlainText("Error eliminando entrada")
                print("Error eliminando entrada")

        elif returnValue == QMessageBox.No:
            pass

    def modificar_perfil(self,MainWindow):

        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QtGui.QIcon("icons/prosthetic.png"))
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
                con = sqlite3.connect('pacientes.db')
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
        self.plainTextEdit_4.clear()
        items = self.treeWidget.topLevelItemCount()
        programa = "Programa_" + str(items + 1)

        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('SELECT max(IdPrograma) FROM programas')
            max_programa = cursor.fetchone()[0]
            if max_programa != None:
                id_programa = max_programa + 1
            else:
                id_programa = 1
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
        my_drive = self.my_drive
        pron_init_angle = str(self.lineEdit_14.text())
        pron_actual_angle = str(30)
        pron_fin_angle = pron_actual_angle
        sup_init_angle = str(self.lineEdit_15.text())
        sup_actual_angle = str(25)
        sup_fin_angle = sup_actual_angle
        if self.radioButton.isChecked():
            miembro = 'Derecho'
        else:
            miembro = 'Izquierdo'
        data_programa = [id_programa, self.temp_id, nombreprograma, miembro, inicio, fin, sesiones, 0,pron_init_angle, pron_init_angle, 0, sup_init_angle, sup_init_angle, 0, comentarios]

        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('INSERT INTO Programas(IdPrograma, IdPaciente, NombrePrograma, Miembro, FechaInicio,FechaFin, NumeroSesiones, SesionesRealizadas ,AngPronInicial, AngPronActual, TMaxP, AngSupInicial, AngSupActual, TMaxS, Comentarios) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', data_programa)
            con.commit()
            con.close()

        except sqlite3.IntegrityError:
            self.plainTextEdit.appendPlainText("Error al generar nuevo programa, programa ya existe")
            print("Error al generar nuevo programa")

        Paciente.ir_a_perfil(self, MainWindow,self.temp_id)
        self.lineEdit_12.clear()
        self.lineEdit_49.clear()
        self.lineEdit_13.clear()
        self.plainTextEdit_4.clear()



    def ver_detalles(self, MainWindow, IdProgram):
        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('SELECT * FROM Programas WHERE IdPrograma = ?', (IdProgram,))
            data = cursor.fetchall()

        except sqlite3.IntegrityError:
            print("Ocurrió un error")


        inicio = datetime.strptime(data[0][4], '%d/%m/%y')
        fin = datetime.strptime(data[0][5], '%d/%m/%y')
        miembro = data[0][3]
        if miembro == "Izquierdo":
            self.radioButton_4.setChecked(True)
        if miembro == "Derecho":
            self.radioButton_3.setChecked(True)

        self.lineEdit_20.setText(data[0][2])
        self.lineEdit_21.setText(str(IdProgram))
        self.lineEdit_51.setText(str(data[0][6]))
        self.lineEdit_27.setText(str(data[0][8]))
        self.lineEdit_23.setText(str(data[0][9]))
        self.lineEdit_24.setText(str(data[0][10]))
        self.lineEdit_25.setText(str(data[0][11]))
        self.lineEdit_26.setText(str(data[0][12]))
        self.lineEdit_22.setText(str(data[0][13]))

        self.dateEdit_5.setDateTime(QtCore.QDateTime(inicio))
        self.dateEdit_6.setDateTime(QtCore.QDateTime(fin))
        self.plainTextEdit_5.setPlainText(data[0][14])

        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute("SELECT * FROM Sesiones WHERE IDPrograma = ?",(IdProgram,))
            rows = cursor.fetchall()
            con.commit()
            con.close()

            self.treeWidget_3.clear()

            for i in range(len(rows)):
                item = "item_" + str(i)
                item = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
            for i in range(len(rows)):
                for j in range(13):
                    self.treeWidget_3.topLevelItem(i).setText(j, str(rows[i][j]))
                    self.treeWidget_3.topLevelItem(i).setTextAlignment(j, QtCore.Qt.AlignCenter)
            #self.plainTextEdit.appendPlainText("Sesiones listados")
            print("Sesiones listados")

        except Error:
            self.plainTextEdit.appendPlainText("Error buscando sesiones")
            print("Error buscando sesiones")

        sesionesrealizadas = self.treeWidget_3.topLevelItemCount()

        self.lineEdit_52.setText(str(sesionesrealizadas))
        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('UPDATE Programas SET SesionesRealizadas = ? WHERE IdPrograma = ?', (sesionesrealizadas,IdProgram,))
            con.commit()
            con.close()
        except Error:
            self.plainTextEdit.appendPlainText("Error buscando sesiones")
            print("Error buscando sesiones")

    def eliminar_programa(self, MainWindow,IdProgram, IdPaciente):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QtGui.QIcon("icons/prosthetic.png"))
        msgBox.setText("Esta seguro de modificar la información del paciente?")
        msgBox.setWindowTitle("Modificar entrada")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            print("Eliminando programa {}".format(IdProgram))
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('DELETE FROM programas WHERE IdPrograma = ?', (int(IdProgram),))
            cursor.execute('DELETE FROM Sesiones WHERE IDPrograma = ?',(IdProgram,))
            self.treeWidget.clear()
            cursor.execute('SELECT * FROM programas WHERE IdPaciente = ?', (IdPaciente,))
            rows = cursor.fetchall()
            for i in range(len(rows)):
                item = "item_" + str(i)
                item = QtWidgets.QTreeWidgetItem(self.treeWidget)
            for i in range(len(rows)):
                for j in range(12):
                    self.treeWidget.topLevelItem(i).setText(j, str(rows[i][j]))
                    self.treeWidget.topLevelItem(i).setTextAlignment(j, QtCore.Qt.AlignCenter)
            self.plainTextEdit.appendPlainText("Pacientes listados")
            print("Pacientes listados")
            con.commit()
            con.close()

    def get_pron_init(self, MainWindow, my_drive, miembro):
        print(self.lineEdit_14.text())
        if miembro:
            my_drive.axis0.requested_state = AXIS_STATE_IDLE
            pron_init_pulses = my_drive.axis0.encoder.pos_estimate
            pron_init_angle = -pron_init_pulses / 66.67
            print(round(pron_init_angle,0))
            self.lineEdit_14.setText(str(round(pron_init_angle,1)))
        else:
            my_drive.axis0.requested_state = AXIS_STATE_IDLE
            pron_init_pulses = my_drive.axis0.encoder.pos_estimate
            pron_init_angle = pron_init_pulses / 66.67
            print(round(pron_init_angle,0))
            self.lineEdit_14.setText(str(round(pron_init_angle,1)))
        return pron_init_angle

    def get_sup_init(self, MainWindow, my_drive, miembro):
        if miembro:
            my_drive.axis0.requested_state = AXIS_STATE_IDLE
            sup_init_pulses = my_drive.axis0.encoder.pos_estimate
            sup_init_angle = -sup_init_pulses / 66.67
            print(round(sup_init_angle,0))
            self.lineEdit_15.setText(str(round(sup_init_angle,1)))
        else:
            my_drive.axis0.requested_state = AXIS_STATE_IDLE
            sup_init_pulses = my_drive.axis0.encoder.pos_estimate
            sup_init_angle = sup_init_pulses / 66.67
            print(round(sup_init_angle,0))
            self.lineEdit_15.setText(str(round(sup_init_angle,1)))
        return sup_init_angle



class Sesion(object):
    def nueva_sesion(self, MainWindow):
        items = self.treeWidget_3.topLevelItemCount() + 1
        nombresesion = "Sesion_" + str(items)
        idpaciente = self.temp_id
        program_id = int(self.lineEdit_21.text())

        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute("SELECT MAX(IDSesion) FROM Sesiones")
            idSesion = cursor.fetchone()[0]
            print(idSesion)
            if idSesion == None:
                idSesion = 1
            else:
                idSesion = int(idSesion)+1
            cursor.execute("SELECT * FROM Programas WHERE IdPrograma = ?", (program_id,))
            data = cursor.fetchall()

        except sqlite3.IntegrityError:
            print("Ocurrió un error")

        idpaciente = data[0][1]
        pron_actual = data[0][9]
        sup_actual = data[0][12]
        self.lineEdit_45.setText(str(idpaciente))
        self.lineEdit_28.setText(str(program_id))
        self.lineEdit_29.setText(str(pron_actual))
        self.lineEdit_30.setText(str(sup_actual))
        self.lineEdit_54.setText(nombresesion)
        self.lineEdit_53.setText(str(idSesion))
        self.lineEdit_46.setText(str(items))
        self.lineEdit_31.setText(str(pron_actual))
        self.lineEdit_34.setText(str(sup_actual))

    def pronacion(self, MainWindow, my_drive, miembro):
        try:
            if miembro:
                self.doubleSpinBox_2.setValue(0)
                current = self.doubleSpinBox.value()
                position = float(self.lineEdit_31.text())
                self.lineEdit_47.setText(str(position))
                Configuration.closed_loop(self,MainWindow, my_drive)
                my_drive.axis0.motor.config.current_lim = current
                my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                my_drive.axis0.controller.move_to_pos(-position*66.67)
            else:
                self.doubleSpinBox_2.setValue(0)
                current = self.doubleSpinBox.value()
                position = float(self.lineEdit_31.text())
                self.lineEdit_47.setText(str(position))
                Configuration.closed_loop(self,MainWindow, my_drive)
                my_drive.axis0.motor.config.current_lim = current
                my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                my_drive.axis0.controller.move_to_pos(position*66.67)
        except ValueError:
            self.plainTextEdit.appendPlainText("Error en el valor ingresado")


    def ganancia(self, MainWindow, my_drive, miembro):
        if miembro:
            position = float(self.lineEdit_31.text())
            ganancia = self.doubleSpinBox_2.value()
            total = position + ganancia
            actual = float(self.lineEdit_47.text())
            # self.lineEdit_31.setText(str(total))
            self.lineEdit_47.setText(str(total))
            my_drive.axis0.controller.move_to_pos(-total * 66.67)
        else:
            position = float(self.lineEdit_31.text())
            ganancia = self.doubleSpinBox_2.value()
            total = (position + ganancia)
            actual = float(self.lineEdit_47.text())
            # self.lineEdit_31.setText(str(total))
            self.lineEdit_47.setText(str(total))
            my_drive.axis0.controller.move_to_pos(total * 66.67)

    def supinacion(self, MainWindow, my_drive, miembro):
        try:
            if miembro:
                self.doubleSpinBox_4.setValue(0)
                current = self.doubleSpinBox_3.value()
                position = float(self.lineEdit_34.text())
                self.lineEdit_48.setText(str(position))
                Configuration.closed_loop(self,MainWindow, my_drive)
                my_drive.axis0.motor.config.current_lim = current
                my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                my_drive.axis0.controller.move_to_pos(-position*66.67)
            else:
                self.doubleSpinBox_4.setValue(0)
                current = self.doubleSpinBox_3.value()
                position = float(self.lineEdit_34.text())
                self.lineEdit_48.setText(str(position))
                Configuration.closed_loop(self,MainWindow, my_drive)
                my_drive.axis0.motor.config.current_lim = current
                my_drive.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
                my_drive.axis0.controller.move_to_pos(position*66.67)
        except ValueError:
            self.plainTextEdit.appendPlainText("Error en el valor ingresado")

    def gananciaSup(self, MainWindow, my_drive, miembro):
        if miembro:
            position = float(self.lineEdit_34.text())
            ganancia = -self.doubleSpinBox_4.value()
            total = (position + ganancia)
            actual = float(self.lineEdit_48.text())
            # self.lineEdit_34.setText(str(total))
            self.lineEdit_48.setText(str(total))
            my_drive.axis0.controller.move_to_pos(-total * 66.67)
        else:
            position = float(self.lineEdit_34.text())
            ganancia = self.doubleSpinBox_4.value()
            total = position - ganancia
            actual = float(self.lineEdit_48.text())
            # self.lineEdit_34.setText(str(total))
            self.lineEdit_48.setText(str(total))
            my_drive.axis0.controller.move_to_pos(total * 66.67)

    def guardarSesion(self, MainWindow):
        idsesion = int(self.lineEdit_53.text())
        idprograma = int(self.lineEdit_28.text())
        nombre = self.lineEdit_54.text()
        sesionnumero = int(self.lineEdit_46.text())
        fecha = self.dateEdit_7.date()
        fecha = datetime.strftime(fecha.toPyDate(), '%d/%m/%y')
        repeticionesp = int(self.lineEdit_41.text())
        anginitp = float(self.lineEdit_29.text())
        angfinp = float(self.lineEdit_47.text())
        repeticioness = int(self.lineEdit_41.text())
        anginits = float(self.lineEdit_30.text())
        angfins = float(self.lineEdit_48.text())
        torquep = float(self.lineEdit_33.text())
        torques = float(self.lineEdit_35.text())

        nsesiones = int(self.lineEdit_52.text()) + 1


        data = [idsesion, idprograma, sesionnumero, nombre,fecha, repeticionesp, anginitp, angfinp, repeticioness, anginits, angfins, torquep, torques]
        data_2 = [nsesiones,angfinp, angfins,torquep, torques, idprograma]

        try:
            con = sqlite3.connect('pacientes.db')
            cursor = con.cursor()
            cursor.execute('INSERT INTO Sesiones(IDSesion, IDPrograma, SesionNumero, Nombre,Fecha, RepeticionesP, AngInitP, AngFinP, RepeticionesS ,AngIniS, AngFinS, TorqueMaxP, TorqueMaxS) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)', data)
            cursor.execute('UPDATE Programas SET SesionesRealizadas=?, AngPronActual=? , AngSupActual=?,TMaxP=?,TMaxS =? WHERE IDPrograma = ?',data_2)
            con.commit()
            con.close()

        except sqlite3.IntegrityError:
            self.plainTextEdit.appendPlainText("Error al generar nueva sesion")
            print("Error al generar nueva sesión")



    def eliminar_sesion(self, MainWindow,IdProgram, IdSesion):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QtGui.QIcon("icons/prosthetic.png"))
        msgBox.setText("Esta seguro de modificar la información del paciente?")
        msgBox.setWindowTitle("Modificar entrada")
        msgBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        returnValue = msgBox.exec()

        if returnValue == QMessageBox.Yes:
            print("Eliminando sesion {}".format(IdSesion))

            try:
                con = sqlite3.connect('pacientes.db')
                cursor = con.cursor()
                cursor.execute('DELETE FROM Sesiones WHERE IDPrograma = ? AND IDSesion = ?', (IdProgram,IdSesion))
                con.commit()
                sesiones = int(self.lineEdit_52.text())
                print('Sesiones ' + str(sesiones))
                nsesiones = sesiones - 1
                print('nsesiones ' + str(nsesiones))
                self.lineEdit_52.setText(str(nsesiones))

                cursor.execute("SELECT * FROM Sesiones WHERE IDPrograma = ?",(IdProgram,))
                rows = cursor.fetchall()

                self.treeWidget_3.clear()

                for i in range(len(rows)):
                    item = "item_" + str(i)
                    item = QtWidgets.QTreeWidgetItem(self.treeWidget_3)
                for i in range(len(rows)):
                    for j in range(13):
                        self.treeWidget_3.topLevelItem(i).setText(j, str(rows[i][j]))
                        self.treeWidget_3.topLevelItem(i).setTextAlignment(j, QtCore.Qt.AlignCenter)
                #self.plainTextEdit.appendPlainText("Sesiones listadas")
                print("Sesiones listadas")
                cursor.execute("SELECT MAX(IDSesion) FROM Sesiones WHERE IDPrograma=?", (IdProgram,))
                idSesion = cursor.fetchone()[0]
                print(idSesion)
                cursor.execute('SELECT * FROM Sesiones WHERE IDSesion = (SELECT MAX(IDSesion) FROM Sesiones) AND IDPrograma = ?', (IdProgram,))
                rows = cursor.fetchone()
                print(rows)
                if rows!=None:
                    angFinP = rows[7]
                    angFinS = rows[10]
                    TMaxP =  rows[11]
                    TMaxS = rows[12]
                    self.lineEdit_23.setText(str(angFinP))
                    self.lineEdit_26.setText(str(angFinS))
                    self.lineEdit_24.setText(str(TMaxP))
                    self.lineEdit_22.setText(str(TMaxS))
                    data = [nsesiones, angFinP, angFinS,TMaxP,TMaxS, IdProgram]
                    print(data)

                else:
                    cursor.execute("SELECT * FROM Programas WHERE IdPrograma = ?", (IdProgram,))
                    datos = cursor.fetchone()
                    pron = datos[8]
                    sup = datos[11]
                    self.lineEdit_23.setText(str(pron))
                    self.lineEdit_26.setText(str(sup))
                    self.lineEdit_24.setText(str(0.0))
                    self.lineEdit_22.setText(str(0.0))
                    data = [nsesiones, pron,sup,0,0,IdProgram]
                cursor.execute('UPDATE Programas SET SesionesRealizadas=?, AngPronActual=? , AngSupActual=?,TMaxP=?,TMaxS =? WHERE IDPrograma = ?',data)
                con.commit()
                con.close()

            except Error:
                self.plainTextEdit.appendPlainText("Error al eliminar la sesión")
                print("Error al eliminar la sesión")
