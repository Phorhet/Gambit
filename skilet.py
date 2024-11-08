from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from sys import argv, exit

class ButtonInLineEdit(QLineEdit):
    def __init__(self,parent=None):
        QLineEdit.__init__(self,parent)

        self.ButtonShowKeyboard = QToolButton(self)
        self.ButtonShowKeyboard.setCursor(Qt.PointingHandCursor)

        self.ButtonShowKeyboard.setFocusPolicy(Qt.NoFocus)
        self.ButtonShowKeyboard.setIcon(QIcon("icons/myIcon.png"))
        self.ButtonShowKeyboard.setStyleSheet("background: transparent; border: none;")

        layout = QHBoxLayout(self)
        layout.addWidget(self.ButtonShowKeyboard,0,Qt.AlignRight)

        layout.setSpacing(0)
        layout.setMargin(5)

        self.ButtonShowKeyboard.setToolTip(QApplication.translate("None", "Show virtual keyboard", None, QApplication.UnicodeUTF8))

def MyFunction(arg=None):
    print ("MyFunction() called: arg = %s"%arg)

a=QApplication(argv)
LineEdit = ButtonInLineEdit()
LineEdit.connect(LineEdit.ButtonShowKeyboard, SIGNAL("clicked()"), MyFunction)
LineEdit.show()
exit(a.exec_())