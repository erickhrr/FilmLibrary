from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QMenu, QLabel)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal


class MainWindow(QMainWindow):
    open_folders = pyqtSignal()  # Сигнал для открытия окна "Папки"
    open_add_movie = pyqtSignal()  # Сигнал для открытия окна "Добавить фильм"
    open_search = pyqtSignal()  # Сигнал для открытия окна "Поиск фильмов"

    def __init__(self):
        super().__init__()

        # Применение стиля
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFE4E1; /* Розовый фон */
            }
            QPushButton {
                background-color: #800000;
                color: #FFE4E1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #800000;
            }
        """)

        # Настройка основного окна
        self.setWindowTitle("Главная")
        self.setGeometry(100, 100, 600, 400)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Верхний бар с кнопками
        self.create_menu(layout)
        self.create_search_button(layout)

        # Заглушка для отображения текста на главной странице
        self.main_label = QLabel("Добро пожаловать в главное окно!")
        self.main_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.main_label)

    def create_menu(self, layout):
        # Создание кнопки Меню с выпадающим списком
        menu_button = QPushButton("Меню")
        menu_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: #FFE4E1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
        """)

        # Создание выпадающего меню
        menu = QMenu()
        menu.setStyleSheet("""
            QMenu {
                background-color: #FFE4E1; /* Розовый фон меню */
                color: #800000; /* Текст меню */
                border: 1px solid #800000; /* Граница меню */
            }
            QMenu::item {
                background-color: transparent; /* Прозрачный фон по умолчанию */
                padding: 5px 10px; /* Отступы внутри элементов */
            }
            QMenu::item:selected {
                background-color: #FFCCCC; /* Светло-розовый при наведении */
                color: #800000; /* Цвет текста при наведении */
            }  
        """)
        folders_action = QAction("Папки", self)
        add_movie_action = QAction("Добавить", self)

        # Добавление действий в меню
        menu.addAction(folders_action)
        menu.addAction(add_movie_action)

        # Подключение сигналов для каждого действия
        folders_action.triggered.connect(self.open_folders)
        add_movie_action.triggered.connect(self.open_add_film_window)

        # Привязка меню к кнопке
        menu_button.setMenu(menu)
        layout.addWidget(menu_button)

    def open_folders_window(self):
        self.open_folders.emit()

    def open_add_film_window(self):
        self.open_add_movie.emit()

    def create_search_button(self, layout):
        # Создание кнопки поиска фильмов
        search_button = QPushButton("Поиск Фильмов")
        search_button.setStyleSheet("""
            QPushButton {
                background-color: #800000;
                color: #FFE4E1;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6666;
            }
            QPushButton:pressed {
                background-color: #e04d71;
            }
        """)
        search_button.clicked.connect(self.open_search_window)
        layout.addWidget(search_button)

    def open_search_window(self):
        self.open_search.emit()

    def show_message(self, message):
        # Отображение сообщения в заглушке
        self.main_label.setText(message)
