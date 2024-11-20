from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Movie(Base):
    __tablename__ = 'movie'  # Название таблицы в БД

    id = Column(Integer, primary_key=True, autoincrement=True)  # Ключ
    poster = Column(LargeBinary, nullable=True)  # Поле для хранения изображения (постера)
    title = Column(String, nullable=False)  # Название фильма
    year = Column(Integer, nullable=False)  # Год выхода фильма
    genre = Column(String, nullable=False)  # Жанр фильма
    director = Column(String, nullable=False)  # Режиссер фильма
    country = Column(String, nullable=False)  # Страна производства

    movie_folders = relationship("FolderToFilm", back_populates="movie")


class User(Base):
    __tablename__ = 'users'  # Название таблицы в БД

    id = Column(Integer, primary_key=True, autoincrement=True)  # Ключ
    username = Column(String, unique=True, nullable=False)  # Имя пользователя
    password = Column(String, nullable=False)  # Пароль пользователя


class Folder(Base):
    __tablename__ = 'folders' # Название таблицы в БД

    id = Column(Integer, primary_key=True, autoincrement=True) # Ключ
    name = Column(String, unique=True, nullable=False) # Название папки (уникальное поле)

    folder_movies = relationship("FolderToFilm", back_populates="folder")


class FolderToFilm(Base):
    __tablename__ = 'folder_to_film' # Название таблицы в БД

    folder_id = Column(Integer, ForeignKey('folders.id'), primary_key=True)
    movie_id = Column(Integer, ForeignKey('movie.id'), primary_key=True)

    folder = relationship("Folder", back_populates="folder_movies")
    movie = relationship("Movie", back_populates="movie_folders")
