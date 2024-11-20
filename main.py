import sys
from PyQt6.QtWidgets import QApplication
from main_win import MainWindow
from registration_win import RegistrationWindow
from folders_win import FoldersWindow
from add_film_win import AddFilmWindow
from search_film_win import AdvancedSearchWindow


class ApplicationController:
    """Контроллер для управления окнами приложения."""

    def __init__(self):
        self.app = QApplication(sys.argv)

        # Инициализация окон
        self.registration_window = RegistrationWindow()
        self.main_window = MainWindow()
        self.folders_window = None  # Создается при необходимости
        self.add_film_window = None  # Создается при необходимости
        self.search_window = None  # Создается при необходимости

        # Связывание сигналов с действиями
        self.setup_connections()

    def setup_connections(self):
        """Настройка связей между окнами."""
        # Открытие главного окна после регистрации
        self.registration_window.registration_complete.connect(self.show_main_window)

        # Связывание кнопок в главном окне с другими окнами
        self.main_window.open_folders.connect(self.show_folders_window)
        self.main_window.open_add_movie.connect(self.show_add_film_window)
        self.main_window.open_search.connect(self.show_search_window)

    def show_main_window(self):
        """Показать главное окно."""
        self.registration_window.close()  # Закрываем окно регистрации
        self.main_window.show()

    def show_folders_window(self):
        """Открывает окно 'Папки'."""
        if not self.folders_window:
            self.folders_window = FoldersWindow()
        self.folders_window.show()

    def show_add_film_window(self):
        """Открывает окно 'Добавить фильм'."""
        if not self.add_film_window:
            self.add_film_window = AddFilmWindow()
        self.add_film_window.show()

    def show_search_window(self):
        """Открывает окно 'Поиск фильмов'."""
        if not self.search_window:
            self.search_window = AdvancedSearchWindow()
        self.search_window.show()

    def run(self):
        """Запуск приложения."""
        self.registration_window.show()  # Начинаем с окна регистрации
        sys.exit(self.app.exec())


if __name__ == "__main__":
    controller = ApplicationController()
    controller.run()
