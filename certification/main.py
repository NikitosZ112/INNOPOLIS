import time
import queue

class Delivery:
    def __init__(self, delivery_number, departure_point, destination_point, weight, delivery_time, priority):
        self.delivery_number = delivery_number
        self.departure_point = departure_point
        self.destination_point = destination_point
        self.weight = weight
        self.delivery_time = delivery_time
        self.priority = priority
        self.status = "В ожидании"

    def __repr__(self):
        return f"Доставка: {self.delivery_number}, От: {self.departure_point}, До: {self.destination_point}, Вес: {self.weight}, Время: {self.delivery_time}, Приоритет: {self.priority}, Статус: {self.status}"
    # Распределеяем поставки по приоритету
    def __lt__(self, other):
        return self.priority < other.priority


class DeliveryManager:
    def __init__(self):
        self.deliveries = []
        self.initialize_deliveries()

    def initialize_deliveries(self):
        deliveries = [
            (1, "Москва", "Тольятти", 50, "10:00", 1),
            (2, "Санкт-Петербург", "Казань", 30, "12:00", 1),
            (3, "Екатеринбург", "Нижний Новгород", 20, "14:00",3),
            (4, "Новосибирск", "Челябинск", 25, "09:00", 2),
            (5, "Казань", "Ростов-на-Дону", 15, "11:30", 4),
        ]

        for delivery in deliveries:
            self.add_delivery(*delivery)
    # Функция добавления поставки
    def add_delivery(self, delivery_number, departure_point, destination_point, weight, delivery_time, priority=1):
        if isinstance(delivery_number, int) and isinstance(weight, (int, float)) and isinstance(delivery_time, str) \
                and isinstance(departure_point, str) and isinstance(destination_point, str) and isinstance(priority,int):
            new_delivery = Delivery(delivery_number, departure_point, destination_point, weight, delivery_time, priority)
            self.deliveries.append(new_delivery)
            print(f"Поставка с номером {delivery_number} добавлена.")
        else:
            print("Ошибка: Проверьте введенные данные. Номер доставки должен быть целым числом, вес - числом, время - строкой, пункты - строками, приоритет - целым числом.")

    # Функция удаления поставки
    def remove_delivery(self, delivery_number):
        try:
            delivery_number = int(delivery_number)
        except ValueError:
            print("Ошибка: Номер доставки должен быть целым числом.")
            return
        delivery_to_remove = None
        for delivery in self.deliveries:
            if delivery.delivery_number == delivery_number:
                delivery_to_remove = delivery
                break
        if delivery_to_remove:
            self.deliveries.remove(delivery_to_remove)
            print(f"Поставка с номером {delivery_number} удалена.")
        else:
            print("Поставка не найдена.")

    # Функция изменения поставки
    def update_delivery(self, delivery_number, new_departure_point=None, new_destination_point=None, new_weight=None, new_delivery_time=None, new_priority=None):
        try:
            delivery_number = int(delivery_number)
        except ValueError:
            print("Ошибка: Номер доставки должен быть целым числом.")
            return

        for delivery in self.deliveries:
            if delivery.delivery_number == delivery_number:
                if new_departure_point is not None:
                    if not isinstance(new_departure_point, str):
                        print("Ошибка: Пункт отправления должен быть строкой.")
                        return
                    delivery.departure_point = new_departure_point

                if new_destination_point is not None:
                    if not isinstance(new_destination_point, str):
                        print("Ошибка: Пункт назначения должен быть строкой.")
                        return
                    delivery.destination_point = new_destination_point

                if new_weight is not None:
                    try:
                        new_weight = float(new_weight)
                    except ValueError:
                        print("Ошибка: Вес должен быть числом.")
                        return
                    delivery.weight = new_weight

                if new_delivery_time is not None:
                     if not isinstance(new_delivery_time, str):
                        print("Ошибка: Время должно быть строкой.")
                        return
                     delivery.delivery_time = new_delivery_time

                if new_priority is not None:
                    try:
                        new_priority = int(new_priority)
                        delivery.priority = new_priority
                    except ValueError:
                        print("Ошибка: Приоритет должен быть целым числом.")
                        return

                print(f"Поставка с номером {delivery_number} обновлена.")
                return

        print("Поставка не найдена.")

    # Сортировка слиянием
    def merge_sort(self, deliveries):
        if len(deliveries) <= 1:
            return deliveries
        middle = len(deliveries) // 2
        left = deliveries[:middle]
        right = deliveries[middle:]

        left = self.merge_sort(left)
        right = self.merge_sort(right)

        return self.merge(left, right)

    def merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i].weight < right[j].weight:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result += left[i:]
        result += right[j:]
        return result

    # Быстрая сортировка
    def quick_sort(self, deliveries):
        if len(deliveries) <= 1:
            return deliveries
        pivot = deliveries[len(deliveries) // 2].delivery_time
        left = [x for x in deliveries if x.delivery_time < pivot]
        middle = [x for x in deliveries if x.delivery_time == pivot]
        right = [x for x in deliveries if x.delivery_time > pivot]
        return self.quick_sort(left) + middle + self.quick_sort(right)

    # Пирамидальная сортировка
    def heap_sort(self, deliveries):
        def heapify(deliveries, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n and deliveries[left].delivery_number > deliveries[largest].delivery_number:
                largest = left

            if right < n and deliveries[right].delivery_number > deliveries[largest].delivery_number:
                largest = right

            if largest != i:
                deliveries[i], deliveries[largest] = deliveries[largest], deliveries[i]
                heapify(deliveries, n, largest)

        n = len(deliveries)
        for i in range(n // 2 - 1, -1, -1):
            heapify(deliveries, n, i)
        for i in range(n - 1, 0, -1):
            deliveries[i], deliveries[0] = deliveries[0], deliveries[i]
            heapify(deliveries, i, 0)
        return deliveries

    # Функция линейного поиска поставки
    def linear_search(self, delivery_number):
        try:
            delivery_number = int(delivery_number)
        except ValueError:
            print("Ошибка: Номер доставки должен быть целым числом.")
            return None

        for delivery in self.deliveries:
            if delivery.delivery_number == delivery_number:
                return delivery
        return None

    # Функция бинароного поиска поставки
    def binary_search(self, sorted_deliveries, delivery_time):
        low = 0
        high = len(sorted_deliveries) - 1
        while low <= high:
            mid = (low + high) // 2
            if sorted_deliveries[mid].delivery_time == delivery_time:
                return sorted_deliveries[mid]
            elif sorted_deliveries[mid].delivery_time < delivery_time:
                low = mid + 1
            else:
                high = mid - 1
        return None

    # Функция извлечения и возврата списка доставок в порядке их приоритета
    def get_prioritized_deliveries(self):
        priority_queue = queue.PriorityQueue()
        for delivery in self.deliveries:
            priority_queue.put(delivery)  # Добавляем в приоритетную очередь
        prioritized_deliveries = []
        while not priority_queue.empty():
            prioritized_deliveries.append(priority_queue.get())  # Извлекаем в порядке приоритета
        return prioritized_deliveries

    # Функция для выполнения доставок в порядке их приоритета
    def execute_tasks(self):
        task_queue = queue.PriorityQueue()
        for delivery in self.deliveries:
            task_queue.put(delivery)
        while not task_queue.empty():
            current_task = task_queue.get()
            current_task.status = "В работе"
            print(f"Выполнение задачи: {current_task.delivery_number} (Приоритет: {current_task.priority} )")
            time.sleep(1)  # Симуляция выполнения задачи
            current_task.status = "Выполнено"
            print(f"Поставка {current_task.delivery_number} выполнена.")


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]
        return None


class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        return None

    def is_empty(self):
        return len(self.queue) == 0

    def peek(self):
        if not self.is_empty():
            return self.queue[0]
        return None

def main_menu():
    manager = DeliveryManager()
    stack = Stack()
    queue = Queue()

    while True:
        print("\nПрограмма управления логистическими поставками")
        print("\nМеню:")
        print("1. Отобразить все поставки")
        print("2. Удалить поставку")
        print("3. Изменить поставку")
        print("4. Добавить поставку")
        print("5. Сортировать по весу груза")
        print("6. Сортировать по времени доставки")
        print("7. Сортировать по номеру доставки")
        print("8. Получение запросов через стек")
        print("9. Отобразить поставки по приоритету")
        print("10. Вывод результата линейного поиска")
        print("11. Вывод результата бинарного поиска")
        print("12. Выполнить поставки")
        print("13. Выйти")

        choice = input("\nВыберите опцию: ")


        if choice == '1':
            print("\nСписок всех доставок:")
            for delivery in manager.deliveries:
                print(delivery)
            print()
            input("Нажмите Enter, для выхода в меню")


        elif choice == '2':
            if not manager.deliveries:
                print("Доставок нет.")
            else:
                print("Список доставок:")
                for delivery in manager.deliveries:
                    print(delivery)
                delivery_number = input("Введите номер доставки для удаления: ")
                manager.remove_delivery(delivery_number)
            input("Нажмите Enter, для выхода в меню")


        elif choice == '3':
            if not manager.deliveries:
                print("Доставок нет.")
            else:
                print("Список доставок:")
                for delivery in manager.deliveries:
                    print(delivery)
            delivery_number = input("Введите номер доставки для изменения: ")
            new_departure_point = input("Введите новый пункт отправления (или Enter, чтобы оставить прежний): ") or None
            new_destination_point = input("Введите новый пункт назначения (или Enter, чтобы оставить прежний): ") or None
            new_weight_str = input("Введите новый вес груза (или Enter, чтобы оставить прежний): ")
            new_weight = float(new_weight_str) if new_weight_str else None
            new_delivery_time = input("Введите новое время доставки (или Enter, чтобы оставить прежний): ") or None
            new_priority_str = input("Введите новый приоритет (или Enter, чтобы оставить прежний): ")
            new_priority = int(new_priority_str) if new_priority_str else None
            manager.update_delivery(delivery_number, new_departure_point, new_destination_point, new_weight, new_delivery_time, new_priority)
            print("Поставка обновлена.")
            input("Нажмите Enter, для выхода в меню")


        elif choice == '4':
            try:
                delivery_number = int(input("Введите номер доставки (целое число): "))
                departure_point = input("Введите пункт отправления: ")
                destination_point = input("Введите пункт назначения: ")
                weight = float(input("Введите вес груза: "))
                delivery_time = input("Введите время доставки (чч:мм): ")
                priority = int(input("Введите приоритет (целое число, чем меньше - тем выше приоритет): "))
                hours, minutes = map(int, delivery_time.split(':'))
                if hours < 0 or hours >= 24 or minutes < 0 or minutes >= 60:
                    raise ValueError("Некорректный формат времени.")

                manager.add_delivery(delivery_number, departure_point, destination_point, weight, delivery_time)
            except ValueError as e:
                print(f"Ошибка: {e}. Проверьте введенные данные.")
            input("Нажмите Enter, для выхода в меню")


        elif choice == '5':
            if not manager.deliveries:
                print("Доставок нет")
            else:
                sorted_deliveries = manager.merge_sort(manager.deliveries)
                print("Поставки отсортированы по весу груза.")
                for delivery in sorted_deliveries:
                    print(delivery)
            input("Нажмите Enter, для выхода в меню")


        elif choice == '6':
            if not manager.deliveries:
                print("Доставок нет.")
            else:
                sorted_deliveries = manager.quick_sort(manager.deliveries)
                print("Поставки отсортированы по времени доставки.")
                for delivery in sorted_deliveries:
                    print(delivery)
            input("Нажмите Enter, для выхода в меню")


        elif choice == '7':
            if not manager.deliveries:
                print("Доставок нет.")
            else:
                sorted_deliveries = manager.heap_sort(manager.deliveries)
                print("Поставки отсортированы по номеру доставки.")
                for delivery in sorted_deliveries:
                    print(delivery)
            input("Нажмите Enter, для выхода в меню")


        elif choice == '8':
            print("\nОбработка запросов через стек (LIFO):")
            stack = Stack()
            for delivery in manager.deliveries:
                stack.push(delivery)
            while not stack.is_empty():
                delivery = stack.pop()
                print(f"Обработка доставки: {delivery}")
            print()
            input("Нажмите Enter, для выхода в меню")


        elif choice == '9':
            print("\nПриоритетные поставки (чем меньше число, тем выше приоритет):")
            prioritized_deliveries = manager.get_prioritized_deliveries()
            for delivery in prioritized_deliveries:
                print(delivery)
            print()
            input("Нажмите Enter, для выхода в меню")


        elif choice == '10':
            delivery_number = input("Введите номер доставки для линейного поиска: ")
            result = manager.linear_search(delivery_number)
            if result:
                print(f"Результат линейного поиска: {result}")
            else:
                print("Поставка не найдена.")
            input("Нажмите Enter, для выхода в меню")


        elif choice == '11':
            delivery_time = input("Введите время доставки для бинарного поиска: ")
            if not manager.deliveries:
                print("Доставок нет.")
            else:
                sorted_deliveries = sorted(manager.deliveries, key=lambda x: x.delivery_time)
                result = manager.binary_search(sorted_deliveries, delivery_time)
                print(f"Результат бинарного поиска: {result}" if result else "Поставка не найдена.")
            input("Нажмите Enter, для выхода в меню")


        elif choice == '12':
            print("\nВыполнение поставок:")
            manager.execute_tasks()
            print()
            input("Нажмите Enter, для выхода в меню")


        elif choice == '13':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main_menu()

