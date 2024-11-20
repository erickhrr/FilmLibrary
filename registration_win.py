from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QApplication, QMessageBox
from database import add_user


class RegistrationWindow(QWidget):
    registration_complete = pyqtSignal()  # Сигнал завершения регистрации
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Регистрация пользователя')

        self.name_label = QLabel('Имя пользователя:')
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Введите имя пользователя')

        self.password_label = QLabel('Пароль:')
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText('Введите пароль')

        self.register_button = QPushButton('Зарегистрироваться')

        self.register_button.clicked.connect(self.register_user)

        self.setStyleSheet("""
            QWidget {
                background-color: #FFE4E1; /* Розовый фон */
                color: #800000; /* Темно-розовый текст */
                font-family: Arial, sans-serif;
                font-size: 14px;
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

        layout = QVBoxLayout()
        layout.addWidget(self.name_label)
        layout.addWidget(self.name_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register_user(self):
        username = self.name_input.text()
        password = self.password_input.text()

        if username and password:
            add_user(username, password)
            self.registration_complete.emit()
        else:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля!")
            return

        # Очистка полей
        self.password_input.clear()
        self.name_input.clear()
        self.close()
