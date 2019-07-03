from PyQt5 import QtCore, QtGui, QtWidgets
from db import *
from PyQt5.QtSql import*

class Ui_Register(object):

    def closeRegister(self,MainWindow):
        from KU_admin import Ui_MainWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.MainWindow = MainWindow
        self.ui.coverFrame.hide()
        self.window.show()

    def setupUi(self, login):
        login.setObjectName("login")
        login.resize(500, 400)
        # self.model = QSqlTableModel()
        # self.model.setTable("usersTable")
        # self.model.select()

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(34)
        font.setWeight(75)
        font.setItalic(True)

        self.RegisterLabel = QtWidgets.QLabel(login)
        self.RegisterLabel.setGeometry(QtCore.QRect(50, 5, 250, 60))
        self.RegisterLabel.setFont(font)
        self.RegisterLabel.setObjectName("RegisterLabel")
        self.RegisterLabel.setText("Registration")

        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)

        self.notifylabel = QtWidgets.QLabel(login)
        self.notifylabel.setGeometry(QtCore.QRect(30,260,300,30))

        self.LoginUserNameLabel = QtWidgets.QLabel(login)
        self.LoginUserNameLabel.setGeometry(QtCore.QRect(20, 70, 101, 31))
        self.LoginUserNameLabel.setFont(font)
        self.LoginUserNameLabel.setObjectName("LoginUserNameLabel")
        self.LoginUserNameLabel.setText("Username:")
        self.LoginPasswordLabel = QtWidgets.QLabel(login)
        self.LoginPasswordLabel.setGeometry(QtCore.QRect(20, 110, 100, 20))

        self.LoginPasswordLabel.setFont(font)
        self.LoginPasswordLabel.setObjectName("LoginPasswordLabel")
        self.LoginPasswordLabel.setText("Password:")
        self.RegisterSubmitButton = QtWidgets.QPushButton(login)
        self.RegisterSubmitButton.setGeometry(QtCore.QRect(90, 300, 150,50))
        self.RegisterSubmitButton.setObjectName("RegisterSubmitButton")
        self.RegisterSubmitButton.setStyleSheet("font:75 20pt \"Times New Roman\";")
        self.RegisterSubmitButton.setText("Register")
        self.RegisterSubmitButton.clicked.connect(self.check)

        self.RegisterCancelButton = QtWidgets.QPushButton(login)
        self.RegisterCancelButton.setGeometry(QtCore.QRect(270, 300, 150, 50))
        self.RegisterCancelButton.setObjectName("RegisterCancelButton")
        self.RegisterCancelButton.setStyleSheet("font:75 20pt \"Times New Roman\";")
        self.RegisterCancelButton.setText("Cancel")
        self.RegisterCancelButton.clicked.connect(self.closeRegister)
        self.LoginRegistrationLabel = QtWidgets.QLabel(login)
        self.LoginRegistrationLabel.setGeometry(QtCore.QRect(20, 230, 200, 21))

        self.LoginRegistrationLabel.setFont(font)
        self.LoginRegistrationLabel.setObjectName("LoginRegistrationLabel")
        self.LoginRegistrationLabel.setText("Registration No.")
        self.LoginUserTypeLabel = QtWidgets.QLabel(login)
        self.LoginUserTypeLabel.setGeometry(QtCore.QRect(20, 190, 101, 21))

        self.LoginUserTypeLabel.setFont(font)
        self.LoginUserTypeLabel.setObjectName("LoginUserTypeLabel")
        self.LoginUserTypeLabel.setText("Type:")
        self.RegisterTypecomboBox = QtWidgets.QComboBox(login)
        self.RegisterTypecomboBox.setGeometry(QtCore.QRect(200, 190, 69, 22))
        self.RegisterTypecomboBox.setObjectName("RegisterTypecomboBox")
        self.RegisterTypecomboBox.addItem("User")
        self.RegisterTypecomboBox.addItem("Admin")
        self.LoginCPasswordLabel = QtWidgets.QLabel(login)
        self.LoginCPasswordLabel.setGeometry(QtCore.QRect(20, 150, 171, 21))

        self.LoginCPasswordLabel.setFont(font)
        self.LoginCPasswordLabel.setObjectName("LoginCPasswordLabel")
        self.LoginCPasswordLabel.setText("Confirm Password:")

        self.RegisterUsernameInput = QtWidgets.QLineEdit(login)
        self.RegisterUsernameInput.setGeometry(QtCore.QRect(200, 69, 191, 31))
        self.RegisterUsernameInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.RegisterUsernameInput.setObjectName("RegisterUsernameInput")
        self.RegisterPasswordInput = QtWidgets.QLineEdit(login)
        self.RegisterPasswordInput.setGeometry(QtCore.QRect(200, 110, 191, 31))
        self.RegisterPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RegisterPasswordInput.setObjectName("RegisterPasswordInput")
        self.RegisterCPasswordInput = QtWidgets.QLineEdit(login)
        self.RegisterCPasswordInput.setGeometry(QtCore.QRect(200, 150, 191, 31))
        self.RegisterCPasswordInput.setEchoMode(QtWidgets.QLineEdit.Password)
        self.RegisterCPasswordInput.setObjectName("RegisterCPasswordInput")
        self.RegistrationInput = QtWidgets.QLineEdit(login)
        self.RegistrationInput.setGeometry(QtCore.QRect(200, 220, 191, 31))
        self.RegistrationInput.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.RegistrationInput.setObjectName("RegistrationInput")

        self.notifylabel.setStyleSheet("QLabel {font-size:15pt; color:red;}")

        QtCore.QMetaObject.connectSlotsByName(login)

    def close(self):
        sys.exit()
    def check(self):
        checker=[]
        if self.RegisterUsernameInput.text() == "" or self.RegisterPasswordInput.text() == "" or self.RegistrationInput.text() == "":
             self.notifylabel.setText("Please fill all fields")
        else:
            query = QSqlQuery()
            count = 0
            query.exec_("SELECT username FROM usersTable")
            while (query.next()):
                name = query.value(0)
                checker.append(name)
            print(checker)
            n = len(checker)
            print(n)
            for i in range(n):
                if self.RegisterUsernameInput.text() == checker[i]:
                    count =+ 1
            if count == 0:
                self.registerUsers()
            else:
                print("Username already taken")
                self.notifylabel.setText("Username already taken")

    def registerUsers(self):
        users_model = QSqlTableModel()
        users_model.setTable("usersTable")
        users_model.select()
        record = users_model.record()
        if self.RegisterPasswordInput.text() == self.RegisterCPasswordInput.text():
            record.setValue("username", self.RegisterUsernameInput.text() )
            record.setValue("password", self.RegisterPasswordInput.text())
            record.setValue("post", self.RegisterTypecomboBox.currentText())
            record.setValue("registration_no", self.RegistrationInput.text())
            print("Users created")
            self.RegisterUsernameInput.clear()
            self.RegisterPasswordInput.clear()
            self.RegisterCPasswordInput.clear()
            self.RegistrationInput.clear()
        else:
            self.notifylabel.setText("Passwords does not match")
            print("Passwords does not match")
            self.RegisterPasswordInput.clear()
            self.RegisterCPasswordInput.clear()
            self.RegistrationInput.clear()

        if users_model.insertRecord(-1, record):
            users_model.select()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)
    login = QtWidgets.QDialog()
    ui = Ui_Register()
    ui.setupUi(login)
    login.show()
    sys.exit(app.exec_())
