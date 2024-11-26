from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QMessageBox, QGridLayout,
                             QMainWindow)
from PyQt6.QtCore import QTimer
import sys


class View(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(300, 80)

        self.label = QLabel('Hi, I am a label')
        self.label.setStyleSheet('border: 1px solid black;')
        self.label.setMaximumHeight(25)
        self.label.setMinimumHeight(25)

        self.label2 = QLabel()
        self.label2.setStyleSheet('border: 1px solid black; background-color: lightyellow')
        self.label2.setMaximumHeight(25)
        self.label2.setMinimumHeight(25)
        self.label2.hide()

        self.button = QPushButton('Click Me')

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 1)
        layout.addWidget(self.label2, 1, 0, 1, 1)
        layout.addWidget(self.button, 2, 0, 1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


class Controller:
    def __init__(self, view):
        self.view = view
        self.duration = 5

        self.view.button.pressed.connect(self.show_msg)

    def show_msg(self):
        self.view.label2.setText(f'I am going to close in {self.duration} seconds.')
        self.view.label2.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

        self.msg = QMessageBox()
        self.msg.setText(f'I am going to close in {self.duration} seconds.')
        self.msg.setIcon(QMessageBox.Icon.Information)
        self.msg.exec()

    def update(self):
        self.view.label2.setText(f'I am going to close in {self.duration} seconds.')
        self.msg.setText(f'I am going to close in {self.duration - 2} seconds.')
        self.duration -= 1

        box_dur = self.duration - 2
        if box_dur < 0:
            self.msg.close()

        if self.duration < 0:
            self.timer.stop()
            self.view.label2.hide()
            self.duration = 5

    def hideit(self, arg):
        arg.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    controller = Controller(View())
    controller.view.show()
    sys.exit(app.exec())