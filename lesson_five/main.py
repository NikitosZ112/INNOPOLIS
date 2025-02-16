import time
import queue

class Task:
    def __init__(self, name, duration, priority=1):
        self.name = name
        self.duration = duration
        self.priority = priority
        self.status = "В ожидании"  # Статус задачи (В ожидании, В работе, Выполнено)

    def __lt__(self, other):
        # Задачи с более высоким приоритетом (меньшее значение) должны выполняться первыми
        return self.priority < other.priority

class TaskScheduler:
    def __init__(self):
        self.task_queue = queue.PriorityQueue()  # Используем приоритетную очередь

    def add_task(self, task):
        self.task_queue.put(task)

    def execute_tasks(self):
        while not self.is_empty():
            current_task = self.task_queue.get()
            current_task.status = "В работе"
            print(f"Выполнение задачи: {current_task.name} (Продолжительность: {current_task.duration} сек)")
            time.sleep(current_task.duration)  # Симуляция выполнения задачи
            current_task.status = "Выполнено"
            print(f"Задача {current_task.name} выполнена.")

    def is_empty(self):
        if self.task_queue.empty() == True:
            print("Очередь пуста")

    def task_count(self):
        return self.task_queue.qsize()

if __name__ == "__main__":
    scheduler = TaskScheduler()

    # Создаем несколько задач с разными приоритетами
    task1 = Task("Задача 1", 2, priority=2)  # Приоритет 2
    task2 = Task("Задача 2", 1, priority=1)  # Приоритет 1
    task3 = Task("Задача 3", 3, priority=3)  # Приоритет 3

    # Добавляем задачи в планировщик
    scheduler.add_task(task1)
    scheduler.add_task(task2)
    scheduler.add_task(task3)

    # Печатаем количество задач в очереди
    print(f"Количество задач в очереди: {scheduler.task_count()}")

    # Выполняем задачи
    scheduler.execute_tasks()

    # Проверяем, пуста ли очередь
    print( scheduler.is_empty())
