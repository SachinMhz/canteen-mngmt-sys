import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import*
import os
from functools import partial
#import from the user files
from db import *

width,height=1300,700
oneUnit = (width+height)/100
# currentBalance = 500
PROJECT_FOLDER = os.path.dirname(__file__)
IMAGE_FOLDER = os.path.join(PROJECT_FOLDER , "image")

class MainInterface(object):
    def openAdminWindow(self,MainWindow):
        from KU_admin import Ui_MainWindow
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        MainWindow.close()
        self.MainWindow = MainWindow
        self.ui.userName = self.userName
        self.ui.registrationNo = self.registrationNo
        self.ui.currentBalance =self.currentBalance
        self.window.show()
        self.ui.userNameText.setText(str(self.userName))
        self.ui.regNoText.setText(str(self.registrationNo))

    def setupUi(self, MainWindow):
        # ---------Window settings --------------------------------
        #initialization
        self.userName = 0
        self.registrationNo = 0
        self.remainingBalance = 0
        self.currentBalance = 500
        self.totalCost = 0
        self.MainWindow = MainWindow
        MainWindow.setWindowTitle("KU Canteen Management System")
        MainWindow.showFullScreen()
        #//for using in full screen
        width,height= MainWindow.frameGeometry().width(),MainWindow.frameGeometry().height()
        self.width,self.height = MainWindow.frameGeometry().width(),MainWindow.frameGeometry().height()
        #---------content that are displayed in window
        self.centralwidget = QtWidgets.QWidget(MainWindow)

        self.userInfoArea = QtWidgets.QFrame(self.centralwidget)
        self.userInfoFrame()

        self.balanceFrame_bottomRight()
        self.billingArea = QtWidgets.QFrame(self.centralwidget)
        self.makeFrame(self.billingArea,"billingArea",width*.7 , height*.15 + 50, width*.3 -2, height*.65 -1-50)

        self.billHeadingFrame = QtWidgets.QFrame(self.centralwidget)
        self.makeFrame(self.billHeadingFrame,"billHeadingFrame",width*.7 , height*.15, width*.3 -2,48)
        self.billHeadingFrame.setStyleSheet("background-color: #00007f;")

        self.itemNameLabel = QtWidgets.QLabel("Item Name",self.billHeadingFrame)
        self.itemNameLabel.setGeometry(QtCore.QRect(15,1 , 100, 50))
        self.itemNameLabel.setStyleSheet("font:90 13pt \"Times New Roman\"; color:white; font-weight:600;")
        self.itemPrice = QtWidgets.QLabel("Price",self.billHeadingFrame)
        self.itemPrice.setGeometry(QtCore.QRect(135, 1, 100, 50))
        self.itemPrice.setStyleSheet("font:90 13pt \"Times New Roman\"; color:white; font-weight:600;")
        self.itemQuantity = QtWidgets.QLabel("Quantity",self.billHeadingFrame)
        self.itemQuantity.setGeometry(QtCore.QRect(210, 1, 100, 50))
        self.itemQuantity.setStyleSheet("font:90 13pt \"Times New Roman\"; color:white; font-weight:600;")
        self.itemAmount = QtWidgets.QLabel("Amount",self.billHeadingFrame)
        self.itemAmount.setGeometry(QtCore.QRect(300, 1, 100, 50))
        self.itemAmount.setStyleSheet("font:90 13pt \"Times New Roman\"; color:white; font-weight:600;")

        self.mainArea = QtWidgets.QFrame(self.centralwidget)
        self.makeFrame(self.mainArea,"mainArea",1, height*.15 +1, width*.7 -2, height*.85 -2)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(2, height*.15 +2, width*.7 -3, height*.85 -3))
        self.tabWidget.setObjectName("self.tabWidget")
        self.tabWidget.setStyleSheet(" font:150 25pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.lunchTab = QtWidgets.QWidget()
        self.lunchTab.setObjectName("lunchTab")
        self.lunchTab.setStyleSheet("font:150 15pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.tabWidget.addTab(self.lunchTab, "Lunch/Snacks")
        self.drinkTab = QtWidgets.QWidget()
        self.drinkTab.setObjectName("drinkTab")
        self.drinkTab.setStyleSheet("font:150 15pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.tabWidget.addTab(self.drinkTab, "Drinks")

        self.billLayoutWidget = QtWidgets.QWidget(self.billingArea)
        self.billLayoutWidget.setGeometry(QtCore.QRect(5,5, 370, 440))
        self.billLayoutWidget.setObjectName("billLayoutWidget")
        self.billLayout = QtWidgets.QVBoxLayout(self.billLayoutWidget)
        self.billLayout.setContentsMargins(0, 0, 0, 0)
        self.billLayout.setObjectName("billLayout")
        self.billLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.billLayout.setSpacing(2)

        #showing Bill labels
        self.billHeadingFrame_topRight()
        #showingImage function contains images arranged in grid format
        self.showingImage2()
        #checking for balance
        self.showBalanceInfoAndDisableButton()
        #For Yes NO window confirm Bill
        self.confirmBillWindow()
        #for success Transactions
        self.successWindowWidget = QtWidgets.QWidget(self.centralwidget)
        self.completeLabel = QtWidgets.QLabel(self.successWindowWidget)
        self._gif = QtWidgets.QLabel(self.successWindowWidget)
        self.menuFrame = QtWidgets.QFrame(self.centralwidget)
        self.makeMenuFrame()
        #for login Window
        self.showLoginWindow()
        MainWindow.setCentralWidget(self.centralwidget)
        self.paybillBtn.clicked.connect(self.showConfirmBillWindow)

    def userInfoFrame(self):
        font = QtGui.QFont("Times New Roman", 15)
        self.makeFrame(self.userInfoArea,"userInfoArea",1,1,self.width*.7 -2, self.height*.15 -2)
        self.userNameLabel = QtWidgets.QLabel("Username: ",self.userInfoArea)
        self.userNameLabel.setGeometry(QtCore.QRect(5,50,150,50))
        self.userNameLabel.setFont(font)
        self.userNameLabel.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.userNameText = QtWidgets.QLabel(self.userInfoArea)
        self.userNameText.setGeometry(QtCore.QRect(150,50,300,50))
        self.userNameText.setFont(font)
        self.userNameText.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.regLabel = QtWidgets.QLabel("Registration No.: ",self.userInfoArea)
        self.regLabel.setGeometry(QtCore.QRect(450,50,250,50))
        self.regLabel.setFont(font)
        self.regLabel.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.regNoText = QtWidgets.QLabel(self.userInfoArea)
        self.regNoText.setGeometry(QtCore.QRect(675,50,300,50))
        self.regNoText.setFont(font)
        self.regNoText.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

    def makeMenuFrame(self):
        self.makeFrame(self.menuFrame,"menuFrame",0,0,self.width ,52)
        self.menuFrame.setStyleSheet("background-color: #00007f;")

        self.menuLabel = QtWidgets.QLabel("Canteen Management System ",self.menuFrame)
        self.menuLabel.setGeometry(QtCore.QRect(0, -1, self.width,50))
        self.menuLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.menuLabel.setStyleSheet("font:150 35pt \"Times New Roman\"; color:white;")

        self.AdminButton = QtWidgets.QPushButton("Admin",self.menuFrame)
        self.AdminButton.setGeometry(QtCore.QRect(self.width-315,3,100,45))
        self.AdminButton.clicked.connect(partial(self.openAdminWindow,self.MainWindow))
        self.AdminButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")

        self.helpButton = QtWidgets.QPushButton("Help",self.menuFrame)
        self.helpButton.setGeometry(QtCore.QRect(self.width-210,3,100,45))
        self.helpButton.clicked.connect(self.showHelp)
        self.helpButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")

        exitButton = QtWidgets.QPushButton("Exit",self.menuFrame)
        exitButton.setGeometry(QtCore.QRect(self.width-105,3,100,45))
        exitButton.clicked.connect(self.showLoginWindow)
        exitButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")
        self.helpLabel = QtWidgets.QLabel(self.centralwidget)
        self.helpLabel.hide()
        self.closeButton = QtWidgets.QPushButton("Close",self.centralwidget)
        self.closeButton.hide()


    def showHelp(self):
        pixmap = QPixmap("image/help.png")
        self.helpLabel.setPixmap(pixmap.scaled(self.width,self.height))
        self.helpLabel.show()
        self.closeButton.setGeometry(QtCore.QRect(self.width-105,3,100,45))
        self.closeButton.clicked.connect(self.hideHelp)
        self.closeButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")
        self.closeButton.show()

    def hideHelp(self):
        self.helpLabel.hide()
        self.closeButton.hide()

    def showLoginWindow(self):
        self.loginWindowWidget = QtWidgets.QWidget(self.centralwidget)
        self.loginWindowWidget.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.loginWindowWidget.setObjectName("loginWindowWidget")
        self.loginWindowWidget.setStyleSheet("background-color: #E9B872;")

        #adding image to label
        self.imageLabel = QtWidgets.QLabel(self.loginWindowWidget)
        pixmap = QPixmap("image/bg3.jpg")
        self.imageLabel.setPixmap(pixmap.scaled(self.width,self.height))

        #layout for Login Window
        testframe = QtWidgets.QFrame(self.loginWindowWidget)
        login = QtWidgets.QFrame(self.loginWindowWidget)
        self.makeFrame(testframe,"testframe",self.width/2-210 ,self.height/2-160,420, 320)
        self.makeFrame(login,"LoginFrame",self.width/2-200 ,self.height/2-150,400, 300)
        testframe.setStyleSheet("background-color: #bc7556;")
        login.setStyleSheet("background-color: #bc856c;")

        self.noticelogin = QtWidgets.QLabel(login)
        self.noticelogin.setGeometry(QtCore.QRect(60, 200,300,40))

        self.LoginButton = QtWidgets.QPushButton(login)
        self.LoginButton.setGeometry(QtCore.QRect(40, 245, 150, 40))
        self.LoginButton.setObjectName("LoginButton")
        self.LoginButton.setStyleSheet("*{border: 2px solid #694a19; border-radius: 5px; background-color: #bc856c; font:75 20pt \"Times New Roman\"; font-weight:600;}"
                            ":hover{border: 2px solid #bd7a11; border-radius: 5px;}"
                                ":pressed{border: 2px solid #694a19; border-radius: 5px; background-color: #8a6324; color:black;}")
        self.LoginButton.clicked.connect(self.login)

        self.LoginUserNameLabel = QtWidgets.QLabel(login)
        self.LoginUserNameLabel.setStyleSheet("font:65 15pt \"Times New Roman\";")
        self.LoginUserNameLabel.setGeometry(QtCore.QRect(10, 85, 150, 30))
        self.LoginUserNameLabel.setObjectName("LoginUserNameLabel")
        self.LoginUserNameLabel.setStyleSheet("font:65 15pt \"Times New Roman\"; font-weight:600;")
        self.LoginPasswordLabel = QtWidgets.QLabel(login)
        self.LoginPasswordLabel.setGeometry(QtCore.QRect(10, 155, 150, 30))
        self.LoginPasswordLabel.setStyleSheet("font:65 15pt \"Times New Roman\"; font-weight:600;")
        self.LoginPasswordLabel.setObjectName("LoginPasswordLabel")

        self.LoginCancelButton = QtWidgets.QPushButton(login)
        self.LoginCancelButton.setGeometry(QtCore.QRect(210, 245,150,40))
        self.LoginCancelButton.setObjectName("LoginCancelButton")
        self.LoginCancelButton.setStyleSheet("*{border: 2px solid #694a19; border-radius: 5px; background-color: #bc856c; font:75 20pt \"Times New Roman\"; font-weight:600;}"
                            ":hover{border: 2px solid #bd7a11; border-radius: 5px;}"
                                ":pressed{border: 2px solid #694a19; border-radius: 5px; background-color: #8a6324; color:black;}")
        self.LoginCancelButton.clicked.connect(sys.exit)

        self.LoginUserNameLabel_2 = QtWidgets.QLabel(login)
        self.LoginUserNameLabel_2.setGeometry(QtCore.QRect(30, 10, 220, 40))
        self.LoginUserNameLabel_2.setStyleSheet("font:75 25pt \"Times New Roman\";")
        self.LoginUserNameLabel_2.setObjectName("LoginUserNameLabel_2")
        self.registration_lineedit = QtWidgets.QLineEdit(login)
        self.registration_lineedit.setGeometry(QtCore.QRect(160, 80, 200, 40))
        self.registration_lineedit.setObjectName("registration_lineedit")
        self.password_lineedit = QtWidgets.QLineEdit(login)
        self.password_lineedit.setGeometry(QtCore.QRect(160, 150, 200, 40))
        self.password_lineedit.setObjectName("password_lineedit")
        self.password_lineedit.setEchoMode(QtWidgets.QLineEdit.Password)

        self.LoginButton.setText( "Login")
        self.LoginUserNameLabel.setText("Registration No:")
        self.LoginPasswordLabel.setText("Password:")
        self.LoginCancelButton.setText("Cancel")
        self.LoginUserNameLabel_2.setText("Log In:")

        font = QtGui.QFont("Times New Roman", 15)
        self.registration_lineedit.setFont(font)
        self.password_lineedit.setFont(font)
        """
        self.tempbutton = QtWidgets.QPushButton("hide Login", login)
        self.tempbutton.setGeometry(QtCore.QRect(220,40,100,30))
        self.tempbutton.clicked.connect(self.goToMainInterface)
        """
        self.loginWindowWidget.show()

    def goToMainInterface(self):
        self.clearLayout(self.billLayout)
        self.showBalanceInfoAndDisableButton()
        self.removeHighLight()
        self.totalCost = 0
        self.remainingBalance = self.currentBalance
        self.loginWindowWidget.hide()
        self.confirmBillWidget.hide()

    def login(self):
        query = QSqlQuery()
        query.exec_("SELECT username,password,post,balance,registration_no FROM usersTable")
        username_list = []
        password_list = []
        post_list = []
        currentBalance_list = []
        registration_list = []

        while (query.next()):
            #0=username 1=password 2=post 3=balance 4=registration_no
            name = query.value(0)
            username_list.append(name)
            password = query.value(1)
            post = query.value(2)
            password_list.append(password)
            post_list.append(post)
            currentbalance = query.value(3)
            currentBalance_list.append(currentbalance)
            registrationNo = str(query.value(4))
            registration_list.append(registrationNo)
        RegistrationNo = self.registration_lineedit.text()
        passWord = self.password_lineedit.text()

        if RegistrationNo !="" and passWord != "":
            if RegistrationNo in registration_list:
                index = registration_list.index(RegistrationNo)
                if str(password_list[index]) == passWord:
                    print("password matched")
                    self.goToMainInterface()
                    self.userPosition = post_list[index]
                    if self.userPosition != "Admin":
                        self.AdminButton.hide()
                    else:
                        self.AdminButton.show()
                    self.userNameText.setText(str(username_list[index]))
                    self.regNoText.setText(str(RegistrationNo))
                    self.currentBalance = int(currentBalance_list[index])
                    self.remainingBalance = self.currentBalance
                    self.showBalanceInfoAndDisableButton()
                    self.userName = str(username_list[index])
                    self.registrationNo = str(registration_list[index])
                else:
                    self.noticelogin.setText("Password does not match.")
                    self.noticelogin.setStyleSheet("font:65 14pt \"Times New Roman\"; color:#a81010; font-weight:600")
            else:
                self.noticelogin.setText("User does not exist")
                self.noticelogin.setStyleSheet("font:65 14pt \"Times New Roman\"; color:#a81010; font-weight:600")
        else:
            self.noticelogin.setText("Fields are empty.")
            self.noticelogin.setStyleSheet("font:65 14pt \"Times New Roman\"; color:#a81010; font-weight:600")

    def showSuccessTransaction(self):
        self.successWindowWidget.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.successWindowWidget.setObjectName("loginWindowWidget")
        self.successWindowWidget.setStyleSheet("background-color: white;")

        self.completeLabel.setGeometry(QtCore.QRect(0, 100, 1300,150))
        self.completeLabel.setText("Transaction Successful")
        self.completeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.completeLabel.setStyleSheet("QLabel {font-size:30pt; font-weight:600; color: black;}")

        self._gif.setGeometry(QtCore.QRect(self.width/2-150,self.height/2-150, 500,500))
        movie = QtGui.QMovie("image/check-circle.gif")
        self._gif.setMovie(movie)
        movie.start()
        QtCore.QTimer.singleShot(2200, self.hideSuccessTransaction)

    def hideSuccessTransaction(self):
        self.successWindowWidget.hide()
        self.confirmBillLayoutWidget.hide()
        self.loginWindowWidget.show()
        query = QSqlQuery()
        query.exec_("UPDATE usersTable SET balance = "+str(self.remainingBalance)+" WHERE registration_no = "+self.registration_lineedit.text()+"")
        self.setupUi(self.MainWindow)
        self.MainWindow.show()

    def confirmBillWindow(self):
        self.confirmBillWidget = QtWidgets.QWidget(self.centralwidget)
        self.confirmBillWidget.setGeometry(QtCore.QRect(0, 0, self.width, self.height))
        self.confirmBillWidget.setObjectName("confirmBillWidget")
        self.confirmBillWidget.setStyleSheet("background-color: white;")
        #layout for confirm Bill
        self.confirmBillFrame = QtWidgets.QFrame(self.confirmBillWidget)
        self.makeFrame(self.confirmBillFrame,"confirmBillFrame",self.width/2-250 ,self.height/2-250,500, 350)
        self.confirmBillLayoutWidget = QtWidgets.QWidget(self.confirmBillFrame)
        self.confirmBillLayoutWidget.setGeometry(QtCore.QRect(5,5, 370, 440))
        self.confirmBillLayoutWidget.setObjectName("billLayoutWidget")
        self.confirmBillLayout = QtWidgets.QVBoxLayout(self.confirmBillLayoutWidget)
        self.confirmBillLayout.setContentsMargins(0, 0, 0, 0)
        self.confirmBillLayout.setObjectName("billLayout")
        self.confirmBillLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.confirmBillLayout.setSpacing(2)

        #for confirm bill table heading
        self.confirmBillHeadingFrame = QtWidgets.QFrame(self.confirmBillWidget)
        self.makeFrame(self.confirmBillHeadingFrame,"confirmBillHeadingFrame",self.width/2-250 ,self.height/2-300,500, 50)
        self.confirmBillHeadingFrame.setStyleSheet("background-color: #99deb5; ")
        self.itemNameLabel = QtWidgets.QLabel("Item Name",self.confirmBillHeadingFrame)
        self.itemNameLabel.setStyleSheet("font:65 18pt \"Times New Roman\";")
        self.itemNameLabel.setGeometry(QtCore.QRect(20, 10, 120, 30))
        self.itemPrice = QtWidgets.QLabel("Rate",self.confirmBillHeadingFrame)
        self.itemPrice.setStyleSheet("font:65 18pt \"Times New Roman\";")
        self.itemPrice.setGeometry(QtCore.QRect(180, 10, 90, 30))
        self.itemQuantity = QtWidgets.QLabel("Quantity",self.confirmBillHeadingFrame)
        self.itemQuantity.setStyleSheet("font:65 18pt \"Times New Roman\";")
        self.itemQuantity.setGeometry(QtCore.QRect(270, 10, 90, 30))
        self.itemAmount = QtWidgets.QLabel("Amount",self.confirmBillHeadingFrame)
        self.itemAmount.setStyleSheet("font:65 18pt \"Times New Roman\";")
        self.itemAmount.setGeometry(QtCore.QRect(400, 10, 90, 30))

        self.priceLabelConfirmBill = QtWidgets.QLabel("Rs. "+str(self.totalCost)+" will be deducted from your balance.",self.confirmBillWidget)
        self.priceLabelConfirmBill.setGeometry(QtCore.QRect(self.width/2-300, self.height-2.1*self.height/6, 1000, 50))
        self.priceLabelConfirmBill.setStyleSheet("QLabel {font-size:20pt; font-weight:500; color:red;}")
        self.warnLabelConfirmBill = QtWidgets.QLabel("Are you sure you want to confirm this bill?",self.confirmBillWidget)
        self.warnLabelConfirmBill.setGeometry(QtCore.QRect(self.width/2-200, self.height-1.75*self.height/6, 1000, 50))
        self.warnLabelConfirmBill.setStyleSheet("QLabel {font-size:15pt; font-weight:400; color:black;}")

        self.yesBtnConfirmBill = QtWidgets.QPushButton("Yes", self.confirmBillWidget)
        self.yesBtnConfirmBill.setGeometry(QtCore.QRect(self.width/2-175, self.height/2+230, 150, 50))
        self.yesBtnConfirmBill.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #99deb5; font:65 20pt \"Times New Roman\"; font-weight:600;}"
                            ":hover{border: 2px solid green; border-radius: 5px;}"
                                ":pressed{border: 2px solid grey; border-radius: 5px; background-color: #5ddeaa; color:black;}")
        self.yesBtnConfirmBill.clicked.connect(self.showSuccessTransaction)
        #self.yesBtnConfirmBill.setStyleSheet("border : 1px solid black;")

        self.noBtnConfirmBill = QtWidgets.QPushButton("No", self.confirmBillWidget)
        self.noBtnConfirmBill.setGeometry(QtCore.QRect(self.width/2+25, self.height/2+230, 150, 50))
        self.noBtnConfirmBill.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #99deb5; font:65 20pt \"Times New Roman\"; font-weight:600;}"
                            ":hover{border: 2px solid green; border-radius: 5px;}"
                                ":pressed{border: 2px solid grey; border-radius: 5px; background-color: #5ddeaa; color:black;}")
        self.noBtnConfirmBill.clicked.connect(self.noClicked)
        #self.noBtnConfirmBill.setStyleSheet("border : 1px solid black;")
        self.confirmBillWidget.hide()

    def noClicked(self):
        self.confirmBillWidget.hide()
        self.clearLayout(self.confirmBillLayout)

    def clearLayout(self,layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def showConfirmBillWindow(self):
        self.confirmBillWidget.show()
        self.priceLabelConfirmBill.setText("Rs. "+str(self.totalCost)+" will be deducted from your balance.")

        frameList = self.getFrameList()
        #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
        for frame in frameList:
            foodName , foodPrice,foodQuantity,foodAmount =frame[1].text(),frame[2].text(),frame[3].text(),frame[4].text()
            frame = QtWidgets.QFrame(self.confirmBillLayoutWidget)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            frame.setSizePolicy(sizePolicy)
            frame.setMinimumSize(QtCore.QSize(475,40))
            frame.setGeometry(QtCore.QRect(0, 0, 475, 40))
            foodLabel = QtWidgets.QLabel(foodName,frame)
            foodLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            foodLabel.setGeometry(QtCore.QRect(20, 10, 300, 30))
            rupeePriceLabel = QtWidgets.QLabel("Rs.",frame)
            rupeePriceLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            rupeePriceLabel.setGeometry(QtCore.QRect(175, 10, 25, 30))
            rupeeAmountLabel = QtWidgets.QLabel("Rs.",frame)
            rupeeAmountLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            rupeeAmountLabel.setGeometry(QtCore.QRect(400, 10, 25, 30))
            priceLabel = QtWidgets.QLabel(foodPrice,frame)
            priceLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            priceLabel.setGeometry(QtCore.QRect(200, 10, 150, 30))
            quantityLabel = QtWidgets.QLabel(foodQuantity,frame)
            quantityLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            quantityLabel.setGeometry(QtCore.QRect(300, 10, 50, 30))
            amountLabel = QtWidgets.QLabel(foodAmount,frame)
            amountLabel.setStyleSheet("font:65 16pt \"Times New Roman\";")
            amountLabel.setGeometry(QtCore.QRect(430, 10, 150, 30))
            self.confirmBillLayout.addWidget(frame)

    def balanceFrame_bottomRight(self):
        self.mainRightButtom = QtWidgets.QFrame(self.centralwidget)
        self.makeFrame(self.mainRightButtom,"mainRightButtom",self.width*.7, self.height*.8, self.width*.3 -2 , self.height*.2-2)

        self.currentBalanceLabel = QtWidgets.QLabel("Current Balance " ,self.mainRightButtom)
        self.currentBalanceLabel.setGeometry(QtCore.QRect(10, 10, 200, 50))
        self.currentBalanceLabel.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:#00007f;}")

        self.currentBalanceAmount = QtWidgets.QLabel(self.mainRightButtom)
        self.currentBalanceAmount.setGeometry(QtCore.QRect(210, 10, 100, 50))
        self.currentBalanceAmount.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:#00007f;}")

        self.totalCostLabel = QtWidgets.QLabel("Total Cost" ,self.mainRightButtom)
        self.totalCostLabel.setGeometry(QtCore.QRect(10, 50, 100, 50))
        self.totalCostLabel.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:red;}")

        self.totalCostAmount = QtWidgets.QLabel("Rs. 0" ,self.mainRightButtom)
        self.totalCostAmount.setGeometry(QtCore.QRect(210, 50, 100, 50))
        self.totalCostAmount.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:red;}")

        self.remainingBalanceLabel = QtWidgets.QLabel("Remaining Balance " ,self.mainRightButtom)
        self.remainingBalanceLabel.setGeometry(QtCore.QRect(10, 90, 200, 50))
        self.remainingBalanceLabel.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:#00007f;}")

        self.remainingBalanceAmount = QtWidgets.QLabel(self.mainRightButtom)
        self.remainingBalanceAmount.setGeometry(QtCore.QRect(210, 90, 100, 50))
        self.remainingBalanceAmount.setStyleSheet("QLabel {font-size:14pt; font-weight:600; color:#00007f;}")

        self.paybillBtn = QtWidgets.QPushButton("Pay Bill",self.mainRightButtom)
        self.paybillBtn.setGeometry(QtCore.QRect(300,oneUnit,100,100))
        self.paybillBtn.setStyleSheet("font-size:15pt; font-weight:600;")
        if self.totalCost == 0:
            self.paybillBtn.setEnabled(False)
            self.paybillBtn.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; font-size:15pt; font-weight:600; font-size:15pt; font-weight:600;}")

    def Add(self):
        source = self.MainWindow.sender()
        objName = source.objectName()
        source.quantity += 1

        #creating a list of frames in lucnhTab
        framesLunch = self.lunchTab.findChildren(QtWidgets.QFrame)
        framesDrink = self.drinkTab.findChildren(QtWidgets.QFrame)
        frames = framesLunch + framesDrink
        #higlighting the selected foodFrame
        for frame in frames:
            if frame.objectName() == source.frame:
                frame.setStyleSheet("#"+frame.objectName()+ " {border : 3px solid blue;}" "#"+frame.objectName()+":hover{border: 2px solid green; border-radius: 5px;}")
                break

        #checking to see if bill has items or not
        labels = self.billLayoutWidget.findChildren(QtWidgets.QLabel)
        if labels != None :
            frameList = self.getFrameList()
            #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
            for frame in frameList:
                for item in frame:
                    if item.objectName() == objName +"foodLabel":
                        incQuantity = int(frame[3].text()) + 1
                        frame[3].setText(str(incQuantity))
                        incAmount = int(frame[4].text()) +int(frame[2].text()) #currentAmount + Price
                        frame[4].setText(str(incAmount))
                        self.showBalanceInfoAndDisableButton() #to update the balance Info if billLayout already have item
                        return
        #adding frames to the billing area if not already present
        frame = QtWidgets.QFrame(self.billLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed,QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(frame.sizePolicy().hasHeightForWidth())
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        frame.setSizePolicy(sizePolicy)
        frame.setMinimumSize(QtCore.QSize(400-2 ,40))
        frame.setGeometry(QtCore.QRect(0, 0,  self.width*.3 +50 , 30))
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Plain)
        frame.setObjectName(objName +"Frame")
        frame.setStyleSheet("border: 2px solid grey; border-radius: 5px;")

        minusButton = QtWidgets.QPushButton("-",frame)
        minusButton.setObjectName(objName +"minusButton")
        minusButton.setGeometry(QtCore.QRect(200-5, 5, 30, 30))
        minusButton.clicked.connect(self.DecQuantity)
        minusButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; font-size:14pt; font-weight:1000; color:#f24d0c;}"
                                ":hover{border: 2px solid #f24d0c; border-radius: 5px; color:#f24d0c;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#f24d0c; color:white;}")

        plus2Button = QtWidgets.QPushButton("u",frame) #plus2Button is not required delete garyo vane plus button chaldaina idk why
        plus2Button.hide()

        plusButton = QtWidgets.QPushButton("+",frame)
        plusButton.setGeometry(QtCore.QRect(250, 5, 30, 30))
        plusButton.setObjectName(objName +"plusButton")
        plusButton.clicked.connect(self.IncQuantity)
        plusButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px;  font-size:13pt; font-weight:1000; color:green;}"
                                ":hover{border: 2px solid green; border-radius: 5px; color:green;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:green; color:white;}")


        deleteButton = QtWidgets.QPushButton("x",frame)
        deleteButton.setGeometry(QtCore.QRect(400 - 40, 5, 30, 30))
        deleteButton.setObjectName(objName +"deleteButton")
        deleteButton.clicked.connect(self.deleteFrame)
        deleteButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; font-size:12pt; font-weight:600; color:red;}"
                                ":hover{border: 2px solid red; border-radius: 5px; color:red;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:red; color:white;}")
        foodLabel = QtWidgets.QLabel(str(source.disName),frame)
        foodLabel.setGeometry(QtCore.QRect(10, 10, 100, 20))
        foodLabel.setObjectName(objName +"foodLabel")
        foodLabel.setStyleSheet("border: 0px; font-size:10pt; font-weight:600; color:black;")
        priceLabel = QtWidgets.QLabel(str(source.price),frame)
        priceLabel.setGeometry(QtCore.QRect(150, 10, 100, 15))
        priceLabel.setObjectName(objName +"priceLabel")
        priceLabel.setStyleSheet("border: 0px;  font-size:10pt; font-weight:600; color:black;")
        quantityLabel = QtWidgets.QLabel(str(source.quantity),frame)
        quantityLabel.setGeometry(QtCore.QRect(230, 10, 16, 15))
        quantityLabel.setObjectName(objName +"quantityLabel")
        quantityLabel.setStyleSheet("border: 0px; font-size:10pt; font-weight:600; color:black;")
        amountLabel = QtWidgets.QLabel(str(source.amount),frame)
        amountLabel.setGeometry(QtCore.QRect(330, 10, 100, 15))
        amountLabel.setObjectName(objName +"Amount")
        amountLabel.setStyleSheet("border: 0px; font-size:10pt; font-weight:600; color:black;")
        rupeePriceLabel = QtWidgets.QLabel("Rs ",frame)
        rupeePriceLabel.setGeometry(QtCore.QRect(130, 10, 100, 15))
        rupeePriceLabel.setObjectName(objName +"RsPrice")
        rupeePriceLabel.setStyleSheet("border: 0px; font-size:10pt; font-weight:600; color:black;")
        rupeeAmountLabel = QtWidgets.QLabel("Rs ",frame)
        rupeeAmountLabel.setGeometry(QtCore.QRect(310, 10, 100, 15))
        rupeeAmountLabel.setObjectName(objName +"RsAmount")
        rupeeAmountLabel.setStyleSheet("border: 0px; font-size:10pt; font-weight:600; color:black;")

        self.showBalanceInfoAndDisableButton() #to update the balance Info if billLayout doesnt already have item
        self.billLayout.addWidget(frame)

    def billHeadingFrame_topRight(self):
        self.mainRightTop = QtWidgets.QFrame(self.centralwidget)
        self.makeFrame(self.mainRightTop,"mainRightTop",self.width*.7, 1, self.width*.3 -2 , self.height*.15-2)

        self.yourBillLabel = QtWidgets.QLabel(self.mainRightTop)
        self.yourBillLabel.setText("Your Bill:")
        self.yourBillLabel.setGeometry(QtCore.QRect(50, 55, 200, 50))
        self.yourBillLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.yourBillLabel.setStyleSheet("QLabel {font-size:25pt; font-weight:600; color:#00007f;}")

        self.billTotalCostLabel = QtWidgets.QLabel(self.mainRightTop)
        self.billTotalCostLabel.setText("Rs. 0")
        self.billTotalCostLabel.setGeometry(QtCore.QRect(200, 55, 200, 50))
        self.billTotalCostLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.billTotalCostLabel.setStyleSheet("QLabel {font-size:25pt; font-weight:600; color:#00007f;}")

    def showBalanceInfoAndDisableButton(self,frameDeletedAmount=0,):
        pushButtonsLunch = self.lunchTab.findChildren(QtWidgets.QPushButton) #adding pushButton from lunchTab to list
        pushButtonsDrink = self.drinkTab.findChildren(QtWidgets.QPushButton) #adding pushButton from drinkTab to list
        pushButtons = pushButtonsLunch + pushButtonsDrink

        labelLunch =self.lunchTab.findChildren(QtWidgets.QLabel)
        labelDrinks =self.drinkTab.findChildren(QtWidgets.QLabel)
        labels = labelLunch + labelDrinks
        textLabels = []
        for name,price,text in zip (labels[0::3],labels[1::3],labels[2::3]):
            list = [name,price,text]
            textLabels.append(text)

        frameList = self.getFrameList()
        self.totalCost = 0
        if (len(frameList)==0 and len(pushButtons)!=0) :
            self.remainingBalance = self.currentBalance
             #in no frames are present in billing
            for i in range(0,len(pushButtons)): #for enabling and disabling Button
                if pushButtons[i].availability == 0:
                    textLabels[i].show()
                    textLabels[i].setText("Unavailabe")
                    textLabels[i].setStyleSheet("color:#850f2a; background-color:grey; font:15pt; border: 2px solid grey; border-radius: 5px; background-color:grey; font-weight:600; ")
                    pushButtons[i].setEnabled(False)

                elif int(self.remainingBalance) < int(pushButtons[i].price) :
                    pushButtons[i].setEnabled(False)
                    textLabels[i].show()
                    textLabels[i].setText("Insufficient \n Balance")
                    textLabels[i].setStyleSheet("color:#850f2a; background-color:grey; font:13pt; border: 2px solid grey; border-radius: 5px; background-color:grey; font-weight:600;" )
                else:
                    textLabels[i].hide()
                    pushButtons[i].setEnabled(True)
        else:
            #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
            for frame in frameList:
                self.totalCost += int(frame[4].text())
                self.remainingBalance = self.currentBalance - self.totalCost
            for frame in frameList:
                if self.remainingBalance < int(frame[2].text()):
                    frame[9].setEnabled(False)
                    frame[9].setStyleSheet("*{border: 2px solid grey; border-radius: 5px;  font-size:13pt; font-weight:1000; color:black; background-color:grey;}")
                else:
                    frame[9].setEnabled(True)
                    frame[9].setStyleSheet("*{border: 2px solid grey; border-radius: 5px;  font-size:13pt; font-weight:1000; color:green;}"
                            ":hover{border: 2px solid green; border-radius: 5px; color:green;}"
                                ":pressed{border: 2px solid grey; border-radius: 5px; background-color:green; color:white;}")


            self.totalCost -= frameDeletedAmount
            self.remainingBalance = self.currentBalance - self.totalCost
             #in no frames are present in billing
            for i in range(0,len(pushButtons)): #for enabling and disabling Button
                if pushButtons[i].availability == 0:
                    textLabels[i].show()
                    textLabels[i].setText("Unavailabe")
                    textLabels[i].setStyleSheet("color:#850f2a; background-color:grey; font:15pt; border: 2px solid grey; border-radius: 5px; background-color:grey; font-weight:600; ")
                    pushButtons[i].setEnabled(False)

                elif int(self.remainingBalance) < int(pushButtons[i].price) :
                    pushButtons[i].setEnabled(False)
                    textLabels[i].show()
                    textLabels[i].setText("Insufficient \n Balance")
                    textLabels[i].setStyleSheet("color:#850f2a; background-color:grey; font:13pt; border: 2px solid grey; border-radius: 5px; background-color:grey; font-weight:600;" )
                else:
                    textLabels[i].hide()
                    pushButtons[i].setEnabled(True)


        self.totalCostAmount.setText("Rs. "+ str(self.totalCost))
        self.remainingBalanceAmount.setText("Rs. "+ str(self.remainingBalance))
        self.billTotalCostLabel.setText("Rs. " + str(self.totalCost))
        self.currentBalanceAmount.setText("Rs. "+ str(self.currentBalance))
        if self.totalCost == 0:
            self.paybillBtn.setEnabled(False)
            self.paybillBtn.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; font-size:15pt; font-weight:600; font-size:15pt; font-weight:600;}")

        else:
            self.paybillBtn.setEnabled(True)
            self.paybillBtn.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #99deb5;font-size:15pt; font-weight:600;}"
                            ":hover{border: 2px solid green; border-radius: 5px;}"
                                ":pressed{border: 2px solid grey; border-radius: 5px; background-color: #5ddeaa; color:black;}")

    def removeHighLight(self,frameName=0):
        """
        #for hovering effect in frames
        query = QSqlQuery()
        query.exec_("SELECT* FROM foodTable")
        availability_list=[]
        while(query.next()):
            avail=query.value(5)
            availability_list.append(avail)
        imageFrames_lunch = self.lunchTab.findChildren(QtWidgets.QFrame)
        imageFrames_drinks = self.drinkTab.findChildren(QtWidgets.QFrame)
        imageFrames = imageFrames_lunch + imageFrames_drinks
        imageFrame = []
        for a,b,c in zip (imageFrames[0::3],imageFrames[1::3],imageFrames[2::3]):
            imageFrame.append(a)
        for i in range(0,len(imageFrame)):
            if frameName == 0:
                if availability_list[i] == 0:
                    imageFrame[i].setStyleSheet("#"+imageFrame[i].objectName()+ " {border : 1px solid black;}" "#"+imageFrame[i].objectName()+":hover{border: 3px solid red; border-radius: 5px;}")
                else:
                    imageFrame[i].setStyleSheet("#"+imageFrame[i].objectName()+ " {border : 1px solid black;}" "#"+imageFrame[i].objectName()+":hover{border: 3px solid green; border-radius: 5px;}")

            if str(imageFrame[i].objectName()) == frameName:
                        imageFrame[i].setStyleSheet("#"+imageFrame[i].objectName()+ " {border : 1px solid black;}" "#"+imageFrame[i].objectName()+":hover{border: 3px solid green; border-radius: 5px;}")
        """
        #creating a list of frames in lucnhTab
        lunchTab_frames = self.lunchTab.findChildren(QtWidgets.QFrame)
        drinkTab_frames = self.drinkTab.findChildren(QtWidgets.QFrame)
        frames = lunchTab_frames + drinkTab_frames
        #removing the higlighting when deleted or decremented
        for frame in frames:
            if frameName==0:
                frame.setStyleSheet("#"+frame.objectName()+ " {border : 1px solid black;}" "#"+frame.objectName()+":hover{border: 3px solid green; border-radius: 5px;}")
            elif str(frame.objectName()) == frameName:
                frame.setStyleSheet("#"+frame.objectName()+ " {border : 1px solid black;}" "#"+frame.objectName()+":hover{border: 3px solid green; border-radius: 5px;}")
        #"""

    def IncQuantity(self):
        source = self.MainWindow.sender()
        objName = source.objectName()
        frameList = self.getFrameList()

        #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
        for frame in frameList:
            for item in frame:
                if item.objectName() == objName:
                    incQuantity = int(frame [3].text()) + 1
                    frame[3].setText(str(incQuantity))
                    incAmount = int(frame[4].text()) +int(frame[2].text()) #currentAmount + Price
                    frame[4].setText(str(incAmount))
                    self.showBalanceInfoAndDisableButton()

    def DecQuantity(self):
        source = self.MainWindow.sender()
        objName = source.objectName()
        frameList = self.getFrameList()
        #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
        for frame in frameList:
            for item in frame:
                if item.objectName() == objName:
                    if int(frame[3].text()) == 1: #remove the frame from the bill area
                        self.removeHighLight(str(frame[0].objectName()))
                        frameDeletedAmount = int(frame[4].text())
                        for item in frame: #delete frame from billing area
                            self.billLayout.removeWidget(item)
                            item.deleteLater()
                            item = None
                        #setting the quantity back to zero
                        frameItems = self.lunchTab.findChildren(QtWidgets.QFrame)
                        for frameItem in frameItems:
                            if frameItem.objectName() == objName[:-11]+"Frame":
                                foodItem = frameItem.findChildren(QtWidgets.QPushButton)
                                foodItem[0].quantity = 0
                        frameAmountDeleted = int(frame[4].text())
                        self.showBalanceInfoAndDisableButton(frameDeletedAmount)

                    if int(frame[3].text()) > 1: #decrement the quantity
                        decQuantity = int(frame [3].text()) - 1
                        frame[3].setText(str(decQuantity))
                        incAmount = int(frame[4].text()) - int(frame[2].text()) #currentAmount - Price
                        frame[4].setText(str(incAmount))
                        frameAmountDeleted = 0
                        self.showBalanceInfoAndDisableButton()

    def deleteFrame(self):
        source = self.MainWindow.sender()
        objName = source.objectName()
        objName=objName[:-12]
        frameList = self.getFrameList()
        #frame index 0=frame 1=name 2=price 3 =quantity 4=Amount 5=RsPricelabel 6=RsAmountLabel 7=minus 8=plus 9=delete
        for frameRight in frameList:
            for item in frameRight:
                if item.objectName() == objName+"Frame":
                    self.removeHighLight(str(frameRight[0].objectName())) #removes higlighting
                    for item in frameRight: #remove frame from bill area
                        self.billLayout.removeWidget(item)
                        item.deleteLater()
                        item = None
                    frameDeletedAmount = int(frameRight[4].text())
                    #setting quantity back to zero
                    frameItems = self.lunchTab.findChildren(QtWidgets.QFrame)
                    for frameItem in frameItems:
                        if frameItem.objectName() == objName+"Frame":
                            foodItem = frameItem.findChildren(QtWidgets.QPushButton)
                            foodItem[0].quantity = 0

        self.showBalanceInfoAndDisableButton(frameDeletedAmount)

    def makeFrame(self,frame,objName,xPos,yPos,width,height):
        frame.setGeometry(QtCore.QRect(xPos, yPos, width,height))
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Plain)
        frame.setObjectName(objName)

    def getFrameList(self):
        #adding list of frames in a list
        labels = self.billLayoutWidget.findChildren(QtWidgets.QFrame)
        buttons = self.billLayoutWidget.findChildren(QtWidgets.QPushButton)
        frameList = []
        for a,b,c,d,e,f,g,h,i,j,k in zip (labels[0::7],labels[1::7],labels[2::7],labels[3::7],labels[4::7],labels[5::7],labels[6::7],buttons[0::4],buttons[1::4],buttons[2::4],buttons[3::4]):
            frame=[a,b,c,d,e,f,g,h,i,j,k]
            frameList.append(frame)
        return frameList

    def frameImage(self,disName,objName,frameName,price,xPos,yPos,imgWi,imgHi,path,cat,availability):
        if cat == "Lunch/Snacks":
            frame = QtWidgets.QFrame(self.lunchTab)
        else:
            frame = QtWidgets.QFrame(self.drinkTab)
        frame.setGeometry(QtCore.QRect(xPos, yPos, imgWi,imgHi+2*oneUnit))
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Plain)
        frame.setObjectName(frameName)
        itemName = QtWidgets.QLabel(disName,frame)
        itemName.setGeometry(QtCore.QRect(0 , 0, imgWi,oneUnit))
        itemName.setAlignment(QtCore.Qt.AlignCenter)
        itemName.setStyleSheet("font-size:135t; font-weight:600; color:#00007f;")
        itemImageButton = QtWidgets.QPushButton( frame)
        itemImageButton.setGeometry(QtCore.QRect(5 , oneUnit, imgWi-10,imgHi))
        itemImageButton.setObjectName(objName)
        itemImageButton.disName = disName
        itemImageButton.price = price
        itemImageButton.frame = frameName
        itemImageButton.quantity = 0
        itemImageButton.amount = price
        itemImageButton.availability = availability
        itemImageButton.clicked.connect(self.Add)
        itemPrice = QtWidgets.QLabel("Rs. "+price,frame)
        itemPrice.setGeometry(QtCore.QRect(0 , oneUnit + imgHi, imgWi,oneUnit))
        itemPrice.setAlignment(QtCore.Qt.AlignCenter)
        itemPrice.setStyleSheet("QLabel {font-size:15pt; font-weight:600; color:red;}")
        itemDetail = QtWidgets.QLabel(" test ",frame)
        itemDetail.setObjectName(objName+"text")
        itemDetail.setGeometry(QtCore.QRect(10 , imgHi/2+40, imgWi-20,45))
        itemDetail.setAlignment(QtCore.Qt.AlignCenter)

        #setting image to the button
        if (path != 0):
            pixmap = QPixmap("image/"+path)
            w = itemImageButton.width()
            h = itemImageButton.height()
            scaled_pixmap = pixmap.scaled(h, w)
            itemImageButton.setIcon(QtGui.QIcon(scaled_pixmap))
            itemImageButton.setIconSize(QtCore.QSize(200,200))

    def getFoodItemList(self):
        query = QSqlQuery()
        query.exec_("SELECT* FROM foodTable")
        foodTableList=[]
        while(query.next()):
            list=[]
            name=query.value(1)
            price=query.value(2)
            cat=query.value(3)
            path=query.value(4)
            avail=query.value(5)
            list.append(name)
            list.append(price)
            list.append(cat)
            list.append(path)
            list.append(avail)
            foodTableList.append(list)
        print(foodTableList)
        return foodTableList

    def showingImage2(self):
        foodList = [["Rice Set","60","cat","path"],["Curd","25","cat","path"],["Chicken Roast","60","drinks","path"],["Panner","80","cat","path"],["Fish","60","cat","path"],["Chicken Curry ","60","cat","path"],["Something","60","cat","path"]]
        foodList =self.getFoodItemList()
        imgWi,imgHi=width*.12,height*.2
        imgXDrinks, imgYDrinks= 2*oneUnit, oneUnit
        imgXSnacks, imgYSnacks= 2*oneUnit, oneUnit
        xDrinksCount,yDrinksCount = 0,0
        xSnacksCount,ySnacksCount = 0,0
        for food in foodList:
            name,price,cat,path,availability=food[0],str(food[1]),food[2],food[3],food[4]
            objName = name.replace(" ", "")
            if cat == "Drinks":
                self.frameImage(name,objName,objName+"Frame",price,imgXDrinks,imgYDrinks,imgWi,imgHi,path,cat,availability)
                if xDrinksCount < 4:
                    imgXDrinks = imgXDrinks + imgWi + oneUnit
                    xDrinksCount +=1
                else:
                    imgYDrinks = imgYDrinks + imgHi + oneUnit*3
                    imgXDrinks = 2*oneUnit
                    xDrinksCount = 0
                    yDrinksCount += 1
            else:
                self.frameImage(name,objName,objName+"Frame",price,imgXSnacks,imgYSnacks,imgWi,imgHi,path,cat,availability)
                if xSnacksCount < 4:
                    imgXSnacks = imgXSnacks + imgWi + oneUnit
                    imgYSnacks = imgYSnacks
                    xSnacksCount +=1
                else:
                    imgYSnacks = imgYSnacks + imgHi + oneUnit*3
                    imgXSnacks = 2*oneUnit
                    xSnacksCount = 0
                    ySnacksCount += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    if not createConnection():
        sys.exit(-1)
    ui = MainInterface()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
