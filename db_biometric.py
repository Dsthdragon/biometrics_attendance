#import MySQLdb
import pymysql
import pymysql.cursors
import datetime
import time
import hashlib
import uuid
import os
from random import randint
from PyQt5 import QtWidgets
import sys

class database():
    def __init__(self, parent):
        self.parent = parent
        self.salt = "biometric_hash"


    def createConfig(self, config, dialog):
        sep = os.sep
        newpath = os.getcwd()+""+sep+"data"+sep+"config"+sep+"config.ini"
        empty = 0
        for i in config:
            if config[i].text()  == "" and i != 'password':
                empty = 1
        if empty == 0:
            configFile = open(newpath, "w")
            for i in config:
                configFile.write(i+"="+config[i].text()+"\n")
            configFile.close()
            self.setConfig()
            dialog.close()
        else:
            dialog.close()
            self.parent.newConfig()

    def runConfig(self):
        try:
            self.conn = pymysql.connect( host = self.config['host'], 
                user = self.config['user'],
                password = self.config['password'],
                db = self.config['database'],
                cursorclass =  pymysql.cursors.DictCursor)
            self.cursor = self.conn.cursor()
            self.parent.configSet = 1
            self.general_data = self.get_general()
        except pymysql.MySQLError as e:
            self.parent.errorReport(str(e))
            self.parent.newConfig(self.config)

    def setConfig(self):
        sep = os.sep
        newpath = os.getcwd()+""+sep+"data"+sep+"config"+sep+"config.ini"
        if not os.path.exists(newpath):
            self.parent.newConfig()
        else:
            configFile = open(newpath)
            self.config = {}
            for line in configFile.readlines():
                line = line.rstrip("\n")
                config = line.split("=")
                self.config[config[0]] = config[1]
            configFile.close()
            self.runConfig()

    def get_general(self):
        try:
            self.cursor.execute("SELECT * FROM general_data WHERE id = 1")
            data = self.cursor.fetchone()
            return data
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def update_session_details(self, _data, dialog):
        try:
            data = {}
            data['semester'] =_data['semester'].currentText()
            data['session'] = _data['session'].text()
            if data['semester'] and data['session']:
                self.cursor.execute("UPDATE general_data SET session = '{}', semester = '{}' WHERE id = 1".format(data['session'], data['semester']))
                self.conn.commit()
                self.general_data = self.get_general()
                dialog.close()
                self.parent.admin_class.adminPage()
            else:
                value = 1
                dialog.close()
                self.parent.admin_class.set_session_details(value)
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def bulk_add_student(self, studentsData):
        alreadyRegistered = 0
        registered = 0
        for student in studentsData:
            try:
                self.cursor.execute("SELECT * FROM students WHERE student_regno = '{}'".format(student['student_regno']))
                if self.cursor.fetchone():
                    alreadyRegistered += 1
                else:
                    self.cursor.execute('INSERT INTO  students(student_name, student_gender, student_regno, student_dob, student_state, student_lga, student_address, student_phone, student_email) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(student['student_name'], student['student_gender'], student['student_regno'], student['student_dob'], student['student_state'], student['student_lga'], student['student_address'], student['student_phone'], student['student_email']))
                    self.conn.commit()
                    registered += 1
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))

        value = "<br />Total NO of students registered: {}<br />".format(alreadyRegistered + registered)
        value += "<font color=green>{} student(s) registered.</font><br />".format(registered)
        value += "<font color=red>{} student(s) already in database</font>".format(alreadyRegistered)
        self.parent.student_class.studentsPage(value)


    def add_student(self, studentData, dialog):

        data = {}
        data['name'] = studentData['name'].text()
        data['regno'] = studentData['regno'].text()
        data['gender'] = studentData['gender'].currentText()
        data['dob'] = studentData['dob'].text()

        data['address'] = studentData['address'].text()
        data['phone'] = studentData['phone'].text()
        data['email'] = studentData['email'].text()

        data['state'] = studentData['state'].currentText()
        data['lga'] = studentData['lga'].text()
        if data['name'] and data['regno'] and data['gender'] and data['dob'] and data['address'] and data['phone'] and data['email'] and data['state'] and data['lga']:
            try:
                self.cursor.execute("SELECT * FROM students WHERE student_regno = '{}'".format(data['regno']))
                if self.cursor.fetchone():
                    value = "<br /><font color=red>Student already in database!</font>"
                else:
                    self.cursor.execute('INSERT INTO  students(student_name, student_gender, student_regno, student_dob, student_state, student_lga, student_address, student_phone, student_email) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(data['name'], data['gender'],
                    data['regno'], data['dob'], data['state'], data['lga'], data['address'],
                    data['phone'], data['email']))
                    self.conn.commit()
                    value = "<br /><font color=green>Student has been registered!</font>"
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.student_class.studentsPage(value)

        else:
            value = 1
            dialog.close()
            self.parent.student_class.add_student_dialog(value)

    def edit_student(self, studentData, dialog, default):

        data = {}
        data['id'] = studentData['id']

        data['name'] = studentData['name'].text()
        data['regno'] = studentData['regno'].text()
        data['gender'] = studentData['gender'].currentText()
        data['dob'] = studentData['dob'].text()

        data['address'] = studentData['address'].text()
        data['phone'] = studentData['phone'].text()
        data['email'] = studentData['email'].text()

        data['state'] = studentData['state'].currentText()
        data['lga'] = studentData['lga'].text()

        if data['name'] and data['regno'] and data['gender'] and data['dob']:
            try:
                self.cursor.execute("UPDATE  students SET student_name = '{}', student_gender = '{}', student_regno = '{}',  student_dob = '{}', student_address = '{}', student_phone = '{}', student_email = '{}', student_state = '{}', student_lga = '{}' WHERE student_id = {}".format(data['name'], data['gender'], data['regno'], data['dob'], data['address'], data['phone'], data['email'], data['state'], data['lga'], data['id']))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.student_class.studentsPage(value)

        else:
            value = 1
            dialog.close()
            self.parent.student_class.edit_student_dialog(default, value)

    def add_studentBulkCourse(self, data, course):
        try:
            self.cursor.execute("SELECT * FROM students WHERE student_regno = {}".format(data))
            student = self.cursor.fetchone()
            if student:
                self.cursor.execute("SELECT * FROM course_students WHERE course_id = {} AND student_id = {} AND session = '{}'".format(course['id'], student['student_id'], str(self.general_data['session']) ))
                if len(self.cursor.fetchall()) < 1:
                    self.cursor.execute("INSERT INTO course_students (course_id, student_id, session) VALUES ('{}', '{}', '{}')".format(course['id'], student['student_id'], self.general_data['session']))
                    self.conn.commit()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def add_studentCourse(self, data, dialog, _data):
        try:
            self.cursor.execute("SELECT * FROM course_students WHERE course_id = {} AND student_id = {} AND session = '{}'".format(data['id'], data['student'].currentData(), str(self.general_data['session']) ))
            if len(self.cursor.fetchall()) < 1:
                self.cursor.execute("INSERT INTO course_students (course_id, student_id, session) VALUES ('{}', '{}', '{}')".format(data['id'], data['student'].currentData(), self.general_data['session']))
                self.conn.commit()
                dialog.close()
                self.parent.course_class.viewCoursesPage(_data)
            else:
                dialog.close()
                self.parent.course_class.add_studentConfirm_dialog()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def delete_student(self, studentData, dialog, parent):
        data = {}
        data['id'] = studentData['student_id']
        if data['id']:
            try:
                self.cursor.execute("DELETE FROM students WHERE student_id = {}".format(data['id']))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            parent.close()
            self.parent.student_class.studentsPage(value)

    def get_attendance(self, data):
        try:
            self.cursor.execute("SELECT * FROM attendance_details WHERE course_id = {} AND session = '{}'".format(data, str(self.general_data['session']) ))
            return self.cursor.fetchall()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def get_report(self, data):
        try:
            self.cursor.execute("SELECT * FROM attendance_details WHERE course_id = {} AND session = '{}'".format(data, str(self.general_data['session']) ))
            attendanceList = self.cursor.fetchall()
            total = len(attendanceList)
            self.cursor.execute("SELECT * FROM course_students WHERE course_id = {}".format(data))
            students = []
            for i in self.cursor.fetchall():
                self.cursor.execute("SELECT * FROM students WHERE student_id = '{}'".format(i['student_id']))
                temp = self.cursor.fetchone()
                students.append(temp)

            for student in students:
                present = 0
                for attendance in attendanceList:
                    self.cursor.execute("SELECT * FROM attendance WHERE attendance_id = '{}' AND student_id = '{}'".format(attendance['id'], student['student_id']))
                    for at in self.cursor.fetchall():
                        if at['present'] == 1:
                            present += 1
                student['present'] = present
                student['total'] = total

            return students
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def get_attendance2(self, _id):
        try:
            self.cursor.execute("SELECT * FROM attendance WHERE attendance_id = '{}'".format(_id['id']))
            data = []
            for i in self.cursor.fetchall():
                self.cursor.execute("SELECT * FROM students WHERE student_id = '{}'".format(i['student_id']))
                temp = self.cursor.fetchone()
                temp['present'] = "Absent"
                if  i['present'] == 1:
                    temp['present'] = "Present"
                data.append(temp)
            return data
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def randomGenerate(self, _data):
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
            self.cursor.execute("INSERT INTO attendance_details (`course_id`, `session`, `date`) VALUES ('{}','{}','{}')".format(_data['id'], str(self.general_data['session']), date))
            self.conn.commit()
            _id = self.cursor.lastrowid
            self.cursor.execute("SELECT * FROM course_students WHERE course_id = {}".format(_data['id']))
            newData = self.cursor.fetchall()
            _newData = []
            for row in newData:
                present = 0
                c =randint(1,10)
                if c >= 3:
                    present = 1
                self.cursor.execute("INSERT INTO attendance (attendance_id, student_id, present) VALUES ('{}', '{}', '{}')".format(_id, row['student_id'], present))
                self.conn.commit()
            self.parent.course_class.attendance(_data)
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def generate_attendace(self, data,dialog, _data):
        try:
            date = str(datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
            self.cursor.execute("INSERT INTO attendance_details (`course_id`, `session`, `date`) VALUES ('{}','{}','{}')".format(_data['id'], str(self.general_data['session']), date))
            self.conn.commit()
            _id = self.cursor.lastrowid
            self.cursor.execute("SELECT * FROM course_students WHERE course_id = {}".format(_data['id']))
            newData = self.cursor.fetchall()
            _newData = []
            for row in newData:
                self.cursor.execute("SELECT * FROM students WHERE student_id = {}".format(row['student_id']))
                _newData.append(self.cursor.fetchone())
            for row in _newData:
                present = 0
                if row['student_regno'] in data:
                    present = 1
                self.cursor.execute("INSERT INTO attendance (attendance_id, student_id, present) VALUES ('{}', '{}', '{}')".format(_id, row['student_id'], present))
                self.conn.commit()
            dialog.close()
            self.parent.course_class.attendance(_data)

        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def presents(self, _id):
        try:
            self.cursor.execute("SELECT * FROM attendance WHERE attendance_id = {}".format(_id))

            present = 0
            total = 0
            for i in self.cursor.fetchall():
                if i['present'] == 1:
                    present += 1
                total += 1
            data = {'present': present, 'total':total}
            return data

        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def get_students(self):
        try:
            self.cursor.execute("SELECT * FROM students")
            return self.cursor.fetchall()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def add_course_db(self, courseData, dialog):
        course = {}
        course['title'] = courseData['title'].text()
        course['code'] = courseData['code'].text()
        course['semester'] = courseData['semester'].currentText()
        if course['title'] and course['code'] and course['semester']:
            try:
                self.cursor.execute('INSERT INTO courses(title, code, semester) VALUES ("{}","{}","{}")'.format(course['title'], course['code'], course['semester']))
                self.conn.commit()
                value=0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.course_class.coursesPage(value)
        else:
            value = 1
            dialog.close()
            self.parent.course_class.add_course_dialog(value)

    def edit_course_db(self, courseData, dialog,  default):
        course = {}
        course['id'] = courseData['id']
        course['title'] = courseData['title'].text()
        course['code'] = courseData['code'].text()
        course['semester'] = courseData['semester'].currentText()
        if course['title'] and course['code'] and course['semester']:
            try:
                self.cursor.execute("UPDATE courses SET title = '{}', code = '{}', semester = '{}' WHERE id = {};".format(course['title'], course['code'], course['semester'], course['id']))
                self.conn.commit()
                value=0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.course_class.coursesPage(value)
        else:
            value = 1
            dialog.close()
            self.parent.course_class.edit_course_dialog(default, value)

    def delete_course(self, courseData, dialog, parent):
        data = {}
        data['id'] = courseData['id']
        if data['id']:
            try:
                self.cursor.execute("DELETE FROM courses WHERE id = {}".format(data['id']))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            parent.close()
            self.parent.course_class.coursesPage(value)

    def get_courses(self):
        try:
            self.cursor.execute("SELECT * FROM courses")
            return self.cursor.fetchall()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def get_course_students(self, id):
        try:
            self.cursor.execute("SELECT * FROM course_students WHERE course_id = {} AND session = '{}'".format(id, str(self.general_data['session']) ))
            oldData = self.cursor.fetchall()
            data = []
            for row in oldData:
                self.cursor.execute("SELECT * FROM students WHERE student_id = {}".format(row['student_id']))
                data.append(self.cursor.fetchone())
            return data
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def add_lecturer(self, lecturerData, dialog):
        data = lecturerData.text()
        if data:
            try:
                self.cursor.execute('INSERT INTO lecturers(lecturer_name) VALUES ("{}")'.format(data))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.lecturer_class.teacherPage(value)
        else:
            value = 1
            dialog.close()
            self.parent.lecturer_class.add_teacher_dialog(value)

    def edit_lecturer(self, lecturerData, dialog, default):
        data = {}
        data['id'] = lecturerData['id']
        data['name'] = lecturerData['name'].text()
        if data['name']:
            try:
                self.cursor.execute("UPDATE lecturers SET lecturer_name = '{}' WHERE lecturer_id = {}".format(data['name'], data['id']))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            self.parent.lecturer_class.teacherPage(value)
        else:
            value = 1
            dialog.close()
            self.parent.lecturer_class.edit_teacher_dialog(default, value)

    def delete_lecturer(self, lecturerData, dialog, parent):
        data = {}
        data['id'] = lecturerData['lecturer_id']
        if data['id']:
            try:
                self.cursor.execute("DELETE FROM lecturers WHERE lecturer_id = {}".format(data['id']))
                self.conn.commit()
                value = 0
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
            dialog.close()
            parent.close()
            self.parent.lecturer_class.teacherPage(value)

    def get_lecturers(self):
        try:
            self.cursor.execute("SELECT * FROM lecturers")
            return self.cursor.fetchall()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def add_user(self, data, dialog):
        if data['username'].text() and data['password'].text():
            password = data['password'].text()
            salt_bytes = self.salt.encode('utf-8')
            pass_bytes = password.encode('utf-8')
            final_password = hashlib.sha512(pass_bytes+salt_bytes).hexdigest()
            try:
                self.cursor.execute("INSERT INTO users (username, password) VALUES ('{}', '{}')".format(data['username'].text(), final_password))
                self.conn.commit()
                dialog.close()
                self.parent.admin_class.adminPage()
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
        else:
            value = 1
            dialog.close()
            self.parent.admin_class.add_user_dialog(value)


    def get_user(self):
        try:
            self.cursor.execute("SELECT * FROM users")
            return self.cursor.fetchall()
        except pymysql.DatabaseError as e:
            self.parent.errorReport(str(e))

    def login(self, data):
        
        if data['password']  and data['username']:
            password = data['password']
            salt_bytes = self.salt.encode('utf-8')
            pass_bytes = password.encode('utf-8')
            final_password = hashlib.sha512(pass_bytes+salt_bytes).hexdigest()
            try:
                self.cursor.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(data['username'], final_password))
                _data = self.cursor.fetchone()
                if _data:
                    self.parent.user['login'] = 1
                    self.parent.user['id'] = _data['id']
                    self.parent.user['username'] = _data['username']
                    self.parent.startPage()
                else:
                    self.parent.loginPage(1)
            except pymysql.DatabaseError as e:
                self.parent.errorReport(str(e))
        else:
            self.parent.loginPage(2)

    def change_password(self, data, dialog):
        if data['old'].text() and data['new'].text() and data['confirm'].text():
            if data['new'].text() == data['confirm'].text():
                password = data['new'].text()
                old_password = data['old'].text()
                salt_bytes = self.salt.encode('utf-8')
                pass_bytes = password.encode('utf-8')
                old_pass_bytes = old_password.encode('utf-8')
                final_password = hashlib.sha512(pass_bytes+salt_bytes).hexdigest()
                old_final_password = hashlib.sha512(old_pass_bytes+salt_bytes).hexdigest()
                try:
                    self.cursor.execute("SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(self.parent.user['username'], old_final_password))
                    _data = self.cursor.fetchone()
                    if _data:
                        self.cursor.execute("UPDATE users SET password = '{}'".format(final_password))
                        self.conn.commit()
                        dialog.close()
                        self.parent.successChange()
                    else:
                        dialog.close()
                        value = 3
                        self.parent.changePassword(value)
                except pymysql.DatabaseError as e:
                    self.parent.errorReport(str(e))
            else:
                dialog.close()
                value = 2
                self.parent.changePassword(value)
        else:
            dialog.close()
            value = 1
            self.parent.changePassword(value)
