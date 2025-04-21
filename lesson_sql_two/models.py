from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, CheckConstraint, text
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import sys

# Базовый класс для моделей
Base = declarative_base()


class Book(Base):
    """Модель книги с информацией о выдаче"""
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    author = Column(String(50), nullable=False)
    published_year = Column(Integer)
    quantity = Column(Integer, nullable=False)
    total_copies = Column(Integer)  # Общее количество экземпляров

    # Связь с записями о выдаче
    borrowings = relationship("BorrowedBook", back_populates="book")

    __table_args__ = (
        CheckConstraint('quantity >= 0', name='quantity_check'),
    )

    def get_availability_status(self):
        """Получение статуса доступности"""
        if self.quantity > 0:
            return f"В наличии ({self.quantity} из {self.total_copies})"
        return "Нет в наличии"


class Reader(Base):
    """Модель читателя с информацией о взятых книгах"""
    __tablename__ = 'readers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    borrowed_books = relationship("BorrowedBook", back_populates="reader")

    def get_borrowed_books_info(self, session):
        """Получение информации о взятых книгах"""
        return session.query(BorrowedBook, Book).join(Book).filter(
            BorrowedBook.reader_id == self.id,
            BorrowedBook.return_date == None
        ).all()


class BorrowedBook(Base):
    """Модель выданной книги с расширенной информацией"""
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey('books.id'))
    reader_id = Column(Integer, ForeignKey('readers.id'))
    borrow_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime)
    due_date = Column(DateTime)

    # Связи
    book = relationship("Book", back_populates="borrowings")
    reader = relationship("Reader", back_populates="borrowed_books")

class LibraryDB:
    """Класс для работы с базой данных библиотеки"""
    def __init__(self, db_url):
        try:
            self.engine = create_engine(db_url, echo=False)
            self._test_connection()
            self.Session = sessionmaker(bind=self.engine)
            self._create_tables()
        except SQLAlchemyError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            sys.exit(1)

    def _test_connection(self):
        """Проверка соединения с базой данных"""
        with self.engine.connect() as conn:
            conn.execute(text("SELECT 1"))

    def _create_tables(self):
        """Создание таблиц в базе данных"""
        Base.metadata.create_all(self.engine)

    def _get_session(self):
        """Получение новой сессии"""
        return self.Session()

    def add_book(self, title, author, published_year=None, quantity=1):
        """Добавление новой книги"""
        with self._get_session() as session:
            try:
                if session.query(Book).filter_by(title=title, author=author).first():
                    print("Книга с таким названием и автором уже существует")
                    return False

                book = Book(title=title, author=author,
                          published_year=published_year, quantity=quantity)
                session.add(book)
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False

    def register_reader(self, name, email):
        """Регистрация нового читателя"""
        with self._get_session() as session:
            try:
                if session.query(Reader).filter_by(email=email).first():
                    print("Читатель с таким email уже зарегистрирован")
                    return False

                reader = Reader(name=name, email=email)
                session.add(reader)
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False

    def borrow_book(self, book_id, reader_id):
        """Выдача книги читателю"""
        with self._get_session() as session:
            try:
                book = session.query(Book).filter_by(id=book_id).with_for_update().first()
                if not book or book.quantity <= 0:
                    print("Книга недоступна для выдачи")
                    return False

                book.quantity -= 1
                borrowed = BorrowedBook(book_id=book_id, reader_id=reader_id)
                session.add(borrowed)
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False

    def return_book(self, borrow_id):
        """Возврат книги в библиотеку"""
        with self._get_session() as session:
            try:
                borrow = session.query(BorrowedBook).filter_by(id=borrow_id, return_date=None).first()
                if not borrow:
                    print("Активная запись о выдаче не найдена")
                    return False

                book = session.query(Book).filter_by(id=borrow.book_id).first()
                if book:
                    book.quantity += 1

                borrow.return_date = datetime.utcnow()
                session.commit()
                return True
            except SQLAlchemyError:
                session.rollback()
                return False

    def get_all_books(self):
        """Получение списка всех книг"""
        with self._get_session() as session:
            return session.query(Book).order_by(Book.published_year).all()

    def search_books(self, query):
        """Поиск книг по названию или автору"""
        with self._get_session() as session:
            return session.query(Book).filter(
                Book.title.ilike(f"%{query}%") |
                Book.author.ilike(f"%{query}%")
            ).all()

    def get_reader_with_books(self, reader_id):
        """Получение информации о читателе с взятыми книгами"""
        with self._get_session() as session:
            reader = session.query(Reader).get(reader_id)
            if not reader:
                return None

            borrowed = reader.get_borrowed_books_info(session)
            return reader, borrowed

    def get_book_status(self, book_id):
        """Получение полного статуса книги"""
        with self._get_session() as session:
            book = session.query(Book).get(book_id)
            if not book:
                return None

            borrowings = session.query(BorrowedBook).filter(
                BorrowedBook.book_id == book_id,
                BorrowedBook.return_date == None
            ).all()

            return {
                'book': book,
                'status': book.get_availability_status(),
                'borrowed_count': len(borrowings),
                'borrowings': borrowings
            }