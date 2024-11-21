from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel
from PyQt6.QtWidgets import QComboBox, QHBoxLayout, QSizePolicy, QFrame
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QScrollArea
from PyQt6.QtGui import QPixmap
from database import search_film


class AdvancedSearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расширенный поиск")
        self.setGeometry(300, 200, 400, 300)

        # Розовый стиль
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
            QLabel {
                font-size: 16px;
                font-weight: bold;
            }
        """)

        # Переменные для хранения значений
        self.title_value = None
        self.year_value = None
        self.country_value = None
        self.genre_value = None

        # Создаем элементы
        self.init_ui()

    def init_ui(self):
        # Поля ввода
        self.title_label = QLabel("Название:")
        self.title_input = QLineEdit()

        self.year_label = QLabel("Год:")
        self.year_input = QLineEdit()

        self.country_label = QLabel("Страна:")
        self.country_input = QLineEdit()

        # Поле выбора Жанра
        self.genre_label = QLabel("Жанр:")
        self.genre_combo = QComboBox()
        genres = [
            "", "Хоррор", "Комедия", "Драма", "Боевик", "Триллер", "Фантастика", "Фэнтези",
            "Мелодрама", "Приключения", "Анимация", "Мюзикл", "Документальный",
            "Детектив", "Исторический", "Криминал"
        ]
        self.genre_combo.addItems(genres)

        # Кнопка для сохранения введенных данных
        self.save_button = QPushButton("Искать")
        self.save_button.clicked.connect(self.save_values)

        # Сетки расположения
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)

        title_layout = QHBoxLayout()
        title_layout.addWidget(self.title_label)
        title_layout.addWidget(self.title_input)

        year_layout = QHBoxLayout()
        year_layout.addWidget(self.year_label)
        year_layout.addWidget(self.year_input)

        country_layout = QHBoxLayout()
        country_layout.addWidget(self.country_label)
        country_layout.addWidget(self.country_input)

        genre_layout = QHBoxLayout()
        genre_layout.addWidget(self.genre_label)
        genre_layout.addWidget(self.genre_combo)

        # Добавляем все элементы в общий макет
        main_layout.addLayout(title_layout)
        main_layout.addLayout(year_layout)
        main_layout.addLayout(country_layout)
        main_layout.addLayout(genre_layout)
        main_layout.addWidget(self.save_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

    def save_values(self):
        # Сохранение введенных значений в переменные и запуск поиска.
        title = self.title_input.text()
        year = self.year_input.text()
        country = self.country_input.text()
        genre = self.genre_combo.currentText()

        # Запрос к базе данных
        movies = search_film(title, year, country, genre)
        if movies:
            self.results_window = FilmResultsWindow(movies)
            self.results_window.show()
        else:
            print("Фильмы не найдены!")

        # Очистка полей
        self.title_input.clear()
        self.year_input.clear()
        self.country_input.clear()
        self.genre_combo.setCurrentIndex(0)


class FilmResultsWindow(QWidget):
    def __init__(self, search_results):
        super().__init__()

        self.setWindowTitle("Результаты поиска")
        self.setGeometry(100, 100, 800, 600)

        # Применяем розовый стиль
        self.setStyleSheet("""
            QWidget {
                background-color: #FFE4E1; /* Розовый фон */
                color: #800000; /* Темно-розовый текст */
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
            }
            QLabel#movie_info {
                font-size: 12px;
                font-weight: normal;
                color: #800000;
            }
            QLabel#poster {
                border: 1px solid #800000;
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
        """)

        # Основной layout
        self.layout = QVBoxLayout(self)

        # Заголовок
        title_label = QLabel("Результаты поиска:")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(title_label)

        # Прокручиваемая область для результатов
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QFrame()
        self.scroll_layout = QVBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)
        self.layout.addWidget(self.scroll_area)

        # Добавляем результаты поиска
        self.add_results(search_results)

    def add_results(self, search_results):
        """Добавляет фильмы в интерфейс."""
        for movie in search_results:
            movie_layout = QHBoxLayout()

            # Постер фильма
            if movie.poster:
                poster_pixmap = QPixmap()
                poster_pixmap.loadFromData(movie.poster)
                poster_label = QLabel()
                poster_label.setPixmap(poster_pixmap.scaledToHeight(150, Qt.TransformationMode.SmoothTransformation))
                poster_label.setObjectName("poster")
                poster_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            else:
                poster_label = QLabel("Нет постера")
                poster_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                poster_label.setFixedSize(100, 150)
                poster_label.setObjectName("poster")
            movie_layout.addWidget(poster_label)

            # Информация о фильме
            info_layout = QVBoxLayout()
            info_label = QLabel(
                f"<b>Название:</b> {movie.title}<br>"
                f"<b>Год:</b> {movie.year}<br>"
                f"<b>Жанр:</b> {movie.genre}<br>"
                f"<b>Режиссер:</b> {movie.director}<br>"
                f"<b>Страна:</b> {movie.country}"
            )
            info_label.setObjectName("movie_info")
            info_label.setWordWrap(True)
            info_layout.addWidget(info_label)

            # Растягиваем информацию на всю оставшуюся ширину
            info_layout.addStretch()
            movie_layout.addLayout(info_layout)

            # Добавляем элемент в прокручиваемый список
            self.scroll_layout.addLayout(movie_layout)

        # Растягиваем элементы по высоте
        self.scroll_layout.addStretch()
