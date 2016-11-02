import sys
import datetime
import functools

from PyQt5 import QtCore, QtGui, QtWidgets

class admins():

    def __init__(self, parent):
        super(admins, self).__init__()
        self.parent = parent

    def adminPage(self, value=0):
        try:
            self.parent.centralWidget = QtWidgets.QWidget(self.parent)
            mainLayout = QtWidgets.QVBoxLayout(self.parent.centralWidget)
            label = QtWidgets.QLabel()
            label_text = "<font size=43><b>Admin PAGE</b></font>"
            label.setText(label_text)
            label.setAlignment(QtCore.Qt.AlignCenter)
            mainLayout.addWidget(label)
            layout = QtWidgets.QHBoxLayout()
            session_txt = "<font size=14><b>Session: "+self.parent.db.general_data['session'] + " Semester: "+self.parent.db.general_data['semester']+ "</b></font>"

            session_lbl = QtWidgets.QLabel(session_txt)
            session_lbl.setAlignment(QtCore.Qt.AlignCenter)
            mainLayout.addWidget(session_lbl)

            data = self.parent.db.get_user()

            table = QtWidgets.QTableWidget()
            table.setColumnCount(1)
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
            for i in ['NAME: ',]:
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
                contentitem.setText(row['username'])


                y+=1

            mainLayout.addWidget(table)
            btnLayout = QtWidgets.QHBoxLayout()

            goBackBtn = QtWidgets.QPushButton()
            goBackBtn.setText("HOME")
            goBackBtn.setMinimumSize(200, 50)
            goBackBtn.clicked.connect(self.parent.startPage)

            updateBtn = QtWidgets.QPushButton()
            updateBtn.setText("Update Session")
            updateBtn.setMinimumSize(200, 50)
            updateBtn.clicked.connect(self.set_session_details)

            addBtn = QtWidgets.QPushButton()
            addBtn.setText("Add")
            addBtn.setMinimumSize(200, 50)
            addBtn.clicked.connect(self.add_user_dialog)

            btnLayout.addWidget(goBackBtn)
            btnLayout.addWidget(updateBtn)
            btnLayout.addWidget(addBtn)

            mainLayout.addLayout(btnLayout)
            mainLayout.setAlignment(goBackBtn, QtCore.Qt.AlignHCenter)

            self.parent.setCentralWidget(self.parent.centralWidget)
        except ValueError as e:
            self.parent.errorReport(str(e))

    def add_user_dialog(self, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>ADD ADMIN FORM</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        user = {}
        user['username'] = QtWidgets.QLineEdit()
        user['password'] = QtWidgets.QLineEdit()
        user['password'].setEchoMode(QtWidgets.QLineEdit.Password)

        lecturer_lbl = QtWidgets.QLabel("Name: ")
        password_lbl = QtWidgets.QLabel("Password: ")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(lecturer_lbl,0,0)
        layout.addWidget(password_lbl,1,0)
        layout.addWidget(user['username'],0,1)
        layout.addWidget(user['password'],1,1)

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.add_user(user, main))

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

    def set_session_details(self, value = 0):
        main = QtWidgets.QDialog()
        mainLayout = QtWidgets.QVBoxLayout(main)
        label = QtWidgets.QLabel()
        label_text = "<font size=43><b>Update Semester/Session</b></font>"
        if value == 1:
            label_text = label_text + "<br /><font color=red>All fields are required!</font>"
        label.setText(label_text)
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        session = {}
        session['semester'] = QtWidgets.QComboBox()
        session['session'] = QtWidgets.QLineEdit()

        session['semester'].addItems(['First', 'Second'])
        session['semester'].setCurrentText(self.parent.db.general_data['semester'])
        session['session'].setText(self.parent.db.general_data['session'])

        semester_lbl = QtWidgets.QLabel("Semester: ")
        session_lbl = QtWidgets.QLabel("Session: ")

        layout = QtWidgets.QGridLayout()
        layout.addWidget(semester_lbl,0,0)
        layout.addWidget(session_lbl,1,0)
        layout.addWidget(session['semester'],0,1)
        layout.addWidget(session['session'],1,1)

        registerBtn = QtWidgets.QPushButton()
        registerBtn.setText("Ok")
        registerBtn.setMinimumSize(200, 50)
        registerBtn.clicked.connect(lambda: self.parent.db.update_session_details(session, main))

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


    def delete_admin(self, data, parent):
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
