import sys
import os
from db import *
from PyQt5.QtSql import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QLabel, QFileDialog, QVBoxLayout
from PyQt5 import QtGui
from functools import partial
import shutil

from PyQt5.QtGui import QPixmap

print( "\\")



class Ui_MainWindow(object):
    def openRegisterInterface(self,MainWindow):
        from Register import Ui_Register
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_Register()
        self.ui.setupUi(self.window)
        #self.MainWindow = MainWindow
        #self.coverFrame.show()
        self.window.show()

    def openUserInterface(self,MainWindow):
        from mainUI import MainInterface
        self.window = QtWidgets.QMainWindow()
        self.ui = MainInterface()
        self.ui.setupUi(self.window)
        self.ui.loginWindowWidget.hide()
        MainWindow.close()
        self.MainWindow = MainWindow
        self.ui.userName = self.userName
        self.ui.registrationNo = self.registrationNo
        self.ui.userNameText.setText(str(self.userName))
        self.ui.regNoText.setText(str(self.registrationNo))
        self.ui.currentBalance = self.currentBalance
        self.ui.showBalanceInfoAndDisableButton()
        self.ui.removeHighLight()
        self.window.show()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("MainWindow")
        MainWindow.showFullScreen()
        self.userName = "0"
        self.registrationNo = "0"
        self.foodImagePath = ""
        # width,height= MainWindow.frameGeometry().width(),MainWindow.frameGeometry().height()
        self.width,self.height = MainWindow.frameGeometry().width(),MainWindow.frameGeometry().height()
        self.oneUnit = (self.width + self.height)/100
        self.MainWindow = MainWindow

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.display_frame = QtWidgets.QFrame(self.centralwidget)
        self.display_frame.setGeometry(QtCore.QRect(0, 0, self.width*.7 -2,self.height))
        self.display_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.display_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.display_frame.setObjectName("display_frame")

        self.username_display_frame = QtWidgets.QFrame(self.display_frame)
        self.username_display_frame.setGeometry(QtCore.QRect(1,1, self.width*.7 -2 , self.height*.15-2))
        self.username_display_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.username_display_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.username_display_frame.setObjectName("username_display_frame")
        self.userInfoFrame()

        self.tabWidget = QtWidgets.QTabWidget(self.display_frame)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(QtCore.QRect(2, self.height*.15 +2, self.width*.7 -3, self.height*.85 -3))
        self.tabWidget.setStyleSheet("font:150 25pt \"Times New Roman\"; color: #00007f; font-weight:600;")

        self.lunch_tab = QtWidgets.QWidget()
        self.lunch_tab.setObjectName("lunch_tab")
        self.lunch_tab.setStyleSheet("font:150 25pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.tabWidget.addTab(self.lunch_tab, "Lunch/Snacks")

        self.drinks_tab = QtWidgets.QWidget()
        self.drinks_tab.setObjectName("drinks_tab")
        self.drinks_tab.setStyleSheet("font:150 25pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.tabWidget.addTab(self.drinks_tab, "Drinks")

        # self.display_layout.addWidget(self.tabWidget)
        self.input_frame = QtWidgets.QFrame(self.centralwidget)
        self.input_frame.setGeometry(QtCore.QRect(self.width*.7 ,52, self.width*.3 -2, self.height))
        self.input_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.input_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.input_frame.setObjectName("input_frame")

        self.helpLabel = QtWidgets.QLabel("Select an item to make it \n available.",self.input_frame)
        self.helpLabel.setGeometry(QtCore.QRect(10,5, 400, 50))
        self.helpLabel.setStyleSheet("font:150 18pt \"Times New Roman\"; color:black; font-weight:600;")

        # self.layoutWidget1 = QtWidgets.QWidget(self.input_frame)
        # self.layoutWidget1.setGeometry(QtCore.QRect(20, self.height*.15 +10, self.width*.3-40, self.height*.45))
        # self.layoutWidget1.setObjectName("layoutWidget1")
        # self.image_layout = QtWidgets.QVBoxLayout(self.input_frame)
        # self.image_layout.setContentsMargins(0, 0, 0, 0)
        # self.image_layout.setObjectName("image_layout")
        self.input_heading_frame = QtWidgets.QFrame(self.input_frame)
        self.input_heading_frame.setGeometry(QtCore.QRect(0,62, self.width*.3 -2 , 50))
        self.input_heading_frame.setFrameShape(QtWidgets.QFrame.Box)
        self.input_heading_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.input_heading_frame.setObjectName("input_heading_frame")

        self.display_heading_label = QtWidgets.QLabel("Add Food Items!!", self.input_heading_frame)
        self.display_heading_label.setGeometry(QtCore.QRect(0, 0, self.width*.3 -2, 50))
        self.display_heading_label.setAlignment(QtCore.Qt.AlignCenter)
        self.display_heading_label.setStyleSheet("QLabel {font-size:20pt; font-weight:600; background-color:#00007f; color:white;}")

        self.image_label = QtWidgets.QLabel(self.input_frame)
        self.image_label.setObjectName("image_label")
        self.image_label.setGeometry(10,120,self.width*.3-20, self.height*.45)

        # self.image_layout.addWidget(self.image_label)
        self.select_image_btn = QtWidgets.QPushButton("Select Image",self.input_frame)
        self.select_image_btn.setObjectName("select_image_btn")
        self.select_image_btn.setGeometry(QtCore.QRect(10,self.height*.65-30,self.width*.3-20,45))
        self.select_image_btn.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.select_image_btn.clicked.connect(self.selectImage)

        # self.image_layout.addWidget(self.select_image_btn)
        self.layoutWidget2 = QtWidgets.QWidget(self.input_frame)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, self.height*.65+20, self.width*.3 - 40, self.height*.2-50))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.layoutWidget2.setStyleSheet("font:90 13pt \"Times New Roman\"; color:black; font-weight:500;")

        self.input_layout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.input_layout.setContentsMargins(0, 0, 0, 0)
        self.input_layout.setObjectName("input_layout")
        self.name_layout = QtWidgets.QHBoxLayout()
        self.name_layout.setObjectName("name_layout")
        self.name_label = QtWidgets.QLabel(self.layoutWidget2)
        self.name_label.setObjectName("name_label")
        self.name_label.setText("Name")
        self.name_layout.addWidget(self.name_label)
        self.name_lineEdit = QtWidgets.QLineEdit(self.layoutWidget2)
        self.name_lineEdit.setObjectName("name_lineEdit")

        self.name_layout.addWidget(self.name_lineEdit)
        self.input_layout.addLayout(self.name_layout)
        self.price_layout = QtWidgets.QHBoxLayout()
        self.price_layout.setObjectName("price_layout")
        self.price_label = QtWidgets.QLabel(self.layoutWidget2)
        self.price_label.setObjectName("price_label")
        self.price_label.setText("Price")
        self.price_layout.addWidget(self.price_label)
        self.price_lineEdit = QtWidgets.QLineEdit(self.layoutWidget2)
        self.price_lineEdit.setObjectName("price_lineEdit")
        self.price_layout.addWidget(self.price_lineEdit)
        self.input_layout.addLayout(self.price_layout)
        self.category_layout = QtWidgets.QHBoxLayout()
        self.category_layout.setObjectName("category_layout")
        self.category_label = QtWidgets.QLabel(self.layoutWidget2)
        self.category_label.setObjectName("category_label")
        self.category_label.setText("Category")
        self.category_layout.addWidget(self.category_label)
        self.category_comboBox = QtWidgets.QComboBox(self.layoutWidget2)
        self.category_comboBox.setObjectName("category_comboBox")
        self.category_comboBox.addItem("Lunch/Snacks")
        self.category_comboBox.addItem("Drinks")
        self.category_layout.addWidget(self.category_comboBox)
        self.input_layout.addLayout(self.category_layout)

        self.save_btn = QtWidgets.QPushButton("Save", self.input_frame)
        self.save_btn.setObjectName("save_btn")
        self.save_btn.setGeometry(QtCore.QRect( 20,self.height*.85, 180, 40))
        self.save_btn.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.save_btn.clicked.connect(self.saveFoodItem)
        if self.foodImagePath == "":
            self.save_btn.setEnabled(False)
        else:
            self.save_btn.setEnabled(True)

        self.cancel_btn = QtWidgets.QPushButton("Cancel", self.input_frame)
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setGeometry(QtCore.QRect( 220 ,self.height*.85,180, 40))
        self.cancel_btn.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.cancel_btn.clicked.connect(self.clearInput)

        self.update_btn = QtWidgets.QPushButton("Update", self.input_frame)
        self.update_btn.setGeometry(QtCore.QRect( 20,self.height*.85, 180, 40))
        self.update_btn.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.update_btn.clicked.connect(self.update_food)
        self.update_btn.hide()

        self.delete_btn = QtWidgets.QPushButton("Delete", self.input_frame)
        self.delete_btn.setGeometry(QtCore.QRect( 220 ,self.height*.85,180, 40))
        self.delete_btn.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:600;")
        self.delete_btn.clicked.connect(self.delete_food)
        self.delete_btn.hide()

        self.showWarningText = QtWidgets.QLabel("", self.input_frame)
        self.showWarningText.setGeometry(QtCore.QRect( 50 ,self.height*.85-40,180, 40))
        self.showWarningText.setStyleSheet("font:90 13pt \"Times New Roman\"; color: #00007f; font-weight:500; color:red;")

        #making menu boarder
        self.menuFrame = QtWidgets.QFrame(self.centralwidget)
        self.makeMenuFrame()

        self.coverFrame = QtWidgets.QFrame(self.centralwidget)
        self.coverFrame.setGeometry(QtCore.QRect(0,0,1500,1500))
        self.coverFrame.hide()
        self.showingImage2()
        MainWindow.setCentralWidget(self.centralwidget)

        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def makeFrame(self,frame,objName,xPos,yPos,width,height):
        frame.setGeometry(QtCore.QRect(xPos, yPos, width,height))
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Plain)
        frame.setObjectName(objName)

    def makeMenuFrame(self):
        self.makeFrame(self.menuFrame,"menuFrame",0,0,self.width ,52)
        self.menuFrame.setStyleSheet("background-color: #00007f;")

        self.menuLabel = QtWidgets.QLabel("Canteen Management System ",self.menuFrame)
        self.menuLabel.setGeometry(QtCore.QRect(0, -1, self.width,50))
        self.menuLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.menuLabel.setStyleSheet("font:150 35pt \"Times New Roman\"; color:white;")

        self.RegisterButton = QtWidgets.QPushButton("Register",self.menuFrame)
        self.RegisterButton.setGeometry(QtCore.QRect(self.width-210,3,100,45))
        self.RegisterButton.clicked.connect(partial(self.openRegisterInterface))
        self.RegisterButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")

        exitButton = QtWidgets.QPushButton("Exit",self.menuFrame)
        exitButton.setGeometry(QtCore.QRect(self.width-105,3,100,45))
        exitButton.clicked.connect(partial(self.openUserInterface,self.MainWindow))
        exitButton.setStyleSheet("*{border: 2px solid grey; border-radius: 5px; background-color: #44449a; color:white; font-size:15pt; font-weight:600;}"
                                ":hover{border: 2px solid green; border-radius: 5px;}"
                                    ":pressed{border: 2px solid grey; border-radius: 5px; background-color:#00007f; color:white;}")

    def userInfoFrame(self):
        font = QtGui.QFont("Times New Roman", 15)
        #self.makeFrame(self.userInfoArea,"userInfoArea",1,1,self.width*.7 -2, self.height*.15 -2)
        self.userNameLabel = QtWidgets.QLabel("Username: ",self.username_display_frame)
        self.userNameLabel.setGeometry(QtCore.QRect(5,50,150,50))
        self.userNameLabel.setFont(font)
        self.userNameLabel.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.userNameText = QtWidgets.QLabel(self.username_display_frame)
        self.userNameText.setGeometry(QtCore.QRect(150,50,200,50))
        #self.userNameText.setText(str(self.userName))
        self.userNameText.setFont(font)
        self.userNameText.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.regLabel = QtWidgets.QLabel("Registration No.: ",self.username_display_frame)
        self.regLabel.setGeometry(QtCore.QRect(450,50,250,50))
        self.regLabel.setFont(font)
        self.regLabel.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

        self.regNoText = QtWidgets.QLabel(self.username_display_frame)
        self.regNoText.setGeometry(QtCore.QRect(675,50,300,50))
        #self.regNoText.setText(str(self.registrationNo))
        self.regNoText.setFont(font)
        self.regNoText.setStyleSheet("QLabel {font-size:20pt; font-weight:600; color: black;}")

    def selectImage(self, MainWindow):
        img_file = QFileDialog.getOpenFileName(self.MainWindow,'??????','./','Image Files(*.png *.jpg *.bmp)')
        self.foodImagePath = os.path.basename(img_file[0])

        pixmap = QPixmap(img_file[0]) #complete path to show image in label
        w = self.image_label.width()
        h = self.image_label.height()
        self.image_label.setPixmap(pixmap.scaled(w,h))
        self.save_btn.show()
        self.cancel_btn.show()
        self.update_btn.hide()
        self.delete_btn.hide()

        if self.foodImagePath == "":
            self.save_btn.setEnabled(False)
        else:
            self.save_btn.setEnabled(True)

        #to copy selected image to our dir image folder
        src_dir = img_file[0].replace(self.foodImagePath , "" )
        img_dir = img_file[0]
        dst_dir = os.getcwd().replace("\\","/") + "/image/"
        dst_img = dst_dir + self.foodImagePath
        for file in os.listdir(src_dir):
            if file == self.foodImagePath:
                if os.path.exists(dst_img):
                    print("asdas")
                    break
                shutil.copy(img_dir,dst_dir)
                break

    def clearInput(self):
        self.name_lineEdit.setText("")
        self.price_lineEdit.setText("")
        self.image_label.clear()
        self.setupUi(self.MainWindow)

    def update_food(self):
        input_name = self.name_lineEdit.text()
        input_price = self.price_lineEdit.text()
        if input_name !="" and input_price != "":
            query = QSqlQuery()
            query.exec_("UPDATE foodTable SET availability = 1,foodName= '"+input_name+"', price= '"+input_price+"' WHERE foodName = '"+input_name+"' ")
            self.clearInput()
        else:
            self.showWarningText.setText("PLease fill all the fields.")

    def delete_food(self):
        input_name = self.name_lineEdit.text()
        input_price = self.price_lineEdit.text()
        if input_name !="" and input_price != "":
            query = QSqlQuery()
            query.exec_("DELETE FROM foodTable WHERE foodName = '"+input_name+"' ")
            self.clearInput()
        else:
            self.showWarningText.setText("PLease fill all the fields.")

    def update(self):
        source = self.MainWindow.sender()
        objName = source.objectName()
        foodName1 = source.foodName
        query = QSqlQuery()
        query.exec_("UPDATE foodTable SET availability = 1 WHERE foodName = '"+foodName1+"' ")
        #creating a list of frames in lucnhTab
        framesLunch = self.lunch_tab.findChildren(QtWidgets.QFrame)
        framesDrink = self.drinks_tab.findChildren(QtWidgets.QFrame)
        frames = framesLunch + framesDrink
        if source.availability == 0:
            source.availability = 1
            for frame in frames:
                if frame.objectName() == source.frame:
                    query.exec_("UPDATE foodTable SET availability = 1 WHERE foodName = '"+foodName1+"' ")
                    frame.setStyleSheet("#"+frame.objectName()+ " {border : 5px solid green;}")
        elif source.availability ==1:
            source.availability = 0
            for frame in frames:
                if frame.objectName() == source.frame:
                    query.exec_("UPDATE foodTable SET availability = 0 WHERE foodName = '"+foodName1+"' ")
                    frame.setStyleSheet("#"+frame.objectName()+ " {border : 5px solid red;}")

        path = os.getcwd().replace("\\","/") + "/image/"+ source.path
        pixmap = QPixmap(path)
        self.image_label.setPixmap(pixmap.scaled(self.image_label.width(),self.image_label.height()))
        self.name_lineEdit.setText(source.foodName)
        self.price_lineEdit.setText(source.price)
        self.update_btn.show()
        self.delete_btn.show()

    def saveFoodItem(self):
        input_name = self.name_lineEdit.text()
        input_price = self.price_lineEdit.text()
        if input_name !="" and input_price != "":
            food_model = QSqlTableModel()
            food_model.setTable("foodTable")
            food_model.select()
            record = food_model.record()
            record.setValue("image",self.foodImagePath)
            record.setValue("foodName", input_name)
            record.setValue("price",input_price)
            record.setValue("category", self.category_comboBox.currentText())
            record.setValue("availability", 0)

            if food_model.insertRecord(-1, record):
                food_model.select()
            # self.frameImage(display_name,objName, frameName,display_price,10,10, 100,100 )
            self.clearInput()
        else:
            self.showWarningText.setText("PLease fill all the fields.")

    def frameImage(self,disName,objName,frameName,price,xPos,yPos,imgWi,imgHi,path,cat,availability):
        if cat == "Lunch/Snacks":
            frame = QtWidgets.QFrame(self.lunch_tab)
        else:
            frame = QtWidgets.QFrame(self.drinks_tab)
        frame.setGeometry(QtCore.QRect(xPos, yPos, imgWi,imgHi+2*self.oneUnit))
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Plain)
        frame.setObjectName(frameName)
        itemName = QtWidgets.QLabel(disName,frame)
        itemName.setGeometry(QtCore.QRect(0 , 0, imgWi,self.oneUnit))
        itemName.setAlignment(QtCore.Qt.AlignCenter)
        if availability == 0:
            frame.setStyleSheet("#"+frame.objectName()+ " {border : 5px solid red;}")
        elif availability == 1:
            frame.setStyleSheet("#"+frame.objectName()+ " {border : 5px solid green;}")
        itemName.setStyleSheet("QLabel {font-size:15pt; font-weight:600; color:#00007f;}")
        itemImageButton = QtWidgets.QPushButton( frame)
        itemImageButton.setGeometry(QtCore.QRect(5 , self.oneUnit, imgWi-10,imgHi))
        itemImageButton.setObjectName(objName)
        itemImageButton.availability = availability
        itemImageButton.frame = frameName
        itemImageButton.price = str(price)
        itemImageButton.foodName = disName
        itemImageButton.path = path
        itemPrice = QtWidgets.QLabel("Rs. "+price,frame)
        itemPrice.setGeometry(QtCore.QRect(0 , self.oneUnit + imgHi, imgWi,self.oneUnit))
        itemPrice.setAlignment(QtCore.Qt.AlignCenter)
        itemImageButton.clicked.connect(self.update)
        itemPrice.setStyleSheet("QLabel {font-size:15pt; font-weight:600; color:#00007f;}")
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
            availability_list= query.value (5)
            list.append(name)
            list.append(price)
            list.append(cat)
            list.append(path)
            list.append(availability_list)
            foodTableList.append(list)
        return foodTableList

    def showingImage2(self):
        #foodList = [["Rice Set","60","cat","path"],["Curd","25","cat","path"],["Chicken Roast","60","drinks","path"],["Panner","80","cat","path"],["Fish","60","cat","path"],["Chicken Curry ","60","cat","path"],["Something","60","cat","path"]]
        foodList =self.getFoodItemList()

        imgWi,imgHi=self.width*.12,self.height*.2
        imgXDrinks, imgYDrinks= self.oneUnit, self.oneUnit
        imgXSnacks, imgYSnacks= self.oneUnit, self.oneUnit
        xDrinksCount,yDrinksCount = 0,0
        xSnacksCount,ySnacksCount = 0,0
        for food in foodList:
            name,price,cat,path,availability=food[0],str(food[1]),food[2],food[3],food[4]
            objName = name.replace(" ", "")
            if cat == "Lunch/Snacks":
                self.frameImage(name,objName,objName+"Frame",price,imgXDrinks,imgYDrinks,imgWi,imgHi,path,cat,availability)
                if xDrinksCount < 4:
                    imgXDrinks = imgXDrinks + imgWi + self.oneUnit
                    xDrinksCount +=1
                else:
                    imgYDrinks = imgYDrinks + imgHi + self.oneUnit*3
                    imgXDrinks = self.oneUnit
                    xDrinksCount = 0
                    yDrinksCount += 1
            else:
                self.frameImage(name,objName,objName+"Frame",price,imgXSnacks,imgYSnacks,imgWi,imgHi,path,cat,availability)
                if xSnacksCount < 4:
                    imgXSnacks = imgXSnacks + imgWi + self.oneUnit
                    imgYSnacks = imgYSnacks
                    xSnacksCount +=1
                else:
                    imgYSnacks = imgYSnacks + imgHi + self.oneUnit*3
                    imgXSnacks = self.oneUnit
                    xSnacksCount = 0
                    ySnacksCount += 1

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    if not createConnection():
        sys.exit(-1)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
