#import MySQLdb
import db_biometric
import student_biometric
import course_biometric
import teacher_biometric
import admin_biometric


import sys
import datetime
import os

from PyQt5 import QtCore, QtGui, QtWidgets


class Biometrics(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(Biometrics, self).__init__(parent)
        self.user = {}
        #stylesheet = """
        #    QMainWindow, QDialog, QTableWidget {
        #        background-color: black;
        #        color: white;
        #    }
        #    QLabel {
        #        color: blue;
        #    }
        #"""
        #self.setStyleSheet(stylesheet)
        self.db = db_biometric.database(self)
        self.db.setConfig()
        self.configSet = 0
        while self.configSet == 0:
            self.db.runConfig()
        self.student_class = student_biometric.students(self)
        self.course_class = course_biometric.course(self)
        self.lecturer_class = teacher_biometric.teachers(self)
        self.admin_class = admin_biometric.admins(self)

        self.showFullScreen()
        self.centralWidget = QtWidgets.QWidget(self)
        self.setWindowTitle("BIOMETRIC ATTENDANCE")

        self.loginPage()

    def loginPage(self, failed = 0):
        self.centralWidget = QtWidgets.QWidget(self)
        mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        login_msg = "<font size=24>Kindly enter login details.<br></font>"
        if failed == 1:
            login_msg  = login_msg + "<font color=red><b><br />Invalid login details</b></font>"
        elif failed == 2:
            login_msg  = login_msg + "<font color=red><b><br />All fields required!</b></font>"
        label = QtWidgets.QLabel(login_msg)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setMaximumHeight(100)
        mainLayout.addWidget(label)

        label2 = QtWidgets.QLabel("safe")
        sep = os.sep
        imagelink = os.getcwd()+""+sep+"data"+sep+"image"+sep+"startup.png"
        image = QtGui.QPixmap(imagelink)
        newimage = image.scaled(label2.size(), QtCore.Qt.KeepAspectRatio)

        label2.setAlignment(QtCore.Qt.AlignCenter)
        label2.setPixmap(newimage)

        mainLayout.addWidget(label2)

        self.name_entry = QtWidgets.QLineEdit()
        self.pass_entry = QtWidgets.QLineEdit()
        self.name_entry.setMaximumWidth(500)
        self.pass_entry.setMaximumWidth(500)
        self.pass_entry.setEchoMode(QtWidgets.QLineEdit.Password)

        nameLayout = QtWidgets.QHBoxLayout()
        name_lbl = QtWidgets.QLabel("NAME")
        name_lbl.setMaximumWidth(300)
        nameLayout.addWidget(name_lbl)
        nameLayout.addWidget(self.name_entry)
        mainLayout.addLayout(nameLayout)
        passLayout = QtWidgets.QHBoxLayout()

        pass_lbl = QtWidgets.QLabel("PASSWORD")
        pass_lbl.setMaximumWidth(300)
        passLayout.addWidget(pass_lbl)
        passLayout.addWidget(self.pass_entry)
        mainLayout.addLayout(passLayout)
        btnLayout = QtWidgets.QHBoxLayout()

        loginBtn = QtWidgets.QPushButton()
        loginBtn.setText("LOGIN")
        loginBtn.setMaximumSize(200, 50)
        loginBtn.clicked.connect(self.login)

        exitBtn = QtWidgets.QPushButton()
        exitBtn.setText("EXIT")
        exitBtn.setMaximumSize(200, 50)
        exitBtn.clicked.connect(self.close)
        btnLayout.addWidget(loginBtn)
        btnLayout.addWidget(exitBtn)
        mainLayout.addLayout(btnLayout)
        self.setCentralWidget(self.centralWidget)

    def login(self):
        data = {
        'username':self.name_entry.text(),
        'password':self.pass_entry.text()
        }
        #self.user = data
        self.db.login(data)
        #self.startPage()
        #if self.name_entry.text() == self.user['username'] and self.pass_entry.text() == self.user['password']:
        #    self.user['login'] = 1
        #if self.user['login'] == 1:
            #self.startPage()
        #else:
        #    self.loginPage(1)

    def startPage(self):
        self.centralWidget = QtWidgets.QWidget(self)
        mainLayout = QtWidgets.QVBoxLayout(self.centralWidget)

        user = QtWidgets.QLabel("<font size=20>WELCOME "+self.user['username']+"</font>")
        user.setAlignment(QtCore.Qt.AlignCenter)
        user.setFixedHeight(80)
        mainLayout.addWidget(user)

        label = QtWidgets.QLabel()
        sep = os.sep
        imagelink = os.getcwd()+""+sep+"data"+sep+"image"+sep+"startup.png"
        image = QtGui.QPixmap(imagelink)
        #label.setStyleSheet("QLabel {background-color: black;}")
        newimage = image.scaled(self.size(), QtCore.Qt.KeepAspectRatio)
        label.setAlignment(QtCore.Qt.AlignCenter)
        label.setPixmap(newimage)

        mainLayout.addWidget(label)

        courses = QtWidgets.QPushButton()
        students = QtWidgets.QPushButton()
        #teachers = QtWidgets.QPushButton()
        about = QtWidgets.QPushButton()
        admin = QtWidgets.QPushButton()
        change_password = QtWidgets.QPushButton()
        _exit = QtWidgets.QPushButton()

        courses.setMaximumSize(200, 50)
        students.setMaximumSize(200, 50)
        #teachers.setMaximumSize(200, 50)
        about.setMaximumSize(200, 50)
        admin.setMaximumSize(200, 50)
        change_password.setMaximumSize(200, 50)
        _exit.setMaximumSize(200, 50)

        courses.setText("Courses")
        #teachers.setText("Teachers")
        about.setText("About")
        students.setText("Students")
        admin.setText("Admin")
        change_password.setText("Change Password")
        _exit.setText("EXIT")

        students.clicked.connect(self.student_class.studentsPage)
        courses.clicked.connect(self.course_class.coursesPage)
        #teachers.clicked.connect(self.lecturer_class.teacherPage)
        about.clicked.connect(self.aboutApp)
        admin.clicked.connect(self.admin_class.adminPage)
        change_password.clicked.connect(self.changePassword)
        _exit.clicked.connect(self.close)

        layout = QtWidgets.QGridLayout()

        layout.addWidget(courses, 0,0,1,1)
        layout.addWidget(students, 0,1,1,1)
        layout.addWidget(admin, 0,2,1,1)

        layout.addWidget(about, 1,0,1,1)
        layout.addWidget(change_password, 1,1,1,1)
        layout.addWidget(_exit, 1,2,1,1)
        mainLayout.addLayout(layout)

        self.setCentralWidget(self.centralWidget)

    def changePassword(self, value = 0):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.SplashScreen)
        layout = QtWidgets.QVBoxLayout(dialog)
        login_msg = "<font size=43><b>CHANGE PASSWORD</b></font><br />"
        if value == 1:
            login_msg  = login_msg + "<font color=red><b><br />All fields required!</b></font>"
        elif value == 2:
            login_msg  = login_msg + "<font color=red><b><br />Password did not match!</b></font>"
        elif value == 3:
            login_msg  = login_msg + "<font color=red><b><br />Password not correct!</b></font>"

        label = QtWidgets.QLabel(login_msg)
        layout.addWidget(label)
        data = {}
        data['old'] = QtWidgets.QLineEdit()
        data['new'] = QtWidgets.QLineEdit()
        data['confirm'] = QtWidgets.QLineEdit()

        data['old'].setEchoMode(QtWidgets.QLineEdit.Password)
        data['new'].setEchoMode(QtWidgets.QLineEdit.Password)
        data['confirm'].setEchoMode(QtWidgets.QLineEdit.Password)

        oldP = QtWidgets.QLabel("Password")
        newP = QtWidgets.QLabel("New Password")
        confirmP = QtWidgets.QLabel("Confirmation")

        layout2 = QtWidgets.QGridLayout()
        layout2.addWidget(oldP,0,0)
        layout2.addWidget(newP,1,0)
        layout2.addWidget(confirmP,2,0)
        layout2.addWidget(data['old'],0,1)
        layout2.addWidget(data['new'],1,1)
        layout2.addWidget(data['confirm'],2,1)

        layout.addLayout(layout2)
        cancelBtn = QtWidgets.QPushButton("CANCEL")
        cancelBtn.clicked.connect(dialog.close)

        updateBtn = QtWidgets.QPushButton("UPDATE")
        updateBtn.clicked.connect(lambda: self.db.change_password(data, dialog))

        btnLayout  = QtWidgets.QHBoxLayout()
        btnLayout.addWidget(cancelBtn)
        btnLayout.addWidget(updateBtn)
        layout.addLayout(btnLayout)
        dialog.exec_()

    def closeEvent(self, event):
        message = QtWidgets.QMessageBox()
        message.setText("Are you sure you want to exit?")
        message.setIcon(QtWidgets.QMessageBox.Question)
        message.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        message.setWindowFlags(QtCore.Qt.SplashScreen)
        reply = message.exec_()

        if reply == QtWidgets.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def successChange(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.SplashScreen)
        dialog.setFixedSize(400, 200)
        layout = QtWidgets.QVBoxLayout(dialog)
        label = QtWidgets.QLabel('<font size=20><b>Password change successful</b></font>')
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)
        okButton = QtWidgets.QPushButton()
        okButton.setText("ok")
        okButton.clicked.connect(dialog.accept)
        layout.addWidget(okButton)
        dialog.exec_()

    def newConfig(self, oldData = None):
        dialog = QtWidgets.QDialog()
        dialog.setWindowFlags(QtCore.Qt.SplashScreen)
        dialog.setFixedSize(400, 400)
        mainLayout = QtWidgets.QVBoxLayout(dialog)
        label = QtWidgets.QLabel("<font size=20>New Config</font>")
        label.setAlignment(QtCore.Qt.AlignCenter)
        mainLayout.addWidget(label)
        formLayout = QtWidgets.QFormLayout()
        config = {}
        config['host'] = QtWidgets.QLineEdit()
        if oldData:
            config['host'].setText(oldData['host'])
        config['database'] = QtWidgets.QLineEdit()
        if oldData:
            config['database'].setText(oldData['database'])
        config['user'] = QtWidgets.QLineEdit()
        if oldData:
            config['user'].setText(oldData['user'])
        config['password'] = QtWidgets.QLineEdit()
        config['password'].setEchoMode(QtWidgets.QLineEdit.Password)
        if oldData:
            config['password'].setText(oldData['password'])

        configlabel = {}
        configlabel['host'] = QtWidgets.QLabel("Hostname")
        configlabel['database'] = QtWidgets.QLabel("database")
        configlabel['user'] = QtWidgets.QLabel("Username")
        configlabel['password'] = QtWidgets.QLabel("Password")

        formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, configlabel['host'])
        formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, configlabel['database'])
        formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, configlabel['user'])
        formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, configlabel['password'])

        formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, config['host'])
        formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, config['database'])
        formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, config['user'])
        formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, config['password'])

        mainLayout.addLayout(formLayout)

        btnLayout = QtWidgets.QHBoxLayout()
        okBtn = QtWidgets.QPushButton("Submit")
        okBtn.clicked.connect(lambda: self.db.createConfig(config, dialog))
        btnLayout.addWidget(okBtn)
        cancelBtn = QtWidgets.QPushButton("Cancel")
        cancelBtn.clicked.connect(lambda: self.closeAll(dialog))
        btnLayout.addWidget(cancelBtn)

        mainLayout.addLayout(btnLayout)
        reply = dialog.exec_()

        def closeEvent(self, event):
            if not self.authenticated:
                event.ignore()

    def errorReport(self, _message):
        message = QtWidgets.QMessageBox()
        message.setText("Error: " + _message)
        message.setIcon(QtWidgets.QMessageBox.Warning)
        message.setStandardButtons(QtWidgets.QMessageBox.Ok)
        message.setWindowFlags(QtCore.Qt.SplashScreen)
        message.exec_()

    def closeAll(self, dialog):
        dialog.close()
        sys.exit()

    def aboutApp(self):
        body = QtWidgets.QDialog()
        body.resize(400, 300)
        body.setWindowFlags(QtCore.Qt.SplashScreen)
        body.setWindowTitle("About RMCO")
        grid = QtWidgets.QVBoxLayout(body)

        label = QtWidgets.QLabel()
        label.setText("<font size=15 color=red>BIOMETRIC ATTENDANCE</font>")
        label.setAlignment(QtCore.Qt.AlignCenter)
        message = QtWidgets.QLabel("This is a biometric attendance app designed to increase the efficiency in taking and generating of attendance and reports for tertiary institutions.")
        message.setWordWrap(True)
        closeBtn = QtWidgets.QPushButton()
        closeBtn.setText("CLOSE")
        closeBtn.clicked.connect(body.close)
        closeBtn.setFixedSize(200, 50)
        grid.addWidget(label)
        grid.addWidget(message)
        grid.addWidget(closeBtn,1, QtCore.Qt.AlignCenter)

        body.exec_()

app = QtWidgets.QApplication(sys.argv)
window = Biometrics()
window.show()
app.exec_()
