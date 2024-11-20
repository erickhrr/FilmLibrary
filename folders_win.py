from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox, QScrollArea, QFrame
)
from database import add_folder, get_folders_from_db, check_unique


class FoldersWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Папки")
        self.setGeometry(100, 100, 400, 500)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFE4E1; /* Розовый фон */
                color: #800000; /* Темно-розовый текст */
                font-family: Arial, sans-serif;
                font-size: 14px;
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
            QPushButton:pressed {
                background-color: #e04d71;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
            QLineEdit {
                border: 1px solid #800000;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        # Основной layout
        self.layout = QVBoxLayout(self)

        # Заголовок
        self.title_label = QLabel("Ваши папки:")
        self.layout.addWidget(self.title_label)

        # Прокручиваемая область для папок
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Поле ввода для добавления новой папки
        self.new_folder_input = QLineEdit()
        self.new_folder_input.setPlaceholderText("Введите название новой папки")
        self.layout.addWidget(self.new_folder_input)

        # Кнопка добавления новой папки
        self.add_folder_button = QPushButton("Добавить папку")
        self.add_folder_button.clicked.connect(self.add_folder)
        self.layout.addWidget(self.add_folder_button)

        # Загрузка папок из базы данных
        self.load_folders()

    def load_folders(self):
        # Загружает список папок из базы данных и обновляет интерфейс.
        # Очищаем layout перед обновлением
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Получаем папки из базы данных
        folders = get_folders_from_db()
        for folder in folders:
            folder_button = QPushButton(folder.name)
            folder_button.setToolTip(f"Папка: {folder.name}")
            folder_button.clicked.connect(lambda _, f=folder.name: self.open_folder(f))
            self.scroll_layout.addWidget(folder_button)

    def add_folder(self):
        # Добавляет новую папку в базу данных.
        folder_name = self.new_folder_input.text().strip()
        if not folder_name:
            QMessageBox.warning(self, "Ошибка", "Название папки не может быть пустым!")
            return

        # Проверяем уникальность названия папки
        if check_unique(folder_name):
            QMessageBox.warning(self, "Ошибка", "Папка с таким названием уже существует!")
            return

        # Добавляем папку в базу данных
        add_folder(folder_name)

        # Очищаем поле ввода и обновляем список папок
        self.new_folder_input.clear()
        self.load_folders()
        QMessageBox.information(self, "Успех", f"Папка '{folder_name}' успешно добавлена!")

    def open_folder(self, folder_name):
        # Обработчик нажатия на кнопку папки.
        QMessageBox.information(self, "Папка", f"Открыта папка: {folder_name}")
