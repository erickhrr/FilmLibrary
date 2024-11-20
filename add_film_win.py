from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QComboBox, QVBoxLayout
from PyQt6.QtWidgets import QPushButton, QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from database import add_movie_to_db


class AddFilmWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Добавить фильм")
        self.setGeometry(100, 100, 400, 400)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFE4E1; /* Розовый фон */
                color: #800000; /* Темно-розовый текст */
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLineEdit, QComboBox {
                border: 1px solid #800000;
                border-radius: 5px;
                padding: 5px;
            }
            QComboBox::drop-down {
                border-left: 1px solid #800000;
            }
            QComboBox::down-arrow {
                width: 10px;
                height: 10px;
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
        """)

        # Основной layout
        layout = QVBoxLayout()

        # Поле загрузки постера
        self.poster_label = QLabel("Постер:")
        self.poster_preview = QLabel("Постер не выбран")
        self.poster_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.poster_preview.setStyleSheet("border: 1px dashed #800000; padding: 10px;")
        self.poster_preview.setFixedHeight(150)
        self.upload_button = QPushButton("Загрузить постер")
        self.upload_button.clicked.connect(self.upload_poster)

        # Поле для ввода названия
        self.title_label = QLabel("Название:")
        self.title_input = QLineEdit()

        # Поле для ввода года
        self.year_label = QLabel("Год:")
        self.year_input = QLineEdit()

        # Поле для ввода страны
        self.country_label = QLabel("Страна:")
        self.country_input = QLineEdit()

        # Поле выбора жанра
        self.genre_label = QLabel("Жанр:")
        self.genre_combo = QComboBox()
        self.genre_combo.addItems([
            "Хоррор", "Комедия", "Драма", "Экшн", "Приключения", "Фантастика",
            "Триллер", "Мелодрама", "Анимация", "Документальный", "Фэнтези",
            "Криминал", "Исторический", "Детектив", "Биография"
        ])
        #Поле Режиссер
        self.director_label = QLabel("Режиссер:")
        self.director_input = QLineEdit()

        #Поле Страна
        self.country_label = QLabel("Страна:")
        self.country_input = QLineEdit()

        # Кнопка добавления фильма
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.save_movie)

        # Добавляем элементы в layout
        layout.addWidget(self.poster_label)
        layout.addWidget(self.poster_preview)
        layout.addWidget(self.upload_button)
        layout.addWidget(self.title_label)
        layout.addWidget(self.title_input)
        layout.addWidget(self.year_label)
        layout.addWidget(self.year_input)
        layout.addWidget(self.country_label)
        layout.addWidget(self.country_input)
        layout.addWidget(self.genre_label)
        layout.addWidget(self.genre_combo)
        layout.addWidget(self.director_label)
        layout.addWidget(self.director_input)
        layout.addWidget(self.country_input)
        layout.addWidget(self.country_label)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

        # Переменная для хранения пути постера
        self.poster_path = None

    def upload_poster(self):
        # Открытие диалога выбора файла с обработкой ошибок.
        try:
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Выберите постер", "", "Images (*.jpg *.jpeg)"
            )
            if file_path:
                self.poster_path = file_path
                pixmap = QPixmap(file_path)

                # Проверка, успешно ли загружено изображение
                if pixmap.isNull():
                    QMessageBox.warning(self, "Ошибка", "Не удалось загрузить изображение!")
                    self.poster_path = None
                    return

                # Масштабирование изображения для предпросмотра
                scaled_pixmap = pixmap.scaled(
                    200, 150, Qt.AspectRatioMode.KeepAspectRatio
                )
                self.poster_preview.setPixmap(scaled_pixmap)
            else:
                # Если пользователь нажал "Отмена"
                print("Пользователь не выбрал изображение.")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def save_movie(self):
        title = self.title_input.text()
        year = self.year_input.text()
        genre = self.genre_combo.currentText()
        director = self.director_input.text()
        country = self.country_input.text()

        if not title or not year or not country or not genre or not director:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        # Чтение данных постера
        poster_data = None
        if self.poster_path:
            with open(self.poster_path, "rb") as file:
                poster_data = file.read()

        # Вызов функции из database.py
        add_movie_to_db(poster_data, title, year, genre, director, country)
        QMessageBox.information(self, "Успех", "Фильм добавлен!")

        # Очистка полей
        self.poster_preview.setPixmap(QPixmap())
        self.poster_preview.setText("Нет изображения")
        self.title_input.clear()
        self.year_input.clear()
        self.genre_combo.setCurrentIndex(0)
        self.director_input.clear()
        self.country_input.clear()
