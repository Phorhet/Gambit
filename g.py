from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import sys


class Window(QMainWindow):

    def __init__(self):
        super().__init__()

        # setting title 
        self.setWindowTitle("Python ")

        # setting geometry 
        self.setGeometry(100, 100, 600, 400)

        # calling method 
        self.UiComponents()

        # showing all the widgets 
        self.show()

        # method for widgets

    def UiComponents(self):
        # creating a combo box widget
        self.combo_box = QComboBox(self)

        # setting geometry of combo box 
        self.combo_box.setGeometry(200, 150, 150, 30)

        # geek list 
        geek_list = ["Sayian", "Super Sayian"]

        # making it editable 
        self.combo_box.setEditable(True)

        # adding list of items to combo box 
        self.combo_box.addItems(geek_list)

        # name 
        name = "Sayian Combo box"

        # setting name to the combo box 
        self.combo_box.setAccessibleName(name)

    # create pyqt5 app


App = QApplication(sys.argv)

# create the instance of our Window 
window = Window()

# start the app 
sys.exit(App.exec()) 