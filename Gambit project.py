import sqlite3
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QTabWidget, \
    QTextEdit, QPlainTextEdit, QLabel, QMessageBox, QTextBrowser
from qt_material import apply_stylesheet
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

con = sqlite3.connect(r"C:\Users\Роман\PycharmProjects\pythonProject\Chess")
cur = con.cursor()


def show_welcome_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText("Добро пожаловать в наше приложение!")
    msg.setWindowTitle("Приветствие")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


class AnotherWindow(QWidget):
    def __init__(self, name):
        super().__init__()
        self.name = name
        layout = QVBoxLayout()
        self.text_browser = QTextBrowser()
        self.text_browser.setText(name)
        layout.addWidget(self.text_browser)
        self.setLayout(layout)
        self.setGeometry(500, 300, 400, 500)


class GambitWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.w = None
        self.initUI()

    def get_all(self):
        result = cur.execute("""select * from gambit""").fetchall()
        all = []
        for i in result:
            all.append(i[1])
        return all

    def enter_pressed(self):
        self.search()

    def initUI(self):
        tabs = QTabWidget()
        search_tab = QWidget()
        search_layout = QVBoxLayout()
        self.search_line_edit = QLineEdit()
        self.search_line_edit.returnPressed.connect(self.enter_pressed)
        self.search_line_edit.setClearButtonEnabled(True)
        search_button = QPushButton("Поиск")
        search_button.clicked.connect(self.search)
        search_layout.addWidget(self.search_line_edit)
        search_layout.addWidget(search_button)
        self.history_list = QTextBrowser()
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
        save_button.clicked.connect(self.save_base)
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
        self.gambits_list.itemDoubleClicked.connect(self.doubleclickmouse)
        #Табы и лаяут
        tabs.addTab(search_tab, "Поиск")
        tabs.addTab(info_tab, "Добавление данных")
        tabs.addTab(gambits_tab, "Гамбиты")
        main_layout = QVBoxLayout()
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
        self.setGeometry(300, 100, 400, 500)
        self.setWindowTitle('Гамбит')
        self.show()

    def search(self):
        search_text = "%" + self.search_line_edit.text().lower() + "%"
        result = cur.execute("""select * from gambit where name  like  ?""", (search_text,)).fetchone()
        self.history_list.clear()
        if result is not None:
            self.history_list.setText(result[2])
        else:
            self.history_list.setText("Ошибка, Гамбит не был обнаружен")

    def save_base(self):
        save_textfl = self.save_line_edit.text().lower()
        save_textsl = self.save_area_edit.toPlainText()
        try:
            save = cur.execute(""""INSERT INTO gambit(name, description) VALUES(?,?); """, (save_textfl, save_textsl))
            con.commit()
            print(cur.lastrowid)
        except:
            print("something went wrong")

    def doubleclickmouse(self, item):
        clicked_name = item.text()
        result = cur.execute(
            """select * from gambit where name = ?""",
            (clicked_name,)
        ).fetchone()
        if result is not None:
            self.w = AnotherWindow(result[2])
            self.w.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Гамбит не найден")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_cyan_500.xml')
    show_welcome_message()
    ex = GambitWindow()
    sys.exit(app.exec())
