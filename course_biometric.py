import sys
import datetime
import time
import functools
import serial
import serial.tools.list_ports
import os

from PyQt5 import QtCore, QtGui, QtWidgets

class course():

    def __init__(self, parent):
        super(course, self).__init__()
        self.parent = parent

    def coursesPage(self, value=0):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>COURSES PAGE</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        data = self.parent.db.get_courses()

        table = QtWidgets.QTableWidget()
        table.setColumnCount(5)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(True)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['COURSE CODE: ', 'TITLE: ', 'SEMESTER: ', "", ""]:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['code'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['title'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(row['semester'])

            view = QtWidgets.QPushButton("VIEW")
            view.clicked.connect(functools.partial(self.viewCoursesPage, row))
            table.setCellWidget(y, 3, view)

            modify = QtWidgets.QPushButton("MODIFY")
            modify.clicked.connect(functools.partial(self.edit_course_dialog, row))
            table.setCellWidget(y, 4, modify)


            y+=1

        mainLayout.addWidget(table)



        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("HOME")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(self.parent.startPage)

        addBtn = QtWidgets.QPushButton()
        addBtn.setText("Add")
        addBtn.setMinimumSize(200, 50)
        addBtn.clicked.connect(self.add_course_dialog)

        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(addBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

        self.parent.setCentralWidget(self.parent.centralWidget)

    def add_course_dialog(self, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>ADD COURSE FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        course_info = {}
        course_info_lbl = {}

        course_info['title'] = QtWidgets.QLineEdit()
        course_info['code'] = QtWidgets.QLineEdit()
        course_info['semester'] = QtWidgets.QComboBox()
        course_info['semester'].addItems(['First', 'Second'])

        course_info_lbl['title'] = QtWidgets.QLabel("Course Title: ")
        course_info_lbl['code'] = QtWidgets.QLabel("Course Code: ")
        course_info_lbl['semester'] = QtWidgets.QLabel("Semester: ")



        layout = QtWidgets.QGridLayout()
        layout.addWidget(course_info['title'],0,1,1,1)
        layout.addWidget(course_info['code'],1,1,1,1)
        layout.addWidget(course_info['semester'],2,1,1,1)

        layout.addWidget(course_info_lbl['title'],0,0,1,1)
        layout.addWidget(course_info_lbl['code'],1,0,1,1)
        layout.addWidget(course_info_lbl['semester'],2,0,1,1)


        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.add_course_db(course_info, main))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        mainLayout.addLayout(layout2)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        main.exec_()

    def edit_course_dialog(self, data, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>EDIT COURSE FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        course_info = {}
        course_info_lbl = {}

        course_info['id'] = data['id']
        course_info['title'] = QtWidgets.QLineEdit()
        course_info['code'] = QtWidgets.QLineEdit()
        course_info['semester'] = QtWidgets.QComboBox()
        course_info['semester'].addItems(['First', 'Second'])

        course_info['title'].setText(data['title'])
        course_info['code'].setText(data['code'])
        course_info['semester'].setCurrentText(data['semester'])

        course_info_lbl['title'] = QtWidgets.QLabel("Course Title: ")
        course_info_lbl['code'] = QtWidgets.QLabel("Course Code: ")
        course_info_lbl['semester'] = QtWidgets.QLabel("Semester: ")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(course_info['title'],0,1,1,1)
        layout.addWidget(course_info['code'],1,1,1,1)
        layout.addWidget(course_info['semester'],2,1,1,1)

        layout.addWidget(course_info_lbl['title'],0,0,1,1)
        layout.addWidget(course_info_lbl['code'],1,0,1,1)
        layout.addWidget(course_info_lbl['semester'],2,0,1,1)


        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.edit_course_db(course_info, main, data))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        deleteBtn = QtWidgets.QPushButton()
        deleteBtn.setText("Delete")
        deleteBtn.setMinimumSize(200, 50)
        deleteBtn.clicked.connect(lambda: self.delete_course(data, main))

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(deleteBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        mainLayout.addLayout(layout2)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        main.exec_()

    def delete_course(self, data, parent):
        main = QtWidgets.QDialog()
        main.resize(400, 200)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=14 color=red><b>ARE YOU SURE YOU WANT REMOVE<br />";
        label_text += data['code']
        label_text +="</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        layout = QtWidgets.QHBoxLayout()

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.delete_course(data, main, parent))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        layout.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        main.exec_()

    def viewCoursesPage(self, _data, value=0):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>"+_data['code']+" REGISTERED STUDENTS</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        data = self.parent.db.get_course_students(_data['id'])

        table = QtWidgets.QTableWidget()
        table.setColumnCount(2)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(True)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'REG NO: ']:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['student_name'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['student_regno'])



            y+=1

        mainLayout.addWidget(table)



        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("PREVIOUS PAGE")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(self.coursesPage)
        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton()
        homeBtn.setText("HOME")
        homeBtn.setMinimumSize(200, 50)
        homeBtn.clicked.connect(self.parent.startPage)

        attendanceBtn = QtWidgets.QPushButton()
        attendanceBtn.setText("ATTENDANCE")
        attendanceBtn.setMinimumSize(200, 50)
        attendanceBtn.clicked.connect(lambda: self.attendance(_data))

        addBtn = QtWidgets.QPushButton()
        addBtn.setText("ADD")
        addBtn.setMinimumSize(200, 50)
        addBtn.clicked.connect(lambda: self.add_student_dialog(_data))

        addBulkBtn = QtWidgets.QPushButton()
        addBulkBtn.setText("ADD BULK")
        addBulkBtn.setMinimumSize(200, 50)
        addBulkBtn.clicked.connect(lambda: self.add_student_bulk(_data))

        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(attendanceBtn)
        btnLayout.addWidget(addBtn)
        btnLayout.addWidget(addBulkBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

        self.parent.setCentralWidget(self.parent.centralWidget)

    def add_student_dialog(self, dat):
        data = self.parent.db.get_students()

        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.SplashScreen)
        layout = QtWidgets.QVBoxLayout(dialog)
        label_text = "<font size=43><b>REGISTER STUDENT</b></font>"
        label = QtWidgets.QLabel(label_text)
        layout.addWidget(label)
        _data = {"id": dat['id']}
        _data['student'] = QtWidgets.QComboBox()
        for i in data:
            _data['student'].addItem(i['student_name'], i['student_id'])

        btn = QtWidgets.QPushButton("ADD")
        btn.clicked.connect(lambda: self.parent.db.add_studentCourse(_data, dialog, dat))
        layout.addWidget(btn)

        layout.addWidget(_data['student'])
        dialog.exec_()

    def add_studentConfirm_dialog(self):
        message = QtWidgets.QMessageBox()
        message.setText("The user has already been registered for this courses")
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.setWindowFlags(QtCore.Qt.SplashScreen)
        message.exec_()

    def attendance(self, _data):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>"+_data['code']+" ATTENDANCE LIST</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        data = self.parent.db.get_attendance(_data['id'])

        table = QtWidgets.QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(True)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['CODE: ', 'DATE: ', 'PRESENT: ', '']:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(_data['code']+"_"+str(row['id']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(str(row['date']))

            attendanceData = self.parent.db.presents(row['id'])
            percentages = attendanceData['present'] / attendanceData['total'] * 100
            percentages = round(percentages)
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(str(percentages))

            view = QtWidgets.QPushButton("VIEW")
            view.clicked.connect(functools.partial(self.viewAttendance, row, _data))
            table.setCellWidget(y, 3, view)

            y+=1

        mainLayout.addWidget(table)



        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("PREVIOUS PAGE")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(lambda: self.viewCoursesPage(_data))
        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton()
        homeBtn.setText("HOME")
        homeBtn.setMinimumSize(200, 50)
        homeBtn.clicked.connect(self.parent.startPage)

        generateBtn = QtWidgets.QPushButton()
        generateBtn.setText("GENERATE")
        generateBtn.setMinimumSize(200, 50)
        generateBtn.clicked.connect(lambda: self._generate(_data))

        reportBtn = QtWidgets.QPushButton()
        reportBtn.setText("REPORT")
        reportBtn.setMinimumSize(200, 50)
        reportBtn.clicked.connect(lambda: self._report(_data))
        if y == 0:
            reportBtn.setDisabled(True)

        addBtn = QtWidgets.QPushButton()
        addBtn.setText("randomGenerate")
        addBtn.setMinimumSize(200, 50)
        addBtn.clicked.connect(lambda: self.parent.db.randomGenerate(_data))


        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(reportBtn)
        btnLayout.addWidget(generateBtn)
        #btnLayout.addWidget(addBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

        self.parent.setCentralWidget(self.parent.centralWidget)

    def _generate(self, _id):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.SplashScreen)
        self.ser = serial.Serial()
        comPort_combox = QtWidgets.QComboBox()

        comPort_combox.addItem("")
        for port in serial.tools.list_ports.comports():
            comPort_combox.addItem(port.device)

        comport_lbl = QtWidgets.QLabel("COMPORT")
        richtextbox1 = QtWidgets.QTextEdit()

        clear_Btn = QtWidgets.QPushButton("CLEAR")


        connect_Btn = QtWidgets.QPushButton("CONNECT")


        get_Btn = QtWidgets.QPushButton("GENERATE")
        get_Btn.setDisabled(True)

        clear_Btn.clicked.connect(lambda: richtextbox1.clear())
        connect_Btn.clicked.connect(lambda: self.connect_func(connect_Btn, comPort_combox, get_Btn))
        get_Btn.clicked.connect(lambda: self.get_attendanceData(richtextbox1, _id, dialog))

        layout = QtWidgets.QGridLayout(dialog)
        header = QtWidgets.QLabel("<font size=20>GET ATTENDANCE</font>")

        layout.addWidget(header,0,0,1,3)
        layout.addWidget(comport_lbl, 1, 0, 1,1)
        layout.addWidget(comPort_combox, 1, 1, 1,2)
        layout.addWidget(richtextbox1,2,0,1,3)
        layout.addWidget(clear_Btn, 3, 0)
        layout.addWidget(connect_Btn, 3, 1)
        layout.addWidget(get_Btn, 3, 2)

        dialog.exec_()


    def connect_func(self, btn, combo, btn2):
        comport = combo.currentText()
        if btn.text() == "CONNECT":
            if comport != "":
                self.ser.close()
                self.ser.port = comport
                self.ser.baudrate = 9600
                self.ser.bytesize = serial.EIGHTBITS
                self.ser.parity = serial.PARITY_NONE
                self.ser.stopbits = serial.STOPBITS_ONE

                self.ser.open()
                self.ser.flushOutput()

                btn.setText("DISCONNECT")
                btn2.setDisabled(False)
            else:
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setWindowTitle("Invalid Selection")
                msg.setText("SELECT a Com port first")
                msg.exec_()
        else:
            self.ser.close()
            btn.setText("CONNECT")
            btn2.setDisabled(True)


    def get_attendanceData(self, richtextbox1, _old, dialog):
        #if self.ser.port:
        #receivedData = self.receiveDataTest()
        receivedData = self.receiveSerialData()
        richtextbox1.setPlainText(receivedData)
        new_data = richtextbox1.toPlainText()
        lines = new_data.split("\n")
        data = []
        x=0
        for line in lines:

            if line and x > 4:
                _data = line.split(" ")
                data.append(_data[1])
            x += 1
        self.parent.db.generate_attendace(data, dialog, _old)



    def receiveDataTest(self):
        return self.file.read()

    def receiveSerialData(self):

        try:
            incoming = bytes()
            amount = self.ser.inWaiting()
            while self.ser.inWaiting() > 0:
                incoming += self.ser.read(1)
            income = incoming.decode("utf-8")
            if income is None:
                return "nothing"
            else:
                return income
        except (OSError, serial.SerialException):
            return "Error: Serial Port read timed out"

    def viewAttendance(self, _id, _data):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>"+_data['code']+"_"+str(_id['id'])+" STUDENT ATTENDANCE LIST</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        data = self.parent.db.get_attendance2(_id)

        table = QtWidgets.QTableWidget()
        table.setColumnCount(3)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(True)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'REG NO: ', 'PRESENT: ']:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0


        for row in data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['student_name'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['student_regno'])


            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(str(row['present']))

            y+=1

        mainLayout.addWidget(table)



        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("PREVIOUS PAGE")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(lambda: self.attendance(_data))


        homeBtn = QtWidgets.QPushButton()
        homeBtn.setText("HOME")
        homeBtn.setMinimumSize(200, 50)
        homeBtn.clicked.connect(self.parent.startPage)

        addBtn = QtWidgets.QPushButton()
        addBtn.setText("ADD")
        addBtn.setMinimumSize(200, 50)
        addBtn.clicked.connect(lambda: self.add_student_dialog(_data))

        btnLayout = QtWidgets.QHBoxLayout()

        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(addBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

        self.parent.setCentralWidget(self.parent.centralWidget)

    def _report(self, _data):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>REPORT: "+_data['code']+" ATTENDANCE LIST</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        data = self.parent.db.get_report(_data['id'])
        table = QtWidgets.QTableWidget()
        table.setColumnCount(4)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(True)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'REG NO: ', 'PERCENTAGE: ', 'STATUS']:
            header = QtWidgets.QTableWidgetItem()
            table.setHorizontalHeaderItem(x, header)
            headeritem = table.horizontalHeaderItem(x)
            headeritem.setText(i)
            x += 1

        y=0

        for row in data:
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 0, content)
            contentitem = table.item(y, 0)
            contentitem.setText(row['student_name'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 1, content)
            contentitem = table.item(y, 1)
            contentitem.setText(row['student_regno'])

            percentages = row['present'] / row['total'] * 100
            percentages = round(percentages)
            qualified = "Qualified"
            if percentages < 75:
                qualified = "Not Qualified"
            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 2, content)
            contentitem = table.item(y, 2)
            contentitem.setText(str(percentages))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 3, content)
            contentitem = table.item(y, 3)
            contentitem.setText(qualified)

            y+=1

        mainLayout.addWidget(table)



        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("PREVIOUS PAGE")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(lambda: self.attendance(_data))
        btnLayout = QtWidgets.QHBoxLayout()

        homeBtn = QtWidgets.QPushButton()
        homeBtn.setText("HOME")
        homeBtn.setMinimumSize(200, 50)
        homeBtn.clicked.connect(self.parent.startPage)

        generateBtn = QtWidgets.QPushButton()
        generateBtn.setText("GENERATE CSV")
        generateBtn.setMinimumSize(200, 50)
        generateBtn.clicked.connect(lambda: self.csvCreate(_data, data))

        addBtn = QtWidgets.QPushButton()
        addBtn.setText("ADD")
        addBtn.setMinimumSize(200, 50)
        addBtn.clicked.connect(lambda: self.add_student_dialog(_data))

        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(homeBtn)
        btnLayout.addWidget(generateBtn)
        btnLayout.addWidget(addBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

        self.parent.setCentralWidget(self.parent.centralWidget)

    def csvCreate(self, course, data):
        today = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
        header = ""
        header += "TITLE: "+course['title']+"\n"
        header += "CODE: "+course['code']+"\n"
        header += "DATE "+today+"\n"
        header += "NO: , NAME: , REG NO: , PERCENTAGE: , STATUS\n"
        body = ""
        y = 1
        for row in data:
            percentages = row['present'] / row['total'] * 100
            percentages = round(percentages)
            qualified = "Qualified"
            if percentages < 75:
                qualified = "Not Qualified"
            body += str(y)+","+row['student_name']+","+row['student_regno']+","+str(percentages)+"%,"+qualified+"\n"
            y+=1

        doc = header
        doc += body
        sep = os.sep
        newpath = os.getcwd()+""+sep+"data"+sep+'reports'+sep+course['code']+sep
        if not os.path.exists(newpath):
            os.makedirs(newpath)
        todayA = today.split(":")
        newToday = ""
        for i in todayA:
            newToday += i+"-"
        newToday.rstrip("-")
        print(newToday)
        filename = newpath+newToday+'.csv'
        csvfile = open(filename, "w+")
        csvfile.write(doc)
        csvfile.close

    def add_student_bulk(self, data):
        Holder = QtWidgets.QWidget()
        filename, ok = QtWidgets.QFileDialog.getOpenFileName(Holder, 'Open file', '.',"TEXT CSV (*.csv)")
        if filename:
            fileName = open(filename)
            for line in fileName.readlines():
                _data = line.split(",")
                if _data[0].isdigit() and _data[1] and _data[4].isdigit():
                    self.parent.db.add_studentBulkCourse(_data[4], data)
            fileName.close()
        self.viewCoursesPage(data)
