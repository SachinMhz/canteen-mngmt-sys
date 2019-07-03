import sys

from PyQt5.QtGui import *
from PyQt5.QtSql import *
from PyQt5.QtCore import *

def createConnection():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('KUcanteen.db')
    print("database connected!!!!")
    if not db.open():
        QtGui.QMessageBox.critical(None, "Cannot open database",
                "Unable to establish a database connection.\n"
                "This example needs SQLite support. Please read the Qt SQL "
                "driver documentation for information how to build it.\n\n"
                "Click Cancel to exit.",
                QtGui.QMessageBox.Cancel)
        return False

    query = QSqlQuery()
    print("table created!!!")
    query.exec_("CREATE TABLE IF NOT EXISTS foodTable (id INTEGER primary key AUTOINCREMENT, foodName TEXT,price NUMERIC,category TEXT, image TEXT, availability BOOLEAN)")
    query.exec_("CREATE TABLE IF NOT EXISTS usersTable (id INTEGER primary key AUTOINCREMENT, registration_no INTEGER,username TEXT, password TEXT,post TEXT,balance INTEGER)")

    # name = query.exec_("SELECT foodName FROM foodTable")
    # print(name)
    return True
