import sys
import datetime
import functools

from PyQt5 import QtCore, QtGui, QtWidgets

class students():

    def __init__(self, parent):
        super(students, self).__init__()
        self.parent = parent

    def studentsPage(self, value = None):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>STUDENTS PAGE</b></font>"
        if value:
            label_text += value
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        layout2 = QtWidgets.QGridLayout()
        data = self.parent.db.get_students()
        table = QtWidgets.QTableWidget()
        table.setColumnCount(8)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(False)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'REG NO: ', 'GENDER: ', 'DATE OF BIRTH: ', 'STATE', 'L.G.A','PHONE', ""]:
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
            contentitem.setText(row['student_gender'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 3, content)
            contentitem = table.item(y, 3)
            contentitem.setText(str(row['student_dob']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 4, content)
            contentitem = table.item(y, 4)
            contentitem.setText(str(row['student_state']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 5, content)
            contentitem = table.item(y, 5)
            contentitem.setText(str(row['student_lga']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 6, content)
            contentitem = table.item(y, 6)
            contentitem.setText(str(row['student_phone']))

            modify = QtWidgets.QPushButton("MODIFY")
            modify.clicked.connect(functools.partial(self.edit_student_dialog, row))
            table.setCellWidget(y, 7, modify)

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
        addBtn.clicked.connect(self.add_student_dialog)

        addBulkBtn = QtWidgets.QPushButton()
        addBulkBtn.setText("Add Bulk")
        addBulkBtn.setMinimumSize(200, 50)
        addBulkBtn.clicked.connect(self.add_student_bulk)

        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(addBtn)
        btnLayout.addWidget(addBulkBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)


        self.parent.setCentralWidget(self.parent.centralWidget)

    def bulk_add_page(self, data):
        self.parent.centralWidget = QtWidgets.QWidget(self.parent)
        mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>NEW STUDENT PAGE</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        layout2 = QtWidgets.QGridLayout()
        table = QtWidgets.QTableWidget()
        table.setColumnCount(7)
        table.setRowCount(len(data))
        table.setSortingEnabled(True)


        table.setAutoScroll(True)
        table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        table.setShowGrid(True)
        table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        table.setGridStyle(QtCore.Qt.SolidLine)
        table.setWordWrap(False)

        table.horizontalHeader().setCascadingSectionResizes(True)
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setHighlightSections(False)
        table.horizontalHeader().setSectionResizeMode(1)

        x =0
        for i in ['NAME: ', 'REG NO: ', 'GENDER: ', 'DATE OF BIRTH: ', 'STATE', 'L.G.A','PHONE']:
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
            contentitem.setText(row['student_gender'])

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 3, content)
            contentitem = table.item(y, 3)
            contentitem.setText(str(row['student_dob']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 4, content)
            contentitem = table.item(y, 4)
            contentitem.setText(str(row['student_state']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 5, content)
            contentitem = table.item(y, 5)
            contentitem.setText(str(row['student_lga']))

            content = QtWidgets.QTableWidgetItem()
            table.setItem(y, 6, content)
            contentitem = table.item(y, 6)
            contentitem.setText(str(row['student_phone']))

            y+=1

        mainLayout.addWidget(table)

        btnLayout = QtWidgets.QHBoxLayout()

        goBackBtn = QtWidgets.QPushButton()
        goBackBtn.setText("HOME")
        goBackBtn.setMinimumSize(200, 50)
        goBackBtn.clicked.connect(self.parent.startPage)

        saveBtn = QtWidgets.QPushButton()
        saveBtn.setText("SAVE")
        saveBtn.setMinimumSize(200, 50)
        saveBtn.clicked.connect(lambda: self.parent.db.bulk_add_student(data))


        btnLayout.addWidget(goBackBtn)
        btnLayout.addWidget(saveBtn)

        mainLayout.addLayout(btnLayout)
        mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)


        self.parent.setCentralWidget(self.parent.centralWidget)


    def add_student_dialog(self, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>ADD STUDENT FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        student_info = {}
        student_info_lbl = {}

        student_info['name'] = QtWidgets.QLineEdit()
        student_info['regno'] = QtWidgets.QLineEdit()
        student_info['dob'] = QtWidgets.QLineEdit()

        student_info['lga']  = QtWidgets.QLineEdit()
        student_info['address']  = QtWidgets.QLineEdit()
        student_info['phone']  = QtWidgets.QLineEdit()
        student_info['email'] = QtWidgets.QLineEdit()

        student_info['gender'] = QtWidgets.QComboBox()
        student_info['state'] = QtWidgets.QComboBox()

        genders = ['Male', 'Female']
        states = [
            'Abia','Adamawa', 'Anambra', 'Awka Ibom', 'Bauchi', 'Bayelsa',
            'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Enugu',
            'Edo', 'Ekiti', 'Gombe', 'Imo', 'Jigawa', 'Kaduna',
            'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos',
            'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
            'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'
            ]

        student_info['gender'].addItems(genders)
        student_info['state'].addItems(states)

        student_info_lbl['name'] = QtWidgets.QLabel("Name: ")
        student_info_lbl['regno'] = QtWidgets.QLabel("Reg No: ")
        student_info_lbl['gender'] = QtWidgets.QLabel("Gender: ")
        student_info_lbl['dob'] = QtWidgets.QLabel("Date of Birth: ")

        student_info_lbl['address'] = QtWidgets.QLabel("Address: ")
        student_info_lbl['lga'] = QtWidgets.QLabel("L.G.A: ")
        student_info_lbl['phone'] = QtWidgets.QLabel("Phone Number: ")
        student_info_lbl['email'] = QtWidgets.QLabel("Email Address: ")
        student_info_lbl['state'] = QtWidgets.QLabel("State: ")


        layout = QtWidgets.QFormLayout()
        layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, student_info_lbl['name'])
        layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, student_info_lbl['regno'])
        layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, student_info_lbl['gender'])
        layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, student_info_lbl['dob'])
        layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, student_info_lbl['state'])
        layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, student_info_lbl['lga'])
        layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, student_info_lbl['address'])
        layout.setWidget(7, QtWidgets.QFormLayout.LabelRole, student_info_lbl['phone'])
        layout.setWidget(8, QtWidgets.QFormLayout.LabelRole, student_info_lbl['email'])

        layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, student_info['name'])
        layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, student_info['regno'])
        layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, student_info['gender'])
        layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, student_info['dob'])
        layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, student_info['state'])
        layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, student_info['lga'])
        layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, student_info['address'])
        layout.setWidget(7, QtWidgets.QFormLayout.FieldRole, student_info['phone'])
        layout.setWidget(8, QtWidgets.QFormLayout.FieldRole, student_info['email'])

        mainLayout.addLayout(layout)


        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.add_student(student_info, main))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)
        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        mainLayout.addLayout(layout2)
        main.exec_()

    def edit_student_dialog(self, data, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>EDIT STUDENT FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        student_info = {}
        student_info_lbl = {}

        student_info['id'] = data['student_id']
        student_info['name'] = QtWidgets.QLineEdit()
        student_info['regno'] = QtWidgets.QLineEdit()
        student_info['dob'] = QtWidgets.QLineEdit()

        student_info['lga']  = QtWidgets.QLineEdit()
        student_info['address']  = QtWidgets.QLineEdit()
        student_info['phone']  = QtWidgets.QLineEdit()
        student_info['email'] = QtWidgets.QLineEdit()

        student_info['gender'] = QtWidgets.QComboBox()
        student_info['state'] = QtWidgets.QComboBox()

        genders = ['Male', 'Female']
        states = [
            'Abia','Adamawa', 'Anambra', 'Awka Ibom', 'Bauchi', 'Bayelsa',
            'Benue', 'Borno', 'Cross River', 'Delta', 'Ebonyi', 'Enugu',
            'Edo', 'Ekiti', 'Gombe', 'Imo', 'Jigawa', 'Kaduna',
            'Kano', 'Katsina', 'Kebbi', 'Kogi', 'Kwara', 'Lagos',
            'Nasarawa', 'Niger', 'Ogun', 'Ondo', 'Osun', 'Oyo',
            'Plateau', 'Rivers', 'Sokoto', 'Taraba', 'Yobe', 'Zamfara'
            ]

        student_info['gender'].addItems(genders)
        student_info['state'].addItems(states)


        student_info['name'].setText(data['student_name'])
        student_info['regno'].setText(data['student_regno'])
        student_info['dob'].setText(data['student_dob'])
        student_info['gender'].setCurrentText(data['student_gender'])

        student_info['address'].setText(data['student_address'])
        student_info['phone'].setText(data['student_phone'])
        student_info['email'].setText(data['student_email'])
        student_info['lga'].setText(data['student_lga'])
        student_info['state'].setCurrentText(data['student_state'])

        student_info_lbl['name'] = QtWidgets.QLabel("Name: ")
        student_info_lbl['regno'] = QtWidgets.QLabel("Reg No: ")
        student_info_lbl['gender'] = QtWidgets.QLabel("Gender: ")
        student_info_lbl['dob'] = QtWidgets.QLabel("Date of Birth: ")

        student_info_lbl['address'] = QtWidgets.QLabel("Address: ")
        student_info_lbl['lga'] = QtWidgets.QLabel("L.G.A: ")
        student_info_lbl['phone'] = QtWidgets.QLabel("Phone Number: ")
        student_info_lbl['email'] = QtWidgets.QLabel("Email Address: ")
        student_info_lbl['state'] = QtWidgets.QLabel("State: ")


        layout = QtWidgets.QFormLayout()
        layout.setWidget(0, QtWidgets.QFormLayout.LabelRole, student_info_lbl['name'])
        layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, student_info_lbl['regno'])
        layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, student_info_lbl['gender'])
        layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, student_info_lbl['dob'])
        layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, student_info_lbl['state'])
        layout.setWidget(5, QtWidgets.QFormLayout.LabelRole, student_info_lbl['lga'])
        layout.setWidget(6, QtWidgets.QFormLayout.LabelRole, student_info_lbl['address'])
        layout.setWidget(7, QtWidgets.QFormLayout.LabelRole, student_info_lbl['phone'])
        layout.setWidget(8, QtWidgets.QFormLayout.LabelRole, student_info_lbl['email'])

        layout.setWidget(0, QtWidgets.QFormLayout.FieldRole, student_info['name'])
        layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, student_info['regno'])
        layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, student_info['gender'])
        layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, student_info['dob'])
        layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, student_info['state'])
        layout.setWidget(5, QtWidgets.QFormLayout.FieldRole, student_info['lga'])
        layout.setWidget(6, QtWidgets.QFormLayout.FieldRole, student_info['address'])
        layout.setWidget(7, QtWidgets.QFormLayout.FieldRole, student_info['phone'])
        layout.setWidget(8, QtWidgets.QFormLayout.FieldRole, student_info['email'])

        mainLayout.addLayout(layout)


        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.edit_student(student_info, main, data))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        deleteBtn = QtWidgets.QPushButton()
        deleteBtn.setText("Delete")
        deleteBtn.setMinimumSize(200, 50)
        deleteBtn.clicked.connect(lambda: self.delete_student(data, main))


        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(deleteBtn, QtCore.Qt.AlignCenter)

        main.setWindowFlags(QtCore.Qt.SplashScreen)
        mainLayout.addLayout(layout2)
        main.exec_()

    def delete_student(self, data, parent):
        main = QtWidgets.QDialog()
        main.resize(400, 200)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=14 color=red><b>ARE YOU SURE YOU WANT REMOVE<br />";
        label_text += data['student_name']
        label_text +="</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        layout = QtWidgets.QHBoxLayout()

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.delete_student(data, main, parent))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        layout.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        main.exec_()

    def add_student_bulk(self):
        Holder = QtWidgets.QWidget()
        filename, ok = QtWidgets.QFileDialog.getOpenFileName(Holder, 'Open file', '.',"TEXT CSV (*.csv)")
        if filename:
            fileName = open(filename)
            x = 0
            data = []
            for line in fileName.readlines():
                _data = line.split(",")
                if _data[0].isdigit() and _data[1]:
                    temp = {}
                    temp['student_name'] = _data[1]+" "+_data[2]+" "+_data[3]
                    temp['student_gender'] = _data[5]
                    temp['student_regno'] = _data[4]
                    temp['student_dob'] = _data[7]
                    temp['student_state'] = _data[8]
                    temp['student_lga'] = _data[6]
                    temp['student_address'] = _data[10]
                    temp['student_phone'] = _data[9]
                    temp['student_email'] = _data[11]
                    data.append(temp)
                x += 1
            self.bulk_add_page(data)
