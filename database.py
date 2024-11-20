from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Movie, User, Folder
import io # Модуль для упрощенной работы с файлами
from PIL import Image

# Настройка подключения к базе данных SQLite
DATABASE_URL = "sqlite:///film_library.db"  # Имя файла базы данных
engine = create_engine(DATABASE_URL, echo=True)  # echo=True выводит SQL-запросы в консоль

# Макет функции добавляющей новую таблицу в БД
def create_new_table():
    from models import FolderToFilm
    try:
        FolderToFilm.__table__.create(bind=engine, checkfirst=True)
        print(f"Новая таблица в БД успешно создана!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при создании новой таблицы в БД: {e}")

# Создание таблиц в базе данных
Base.metadata.create_all(engine)

# Настройка сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# Добавление новых фильмов в таблицу 'movie' через окно AddFilmWindow
def add_movie_to_db(poster_data, title, year, genre, director, country):
    new_movie = Movie(
        poster=poster_data,
        title=title,
        year=year,
        genre=genre,
        director=director,
        country=country
    )
    try:
        session.add(new_movie)
        session.commit()
        print(f"Фильм {title} успешно добавлен!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении фильма: {e}")

def add_folder(name):
    new_folder = Folder(name=name)
    try:
        session.add(new_folder)
        session.commit()
        print(f"Папка {name} успешно добавлена!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при добавлении папки: {e}")

# Добавление новых пользователей в таблицу 'users' через окно RegistrationWindow
def add_user(username, password):
    # Создание нового пользователя
    new_user = User(username=username, password=password)
    try:
        session.add(new_user)
        session.commit()
        print(f"Пользователь {username} зарегистрирован!")
    except Exception as e:
        session.rollback()
        print(f"Ошибка при регистрации: {e}")

# Поиск фильмов
def search_film(title, year, country, genre):
    query = session.query(Movie)
    if title:
        query = query.filter(Movie.title.ilike(f"%{title}%"))
    if year:
        query = query.filter(Movie.year == int(year))
    if country:
        query = query.filter(Movie.country.ilike(f"%{country}%"))
    if genre:
        query = query.filter(Movie.genre.ilike(f"%{genre}%"))

    movies = query.all()
    return movies

def delete_movie(movie_id):
    # Находим фильм по ID
    movie_to_delete = session.query(Movie).filter(Movie.id == movie_id).first()

    if movie_to_delete:
        # Удаляем найденную запись
        session.delete(movie_to_delete)
        session.commit()
        print(f"Фильм с ID {movie_id} был успешно удален.")

def delete_user(user_id):
    user_to_delete = session.query(User).filter(User.id == user_id).first()

    if user_to_delete:
        session.delete(user_to_delete)
        session.commit()
        print(f"Пользователь с ID {user_id} был успешно удален.")

def show_movie_and_user_info():
    # Получаем информацию о фильмах
    movies = session.query(Movie).all()
    if movies:
        print("\nТестовые фильмы в базе данных:")
        for movie in movies:
            print(f"ID: {movie.id}, Title: {movie.title}, Year: {movie.year}")
            if movie.poster:
                image = Image.open(io.BytesIO(movie.poster))
                image.show()  # Показываем постер
            else:
                print("Нет постера для этого фильма.")
    else:
        print("Нет фильмов в базе данных.")

    # Получаем информацию о пользователях
    users = session.query(User).all()
    if users:
        print("\nПользователи в базе данных:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}")
    else:
        print("Нет пользователей в базе данных.")
    folders = session.query(Folder).all()
    if folders:
        print("\nПапки в базе данных:")
        for folder in folders:
            print(f"ID: {folder.id}, Name: {folder.name}")

def get_folders_from_db():
    return session.query(Folder).all()

def check_unique(folder_name):
    return session.query(Folder).filter_by(name=folder_name).first()


if __name__ == "__main__":
    show_movie_and_user_info()