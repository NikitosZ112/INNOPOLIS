import json
import os

class Book:
    """Класс для представления книги"""

    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

    def __repr__(self):
        return f"Книга: {self.title} (Автор: {self.author}, Год: {self.year})"


# Алгоритмы сортировки
def quick_sort(books, key):
    """Быстрая сортировка"""
    if len(books) <= 1:
        return books
    pivot = books[len(books) // 2]
    left = [book for book in books if getattr(book, key) < getattr(pivot, key)]
    middle = [book for book in books if getattr(book, key) == getattr(pivot, key)]
    right = [book for book in books if getattr(book, key) > getattr(pivot, key)]
    return quick_sort(left, key) + middle + quick_sort(right, key)


def merge_sort(books, key):
    """Сортировка слиянием"""
    if len(books) <= 1:
        return books

    mid = len(books) // 2
    left = merge_sort(books[:mid], key)
    right = merge_sort(books[mid:], key)

    return merge(left, right, key)


def merge(left, right, key):
    result = []
    while left and right:
        if getattr(left[0], key) <= getattr(right[0], key):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right

# Функция пирамидальной сортировки
def heapify(books, n, i, key):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and getattr(books[left], key) > getattr(books[largest], key):
        largest = left
    if right < n and getattr(books[right], key) > getattr(books[largest], key):
        largest = right
    if largest != i:
        books[i], books[largest] = books[largest], books[i]
        heapify(books, n, largest, key)

def heap_sort(books, key):
    n = len(books)
    for i in range(n // 2 - 1, -1, -1):
        heapify(books, n, i, key)
    for i in range(n - 1, 0, -1):
        books[i], books[0] = books[0], books[i]
        heapify(books, i, 0, key)

    return books


# Работа с файлами
def save_library(library, filename='library.json'):
    """Сохранение библиотеки в файл"""
    data = [{'title': b.title, 'author': b.author, 'year': b.year} for b in library]
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)


def load_library(filename='library.json'):
    """Загрузка библиотеки из файла"""
    if not os.path.exists(filename):
        return []
    with open(filename, encoding='utf-8') as f:
        data = json.load(f)
    return [Book(item['title'], item['author'], item['year']) for item in data]


# Основная логика
class LibraryManager:
    def __init__(self):
        # Попытка загрузить библиотеку из файла
        self.library = self.load_library()

        # Если библиотека пустая, добавляем начальные книги
        if not self.library:
            self.library = [
                Book("Война и мир", "Лев Толстой", 1869),
                Book("1984", "Джордж Оруэлл", 1949),
                Book("Мастер и Маргарита", "Михаил Булгаков", 1967),
                Book("Программирование на Python", "Васильев А. Н.", 2021),
                Book("Гордость и предубеждение", "Джейн Остен", 1813),
                Book("Великий Гэтсби", "Фрэнсис Скотт Фицджеральд", 1925),
                Book("Ромео и Джульетта", "Уильям Шекспир", 1597),
                Book("А зори здесь тихие", "Борис Васильев", 1969),
                Book("Волшебник Изумрудного города", "Александр Волков", 1939),
                Book("Анна Каренина", "Лев Толстой", 1878)
            ]

    def show_books(self, books=None):
        """Отображение всех книг или переданного списка книг"""
        books_to_show = books if books is not None else self.library
        if not books_to_show:
            print("Нет книг для отображения.")
            return
        for i, book in enumerate(books_to_show, start=1):
            print(f"{i}. {book}")

    def search_books(self, query: str, by: str):
        """Поиск книг по названию или автору"""
        return [b for b in self.library if query.lower() in getattr(b, by).lower()]

    def add_book(self, title, author, year):
        """Добавление новой книги в библиотеку с обработкой ошибок"""
        # Проверка, что имя автора состоит только из букв
        if not author.replace(" ", "").isalpha():  # Учитываем пробелы для составных имен
            print("Ошибка: Имя автора должно содержать только буквы.")
            return

        # Проверка, что название книги не пустое
        if not title or not title.strip():
            print("Ошибка: Название книги не должно быть пустым.")
            return

        # Проверка, что год издания является числом и больше нуля
        if not str(year).isdigit() or int(year) <= 0:
            print("Ошибка: Год издания должен быть положительным числом.")
            return

        if any(book.title == title for book in self.library):
            print(f"Книга '{title}' уже существует в библиотеке.")
            return

        # Если все проверки пройдены, добавляем книгу
        new_book = Book(title, author, year)
        self.library.append(new_book)
        self.save_library()  # Сохранение библиотеки после добавления
        print(f"Книга '{title}' успешно добавлена.")

    def remove_book(self, title):
        """Удаление книги из библиотеки с обработкой ошибок"""
        try:
            self.library = [book for book in self.library if book.title != title]
            self.save_library()  # Сохранение библиотеки после удаления
            print(f"Книга '{title}' успешно удалена.")
        except Exception as e:
            print(f"Произошла ошибка при удалении книги: {e}")

    def save_library(self, filename='library.json'):
        """Сохранение библиотеки в файл"""
        data = [{'title': b.title, 'author': b.author, 'year': b.year} for b in self.library]
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)  # Сохраняем библиотеку в формате JSON

    def load_library(self, filename='library.json'):
        """Загрузка библиотеки из JSON файла"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return [Book(item['title'], item['author'], item['year']) for item in data]
        except FileNotFoundError:
            return []  # Если файл не найден, возвращаем пустой список


# Пользовательский интерфейс
def main():
    manager = LibraryManager()

    while True:
        print("\nДобро пожаловать в систему управления библиотекой!")
        print("1. Показать все книги")
        print("2. Сортировать книги по названию")
        print("3. Сортировать книги по автору")
        print("4. Сортировать книги по году издания")
        print("5. Найти книгу по названию")
        print("6. Найти книгу по автору")
        print("7. Добавить книгу")
        print("8. Удалить книгу")
        print("9. Выйти")

        choice = input("\nВыберите действие: ")

        if choice == '1':
            manager.show_books()
            input("Нажмите Enter, для выхода в меню")

        elif choice == '2':
            sorted_books = quick_sort(manager.library.copy(), 'title')
            manager.show_books(sorted_books)
            input("Нажмите Enter, для выхода в меню")

        elif choice == '3':
            sorted_books = merge_sort(manager.library.copy(), 'author')
            manager.show_books(sorted_books)
            input("Нажмите Enter, для выхода в меню")

        elif choice == '4':
            sorted_books = heap_sort(manager.library.copy(), 'year')
            manager.show_books(sorted_books)
            input("Нажмите Enter, для выхода в меню")

        elif choice == '5':
            query = input("Введите название для поиска: ")
            results = manager.search_books(query=query, by='title')
            manager.show_books(results)
            input("Нажмите Enter, для выхода в меню")

        elif choice == '6':
            query = input("Введите автора для поиска: ")
            results = manager.search_books(query=query, by='author')
            manager.show_books(results)
            input("Нажмите Enter, для выхода в меню")

        elif choice == '7':
            title = input("Название книги: ")
            author = input("Автор книги: ")
            try:
                year = int(input("Год издания: "))
                manager.add_book(title=title, author=author, year=year)
            except ValueError:
                print("Ошибка: Год должен быть числом!")
            input("Нажмите Enter, для выхода в меню")

        elif choice == '8':
            try:
                index = int(input("Введите номер книги для удаления: "))
                # Получаем книгу по индексу
                if 1 <= index <= len(manager.library):
                    book_to_remove = manager.library[index - 1]
                    manager.remove_book(book_to_remove.title)
                    print("Книга успешно удалена!")
                else:
                    print("Неверный номер книги!")
            except ValueError:
                print("Ошибка: Введите корректный номер!")
            input("Нажмите Enter, для выхода в меню")

        elif choice == '9':
            print("До свидания!")
            break
        else:
            print("Неверный выбор! Попробуйте снова.")


if __name__ == "__main__":
    main()
