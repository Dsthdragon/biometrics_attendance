import sys
import datetime
import functools

from PyQt5 import QtCore, QtGui, QtWidgets

class teachers():

    def __init__(self, parent):
        super(teachers, self).__init__()
        self.parent = parent

    def teacherPage(self, value=0):
        try:
            self.parent.centralWidget = QtWidgets.QWidget(self.parent)
            mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
            label = QtWidgets.QLabel()
            label_text = "<font size=43><b>LECTURERS PAGE</b></font>"
            label.setText(label_text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            mainLayout.addWidget(label)
            data = self.parent.db.get_lecturers()

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
            table.setWordWrap(False)

            table.horizontalHeader().setCascadingSectionResizes(True)
            table.horizontalHeader().setStretchLastSection(True)
            table.horizontalHeader().setHighlightSections(False)
            table.horizontalHeader().setSectionResizeMode(1)

            x =0
            for i in ['NAME: ', ""]:
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
                contentitem.setText(row['lecturer_name'])
                course = QtWidgets.QPushButton("COURSE")
                course.clicked.connect(functools.partial(self.edit_teacher_dialog,))
                table.setCellWidget(y, 1, course)
                modify = QtWidgets.QPushButton("MODIFY")
                modify.clicked.connect(functools.partial(self.edit_teacher_dialog, row))
                table.setCellWidget(y, 2, modify)

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
            addBtn.clicked.connect(self.add_teacher_dialog)

            btnLayout.addWidget(goBackBtn)
            btnLayout.addWidget(addBtn)

            mainLayout.addLayout(btnLayout)
            mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

            self.parent.setCentralWidget(self.parent.centralWidget)
        except ValueError as e:
            self.parent.errorReport(str(e))

    def add_teacher_dialog(self, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>ADD LECTURER FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        lecturer_txt = QtWidgets.QLineEdit()
        lecturer_lbl = QtWidgets.QLabel("Name: ")
        layout = QtWidgets.QHBoxLayout()

        layout.addWidget(lecturer_lbl)
        layout.addWidget(lecturer_txt)


        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.add_lecturer(lecturer_txt, main))

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


    def edit_teacher_dialog(self, data, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>EDIT LECTURER FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)

        lecturer = {}
        lecturer['id'] = data['lecturer_id']
        lecturer['name'] = QtWidgets.QLineEdit()
        lecturer['name'].setText(data['lecturer_name'])
        lecturer_lbl = QtWidgets.QLabel("Name: ")
        layout = QtWidgets.QHBoxLayout()


        layout.addWidget(lecturer_lbl)
        layout.addWidget(lecturer['name'])

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.edit_lecturer(lecturer, main, data))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        deleteBtn = QtWidgets.QPushButton()
        deleteBtn.setText("Delete")
        deleteBtn.setMinimumSize(200, 50)
        deleteBtn.clicked.connect(lambda: self.delete_teacher(data, main))

        layout2 = QtWidgets.QHBoxLayout()
        layout2.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        layout2.addWidget(deleteBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        mainLayout.addLayout(layout2)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        main.exec_()

    def delete_teacher(self, data, parent):
        main = QtWidgets.QDialog()
        main.resize(400, 200)
        main.setWindowFlags(QtCore.Qt.SplashScreen)
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=14 color=red><b>ARE YOU SURE YOU WANT REMOVE<br />";
        label_text += data['lecturer_name']
        label_text +="</b></font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        layout = QtWidgets.QHBoxLayout()

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.delete_lecturer(data, main, parent))

        cancelBtn = QtWidgets.QPushButton()
        cancelBtn.setText("Cancel")
        cancelBtn.setMinimumSize(200, 50)
        cancelBtn.clicked.connect(main.reject)

        layout.addWidget(registerBtn, QtCore.Qt.AlignCenter)
        layout.addWidget(cancelBtn, QtCore.Qt.AlignCenter)
        mainLayout.addLayout(layout)
        main.exec_()
