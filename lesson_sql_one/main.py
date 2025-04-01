import psycopg2
from typing import List, Tuple, Optional
from psycopg2 import OperationalError, Error as PGError


class StudentDatabase:
    """
    Класс для работы с базой данных студентов PostgreSQL.
    С комплексной обработкой ошибок для всех операций.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """
        Инициализация подключения к PostgreSQL с обработкой ошибок.
        """
        self.connection_params = {
            "dbname": dbname,
            "user": user,
            "password": password,
            "host": host,
            "port": port,
        }
        self.conn = None
        try:
            self.conn = psycopg2.connect(**self.connection_params)
            self._initialize_database()
            print("Успешное подключение к базе данных!")
        except OperationalError as e:
            print(f"Ошибка подключения к базе данных: {e}")
            raise
        except Exception as e:
            print(f"Неожиданная ошибка при инициализации: {e}")
            raise

    def _initialize_database(self) -> None:
        """Создает таблицу студентов с обработкой ошибок."""
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS students (
                        id SERIAL PRIMARY KEY,
                        first_name VARCHAR(50) NOT NULL,
                        last_name VARCHAR(50) NOT NULL,
                        course INTEGER NOT NULL,
                        age INTEGER NOT NULL,
                        CONSTRAINT valid_course CHECK (course > 0),
                        CONSTRAINT valid_age CHECK (age BETWEEN 15 AND 100)
                    )
                """)
                self.conn.commit()
        except PGError as e:
            print(f"Ошибка при создании таблицы: {e}")
            self.conn.rollback()
            raise

    def add_student(self, first_name: str, last_name: str, course: int, age: int) -> bool:
        """
        Добавляет нового студента с обработкой ошибок.
        Возвращает True при успехе, False при ошибке.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO students (first_name, last_name, course, age)
                    VALUES (%s, %s, %s, %s)
                """, (first_name, last_name, course, age))
                self.conn.commit()
                return True
        except PGError as e:
            print(f"Ошибка при добавлении студента: {e}")
            self.conn.rollback()
            return False

    def get_all_students(self) -> List[Tuple]:
        """
        Возвращает список всех студентов с обработкой ошибок.
        При ошибке возвращает пустой список.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT id, first_name, last_name, course, age FROM students")
                return cursor.fetchall()
        except PGError as e:
            print(f"Ошибка при получении списка студентов: {e}")
            return []

    def get_student_by_id(self, student_id: int) -> Optional[Tuple]:
        """
        Находит студента по ID с обработкой ошибок.
        Возвращает None при ошибке или если студент не найден.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    SELECT id, first_name, last_name, course, age 
                    FROM students 
                    WHERE id = %s
                """, (student_id,))
                return cursor.fetchone()
        except PGError as e:
            print(f"Ошибка при поиске студента: {e}")
            return None

    def update_student(self, student_id: int, first_name: str, last_name: str,
                       course: int, age: int) -> bool:
        """
        Обновляет информацию о студенте с обработкой ошибок.
        Возвращает True при успехе, False при ошибке.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE students 
                    SET first_name = %s, last_name = %s, course = %s, age = %s
                    WHERE id = %s
                """, (first_name, last_name, course, age, student_id))
                self.conn.commit()
                return cursor.rowcount > 0
        except PGError as e:
            print(f"Ошибка при обновлении студента: {e}")
            self.conn.rollback()
            return False

    def delete_student(self, student_id: int) -> bool:
        """
        Удаляет студента с обработкой ошибок.
        Возвращает True при успехе, False при ошибке.
        """
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
                self.conn.commit()
                return cursor.rowcount > 0
        except PGError as e:
            print(f"Ошибка при удалении студента: {e}")
            self.conn.rollback()
            return False

    def __del__(self):
        """Закрывает соединение при уничтожении объекта."""
        if self.conn and not self.conn.closed:
            try:
                self.conn.close()
            except PGError as e:
                print(f"Ошибка при закрытии соединения: {e}")


def display_menu() -> None:
    """Выводит меню доступных действий."""
    print("\nМеню:")
    print("1. Показать всех студентов")
    print("2. Добавить студента")
    print("3. Найти студента по ID")
    print("4. Обновить информацию о студенте")
    print("5. Удалить студента")
    print("6. Выйти")


def display_students(students: List[Tuple]) -> None:
    """Выводит список студентов с обработкой ошибок."""
    try:
        if not students:
            print("Нет студентов в базе данных.")
            return

        print("\nСписок студентов:")
        print("{:<5} {:<15} {:<15} {:<10} {:<10}".format(
            "ID", "Имя", "Фамилия", "Курс", "Возраст"))
        print("-" * 55)
        for student in students:
            print("{:<5} {:<15} {:<15} {:<10} {:<10}".format(
                student[0], student[1], student[2], student[3], student[4]))
    except Exception as e:
        print(f"Ошибка при отображении студентов: {e}")


def get_student_info() -> Tuple[str, str, int, int]:
    """
    Запрашивает информацию о студенте с обработкой ошибок ввода.
    Повторяет запрос при некорректных данных.
    """
    while True:
        try:
            first_name = input("Введите имя: ").strip()
            if not first_name:
                raise ValueError("Имя не может быть пустым")

            last_name = input("Введите фамилию: ").strip()
            if not last_name:
                raise ValueError("Фамилия не может быть пустой")

            course = int(input("Введите номер курса: "))
            if course < 1:
                raise ValueError("Курс должен быть положительным числом")

            age = int(input("Введите возраст: "))
            if not (15 <= age <= 100):
                raise ValueError("Возраст должен быть от 15 до 100 лет")

            return first_name, last_name, course, age

        except ValueError as e:
            print(f"Ошибка ввода: {e}. Пожалуйста, попробуйте снова.")
        except Exception as e:
            print(f"Неожиданная ошибка: {e}. Пожалуйста, попробуйте снова.")


def main() -> None:
    """Основная функция с комплексной обработкой всех возможных ошибок."""
    db = None
    try:
        print("Подключение к PostgreSQL базе данных")
        dbname = input("Имя базы данных: ").strip()
        user = input("Имя пользователя: ").strip()
        password = input("Пароль: ").strip()

        try:
            db = StudentDatabase(dbname, user, password)
        except Exception:
            print("Не удалось подключиться к базе данных. Завершение работы.")
            return

        while True:
            try:
                display_menu()
                choice = input("Выберите действие (1-6): ").strip()

                if choice == "1":
                    try:
                        students = db.get_all_students()
                        display_students(students)
                    except Exception as e:
                        print(f"Ошибка при отображении студентов: {e}")

                elif choice == "2":
                    print("\nДобавление нового студента:")
                    try:
                        student_data = get_student_info()
                        if db.add_student(*student_data):
                            print("Студент успешно добавлен!")
                        else:
                            print("Не удалось добавить студента.")
                    except Exception as e:
                        print(f"Ошибка при добавлении студента: {e}")

                elif choice == "3":
                    try:
                        student_id = int(input("Введите ID студента: "))
                        student = db.get_student_by_id(student_id)
                        if student:
                            display_students([student])
                        else:
                            print("Студент с таким ID не найден.")
                    except ValueError:
                        print("Ошибка: ID должен быть целым числом.")
                    except Exception as e:
                        print(f"Ошибка при поиске студента: {e}")

                elif choice == "4":
                    try:
                        student_id = int(input("Введите ID студента для обновления: "))
                        student = db.get_student_by_id(student_id)
                        if not student:
                            print("Студент с таким ID не найден.")
                            continue

                        print("\nТекущая информация о студенте:")
                        display_students([student])

                        print("\nВведите новые данные:")
                        new_data = get_student_info()

                        if db.update_student(student_id, *new_data):
                            print("Информация о студенте успешно обновлена!")
                        else:
                            print("Не удалось обновить информацию о студенте.")
                    except ValueError:
                        print("Ошибка: ID должен быть целым числом.")
                    except Exception as e:
                        print(f"Ошибка при обновлении студента: {e}")

                elif choice == "5":
                    try:
                        student_id = int(input("Введите ID студента для удаления: "))
                        if db.delete_student(student_id):
                            print("Студент успешно удален!")
                        else:
                            print("Студент с таким ID не найден.")
                    except ValueError:
                        print("Ошибка: ID должен быть целым числом.")
                    except Exception as e:
                        print(f"Ошибка при удалении студента: {e}")

                elif choice == "6":
                    print("Выход из программы...")
                    break

                else:
                    print("Неверный выбор. Пожалуйста, введите число от 1 до 6.")

            except KeyboardInterrupt:
                print("\nПрервано пользователем. Возврат в меню...")
            except Exception as e:
                print(f"Неожиданная ошибка: {e}. Продолжение работы...")

    finally:
        if db:
            try:
                del db  # Вызовет __del__ и закроет соединение
            except Exception as e:
                print(f"Ошибка при закрытии соединения с БД: {e}")
        print("Программа завершена.")


if __name__ == "__main__":
    main()