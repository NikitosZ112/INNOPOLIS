import asyncio
import models


async def main():
    manager = models.TaskManager()

    try:
        print("Инициализация базы данных...")
        await manager.initialize()
        print("Подключение к БД успешно установлено")
    except Exception as e:
        print(f"Не удалось подключиться к БД: {e}")
        return

    while True:
        print("\nМенеджер задач (PostgreSQL)")
        print("1. Добавить задачу")
        print("2. Удалить задачу")
        print("3. Запустить все задачи")
        print("4. Показать список задач")
        print("5. Найти задачу по ID")
        print("6. Выйти")

        choice = input("Выберите действие: ")

        try:
            if choice == "1":
                description = input("Введите описание задачи: ")
                await manager.add_task(description)
            elif choice == "2":
                task_id = input("Введите ID задачи: ")
                await manager.remove_task(task_id)
            elif choice == "3":
                await manager.run_tasks()
            elif choice == "4":
                manager.list_tasks()
            elif choice == "5":
                task_id = input("Введите ID задачи: ")
                manager.find_task(task_id)
            elif choice == "6":
                print("Выход из программы")
                break
            else:
                print("Неверный выбор, попробуйте снова")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    asyncio.run(main())