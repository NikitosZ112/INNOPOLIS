import asyncio
import time
import psycopg2
import asyncpg
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

DB_CONFIG = {
    "user": "postgres",
    "password": "12345",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "postgres"
}

@dataclass
class Task:
    id: int
    description: str
    created_at: float = field(default_factory=time.time)
    completed: bool = False


class Command(ABC):
    @abstractmethod
    async def execute(self):
        pass


class TaskCommand(Command):
    def __init__(self, task: Task, db_pool):
        self.task = task
        self.db_pool = db_pool

    async def execute(self):
        try:
            print(f"Выполняется задача {self.task.id}: {self.task.description}")
            await asyncio.sleep(3)

            async with self.db_pool.acquire() as conn:
                await conn.execute(
                    "UPDATE tasks SET completed = TRUE WHERE task_id = $1",
                    self.task.id
                )

            self.task.completed = True
            print(f"Задача {self.task.id} выполнена!")
        except Exception as e:
            print(f"Ошибка при выполнении задачи: {e}")


class TaskQueue:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.db_pool = None
            cls._instance.tasks: Dict[int, Task] = {}
            cls._instance.commands: Dict[int, TaskCommand] = {}
        return cls._instance

    async def initialize_db(self):
        try:
            # Синхронное подключение для создания таблицы
            sync_conn = psycopg2.connect(**DB_CONFIG)
            with sync_conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tasks (
                        task_id SERIAL PRIMARY KEY,
                        description TEXT NOT NULL,
                        created_at FLOAT NOT NULL,
                        completed BOOLEAN DEFAULT FALSE
                    )
                """)
                sync_conn.commit()
            sync_conn.close()

            # Асинхронный пул соединений
            self.db_pool = await asyncpg.create_pool(**DB_CONFIG)
            await self._load_tasks_from_db()
        except Exception as e:
            print(f"Ошибка инициализации БД: {e}")
            raise

    async def _load_tasks_from_db(self):
        async with self.db_pool.acquire() as conn:
            records = await conn.fetch("SELECT * FROM tasks ORDER BY task_id")
            for record in records:
                task = Task(
                    id=record['task_id'],
                    description=record['description'],
                    created_at=record['created_at'],
                    completed=record['completed']
                )
                self.tasks[task.id] = task
                self.commands[task.id] = TaskCommand(task, self.db_pool)

    async def add_task(self, description: str) -> Task:
        try:
            async with self.db_pool.acquire() as conn:
                # Вставляем задачу и возвращаем сгенерированный ID
                record = await conn.fetchrow(
                    "INSERT INTO tasks (description, created_at) VALUES ($1, $2) RETURNING task_id",
                    description, time.time()
                )
                task_id = record['task_id']
                task = Task(id=task_id, description=description)

                self.tasks[task.id] = task
                self.commands[task.id] = TaskCommand(task, self.db_pool)
                return task
        except Exception as e:
            print(f"Ошибка при добавлении задачи в БД: {e}")
            raise

    async def remove_task(self, task_id: int) -> bool:
        try:
            async with self.db_pool.acquire() as conn:
                result = await conn.execute(
                    "DELETE FROM tasks WHERE task_id = $1",
                    task_id
                )

            if result == "DELETE 1":
                if task_id in self.tasks:
                    del self.tasks[task_id]
                    del self.commands[task_id]
                return True
            return False
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")
            return False

    def get_all_tasks(self) -> List[Task]:
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> Optional[Task]:
        return self.tasks.get(task_id)


class TaskSorter:
    @staticmethod
    def bubble_sort(tasks: List[Task]) -> List[Task]:
        n = len(tasks)
        for i in range(n):
            for j in range(0, n - i - 1):
                if tasks[j].created_at > tasks[j + 1].created_at:
                    tasks[j], tasks[j + 1] = tasks[j + 1], tasks[j]
        return tasks


class TaskFinder:
    @staticmethod
    def linear_search(tasks: List[Task], task_id: int) -> Optional[Task]:
        for task in tasks:
            if task.id == task_id:
                return task
        return None


class TaskManager:
    def __init__(self):
        self.queue = TaskQueue()
        self.sorter = TaskSorter()
        self.finder = TaskFinder()

    async def initialize(self):
        await self.queue.initialize_db()

    async def add_task(self, description: str):
        try:
            task = await self.queue.add_task(description)
            print(f"Задача добавлена: ID={task.id}")
        except Exception as e:
            print(f"Ошибка при добавлении задачи: {e}")

    async def remove_task(self, task_id: str):
        try:
            task_id_int = int(task_id)
            if await self.queue.remove_task(task_id_int):
                print(f"Задача {task_id_int} удалена")
            else:
                print(f"Задача {task_id_int} не найдена")
        except ValueError:
            print("Ошибка: ID задачи должен быть числом")
        except Exception as e:
            print(f"Ошибка при удалении задачи: {e}")

    async def run_tasks(self):
        try:
            tasks = self.queue.get_all_tasks()
            if not tasks:
                print("Нет задач для выполнения")
                return

            print(f"Запуск {len(tasks)} задач...")
            commands = [self.queue.commands[task.id] for task in tasks]
            await asyncio.gather(*[cmd.execute() for cmd in commands])
            print("Все задачи выполнены!")
        except Exception as e:
            print(f"Ошибка при выполнении задач: {e}")

    def list_tasks(self):
        try:
            tasks = self.queue.get_all_tasks()
            if not tasks:
                print("Список задач пуст")
                return

            sorted_tasks = self.sorter.bubble_sort(tasks)
            print("\nСписок задач (от старых к новым):")
            for task in sorted_tasks:
                status = "✓" if task.completed else "✗"
                print(f"[{status}] {task.id}: {task.description}")
        except Exception as e:
            print(f"Ошибка при выводе списка задач: {e}")

    def find_task(self, task_id: str):
        try:
            task_id_int = int(task_id)
            task = self.finder.linear_search(self.queue.get_all_tasks(), task_id_int)
            if task:
                status = "✓" if task.completed else "✗"
                print(f"Найдена задача [{status}]: {task.description}")
            else:
                print(f"Задача {task_id_int} не найдена")
        except ValueError:
            print("Ошибка: ID задачи должен быть числом")
        except Exception as e:
            print(f"Ошибка при поиске задачи: {e}")


async def main():
    manager = TaskManager()

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