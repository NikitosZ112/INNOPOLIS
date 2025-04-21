from models import LibraryDB
from getpass import getpass


def get_db_url():
    """Получение параметров подключения к базе данных"""
    print("=== Подключение к PostgreSQL ===")
    host = input("Хост: ") or "localhost"
    port = input("Порт: ") or "5432"
    dbname = input("Имя базы данных: ") or "postgres"
    user = input("Пользователь: ") or "postgres"
    password = input("Пароль: ")

    return f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"


def main():
    """Основная функция работы с библиотекой"""
    db_url = get_db_url()
    db = LibraryDB(db_url)

    while True:
        print("\n=== Система управления библиотекой ===")
        print("1. Добавить книгу")
        print("2. Зарегистрировать читателя")
        print("3. Выдать книгу")
        print("4. Вернуть книгу")
        print("5. Список всех книг")
        print("6. Поиск книг")
        print("7. Выход")

        choice = input("Выберите действие: ")

        if choice == '1':
            title = input("Название: ")
            author = input("Автор: ")
            year = input("Год издания (необязательно): ") or None
            quantity = input("Количество [1]: ") or "1"

            if db.add_book(title, author, year, int(quantity)):
                print("Книга успешно добавлена")

        elif choice == '2':
            name = input("Имя: ")
            email = input("Email: ")

            if db.register_reader(name, email):
                print("Читатель зарегистрирован")


        elif choice == '3':

            # Показываем доступные книги

            available_books = db.get_available_books()

            if not available_books:
                print("\nНет доступных книг для выдачи")

                continue

            print("\nДоступные книги:")

            for book in available_books:
                status = db.get_book_status(book.id)

                print(f"{book.id}: {book.title} - {book.author} | {status['status']}")

            # Запрос ID книги

            book_id = input("\nВведите ID книги для выдачи: ")

            if not book_id.isdigit():
                print("Ошибка: введите числовой ID")

                continue

            # Запрос ID читателя

            reader_id = input("Введите ID читателя: ")

            if not reader_id.isdigit():
                print("Ошибка: введите числовой ID")

                continue

            # Проверка читателя

            reader_info = db.get_reader_with_books(int(reader_id))

            if not reader_info:
                print("Читатель не найден")

                continue

            reader, current_borrowed = reader_info

            print(f"\nЧитатель: {reader.name}")

            print(f"Уже взято книг: {len(current_borrowed)}")

            # Выдача книги

            if db.borrow_book(int(book_id), int(reader_id)):
                print("Книга успешно выдана")

                # Обновляем статус

                status = db.get_book_status(int(book_id))

                print(f"Текущий статус книги: {status['status']}")

        elif choice == '4':
            borrow_id = input("ID записи о выдаче: ")

            if db.return_book(int(borrow_id)):
                print("Книга возвращена")

        elif choice == '5':
            books = db.get_all_books()
            print("\nВсе книги в библиотеке:")
            for book in books:
                print(f"{book.id}: {book.title} - {book.author} ({book.published_year}) - Доступно: {book.quantity}")

        elif choice == '6':
            query = input("Поиск (название или автор): ")
            books = db.search_books(query)
            print("\nРезультаты поиска:")
            for book in books:
                print(f"{book.id}: {book.title} - {book.author}")

        elif choice == '7':
            print("До свидания!")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()