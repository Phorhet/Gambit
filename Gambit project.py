import sqlite3
import sys
import os
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QTabWidget, \
    QPlainTextEdit, QLabel, QMessageBox, QTextBrowser, QFormLayout, QGridLayout, QLineEdit, QComboBox
from qt_material import apply_stylesheet
from PyQt6.QtGui import QPixmap

PATH = os.path.join(os.getcwd(), "Chess")
con = sqlite3.connect(PATH)
cur = con.cursor()

def show_welcome_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Information)
    msg.setText(
        "Добро пожаловать в Проект Гамбит!\n\n"
        "В нашем приложении вы можете:\n"
        "- Ввести название дебюта или гамбита в поисковую строку и получить информацию.\n"
        "- Во второй вкладке пополнить базу данных новой информацией.\n"
        "- В третьей вкладке просмотреть содержимое базы данных.\n"
        "- Двойной клик на элемент откроет новое окно с подробностями и изображением.\n"
        "- Имеется удобный dropbox с информацией которая выводится по клику\n"
        "- В будущем планируются доработки интерфейса и функционала.\n"
        "- Хорошего время препровождения! \n"
    )
    msg.setWindowTitle("Приветствуем Пользователь!")
    msg.setStandardButtons(QMessageBox.StandardButton.Ok)
    msg.exec()


class AnotherWindow(QWidget):
    def __init__(self, description, image_name):
        super().__init__()
        self.image_name = image_name
        print(self.image_name)
        self.setWindowTitle('PyQt QTabWidget')
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        tab = QTabWidget(self)
        # Text tab
        text_page = QWidget(self)
        layout = QFormLayout()
        text_page.setLayout(layout)
        self.description = description
        self.text_browser = QTextBrowser()
        self.text_browser.setText(description)
        layout.addWidget(self.text_browser)
        # Image tab
        image_page = QWidget(self)
        layout = QFormLayout()
        self.im = QPixmap(PATH + "Images\\" + self.image_name)
        self.label = QLabel()
        self.label.setPixmap(self.im)
        layout.addWidget(self.label)
        image_page.setLayout(layout)
        tab.addTab(text_page, 'Text')
        tab.addTab(image_page, 'Image')
        main_layout.addWidget(tab, 0, 0, 2, 1)
        self.setGeometry(500, 300, 400, 500)
        self.show()


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
        self.combobox = QComboBox()
        self.combobox.addItem('Информация')
        self.combobox.addItem('О приложении')
        self.combobox.addItem('Вопросы которые могут возникнуть')
        self.combobox.addItem('Связь')
        self.combobox.setObjectName('myComboBox')
        self.combobox.currentIndexChanged.connect(self.on_combobox_changed)
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
        info_tab = QWidget()
        info_layout = QVBoxLayout()
        self.save_line_edit = QLineEdit()
        self.nameLabel = QLabel(self)
        self.save_line_edit.setPlaceholderText("Имя Гамбита")
        self.save_area_edit = QPlainTextEdit()
        self.save_area_edit.setPlaceholderText("Информация про Гамбит")
        self.save_photo_name_edit = QLineEdit()
        self.save_photo_name_edit.setPlaceholderText("Имя изображения")
        info_layout.addWidget(self.save_line_edit)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_base)
        info_layout.addWidget(self.save_area_edit)
        info_layout.addWidget(self.save_photo_name_edit)
        info_layout.addWidget(save_button)
        info_tab.setLayout(info_layout)
        gambits_tab = QWidget()
        gambits_layout = QVBoxLayout()
        self.gambits_list = QListWidget()
        self.gambits_list.addItems(self.get_all())
        gambits_layout.addWidget(self.gambits_list)
        gambits_tab.setLayout(gambits_layout)
        self.gambits_list.itemDoubleClicked.connect(self.doubleclickmouse)
        tabs.addTab(search_tab, "Поиск")
        tabs.addTab(info_tab, "Добавление данных")
        tabs.addTab(gambits_tab, "Гамбиты")
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.combobox)
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)
        self.setGeometry(300, 100, 400, 500)
        self.setWindowTitle('Гамбит')
        self.show()

    def on_combobox_changed(self, index):
        if index == 1:
            msg = QMessageBox.information(self, 'О приложении', "В нашем приложении вы можете:\n"
        "- Ввести название дебюта или гамбита в поисковую строку и получить информацию.\n"
        "- Во второй вкладке пополнить базу данных новой информацией.\n"
        "- В третьей вкладке просмотреть содержимое базы данных.\n"
        "- Двойной клик на элемент откроет новое окно с подробностями и изображением.\n"
    )
        elif index == 2:
            msg = QMessageBox.warning(self, 'Вопросы', "При работе с приложением у вас могут быть вопросы:\n"
        "- Что будет если я неправильно введу имя Гамбита или Дебюта?\n"
        "- Ничего страшного не случится.У вас просто появится сообщение о ошибке что нет гамбита данного\n"
        "- Что если я хочу увидеть не только чистую информацию про гамбит но и картинку?\n"
        "- Откройте третию вкладку и сделайте двойной клик по элементу.Тогда откроется окно с картинкой и данными\n"
        "- Я не знаю не одного названия.Что делать?\n"
        "- Откройте последнюю Гамбиты.Там будут данные из БД. Двойной клик на элемент откроет новое окно с данными.\n"
        "- Зачем нужна вкладка с добовление информации?\n"
        "- Данная вкладка нужна для добовлении данных в БД если вы что-то не смогли найти. \n"
        "- Таким образом вы сможете сами внести вклад в развитие проекта! \n"
        "- Как с вами связаться?\n"
        "- В том же dropbox есть вкладка связь. Нажмите на неё и вы увидете почту по который вы можете связаться\n"
    )
        elif index == 3:
            msg = QMessageBox.warning(self, 'Связь', "Если вы не нашли ответ на вопрос или что-то еще.\n"
        "-То вы можете спокойно с нами связаться. \n"
        "-Вот наша почта:********@neyandex.ru \n"
        "- Мы не на связи 24/7.\n"
        "- Обращайтесь если найдете недостатки или будут вопросы на которые нет ответа.\n"
        "- Ответ вам придет через 50 лет ожидания\n"
    )


    def search(self):
        search_text = "%" + self.search_line_edit.text().lower() + "%"
        result = cur.execute(
            """select * from gambit where name  like  ?""", (search_text,)).fetchone()
        self.history_list.clear()
        if result is not None:
            self.history_list.setText(result[2])
        else:
            self.history_list.setText("Ошибка, Гамбит не был обнаружен")

    def save_base(self):
        save_textfl = self.save_line_edit.text().lower()
        save_textsl = self.save_area_edit.toPlainText()
        save_photo = self.save_photo_name_edit.text()
        try:
            save = cur.execute(
                """INSERT INTO gambit(name, description, image_fnane) VALUES(?,?,?); """
                               , (save_textfl, save_textsl, save_photo))
            con.commit()
        except:
            QMessageBox.warning(self, "Ошибка", " Не удалось сделать сохранение информации в базу данных")

    def doubleclickmouse(self, item):
        clicked_name = item.text()
        result = cur.execute(
            """select * from gambit where name = ?""",
            (clicked_name,)
        ).fetchone()
        if result is not None:
            self.w = AnotherWindow(result[2], result[3])
            self.w.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Гамбит не найден")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme='light_cyan_500.xml')
    show_welcome_message()
    ex = GambitWindow()
    sys.exit(app.exec())
