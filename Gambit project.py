import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QTabWidget, \
    QTextEdit, QPlainTextEdit, QLabel
from qt_material import apply_stylesheet

# from PyQt6 import QtCore, Qt


con = sqlite3.connect(r"C:\Users\Роман\PycharmProjects\pythonProject\Chess")
cur = con.cursor()


class GambitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def get_all(self):
        result = cur.execute("""select * from gambit""").fetchall()
        all = []
        for i in result:
            all.append(i[1])
        return all

    def initUI(self):
        tabs = QTabWidget()
        search_tab = QWidget()
        search_layout = QVBoxLayout()
        self.search_line_edit = QLineEdit()
        search_button = QPushButton("Поиск")
        clear_button = QPushButton("Х")
        search_button.clicked.connect(self.search)
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(search_button)
        search_layout.addWidget(clear_button)
        self.history_list = QListWidget()
        search_layout.addWidget(self.history_list)
        search_tab.setLayout(search_layout)


        # таб для сохранения
        info_tab = QWidget()
        info_layout = QVBoxLayout()
        self.save_line_edit = QLineEdit()
        self.nameLabel = QLabel(self)
        self.save_line_edit.setPlaceholderText("Имя Гамбита")
        self.save_area_edit = QPlainTextEdit()
        self.save_area_edit.setPlaceholderText("Информация про Гамбит")
        info_layout.addWidget(self.save_line_edit)
        save_button = QPushButton("Save")
        info_layout.addWidget(self.save_area_edit)
        info_layout.addWidget(save_button)
        info_tab.setLayout(info_layout)

        # таб гамбиты
        gambits_tab = QWidget()
        gambits_layout = QVBoxLayout()
        self.gambits_list = QListWidget()
        self.gambits_list.addItems(self.get_all())
        gambits_layout.addWidget(self.gambits_list)
        gambits_tab.setLayout(gambits_layout)
        tabs.addTab(search_tab, "Поиск")
        tabs.addTab(info_tab, "Информация")
        tabs.addTab(gambits_tab, "Гамбиты")

        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
        self.setGeometry(300, 100, 400, 500)
        self.setWindowTitle('Гамбит')
        self.show()

    def search(self):
        search_text = "%" + self.search_line_edit.text() + "%"
        print(search_text)
        result = cur.execute("""select * from gambit where name like ?""", (search_text,)).fetchone()
        print(result[2])
        self.history_list.clear()
        self.history_list.addItem(result[2])


    # def keyPressEvent(self, event):
    # if event.key() == Qt.Key_Return:
    # self.on_click()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_cyan_500.xml')
    ex = GambitWindow()
    sys.exit(app.exec())