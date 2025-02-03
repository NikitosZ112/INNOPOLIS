
class Employee: # Информация о работниках
    def __init__(self, surname: str, age: int, salary: int) -> None:
        self.surname = surname
        self.age = age
        self.salary = salary

    def __repr__(self) -> str:
        return f"Данные сотрудника: Фамилия: {self.surname}, Возраст: {self.age}, Зарплата: {self.salary}"

def shell_sort(list_employees, key): # Сортировка Шелла
    n = len(list_employees)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = list_employees[i]
            j = i

            while j >= gap and getattr(list_employees[j - gap], key) > getattr(temp, key):
                list_employees[j] = list_employees[j - gap]
                j -= gap

            list_employees[j] = temp

        gap //= 2

    return list_employees

class EmployeeAccounting: # Система сортировки работников
    def __init__(self):
        self.employees = [] # Список работников

    def add_employee(self, surname: str, age: int, salary: int): # Метод для добавления нового работника
        employee = Employee(surname, age, salary)
        self.employees.append(employee)

    def sort_employees(self, key): # Метод для сортировки работников по критериям
        shell_sort(self.employees, key)

    def display_employees(self): # Метод для отображения списка работников
        for employee in self.employees:
            print(f"Фамилия: {employee.surname}, Возраст: {employee.age}, Зарплата: {employee.salary}")


if __name__ == "__main__":
    manager = EmployeeAccounting()

    # Добавление работников
    manager.add_employee("Петров", 50, 100000)
    manager.add_employee("Иванов", 30, 120000)
    manager.add_employee("Алексеев", 19, 25000)

    print("Работники до сортировки:")
    manager.display_employees()

    # Сортировка по фамилии
    manager.sort_employees('surname')

    print("\nРаботники после сортировки по фамилии:")
    manager.display_employees()

    # Сортировка по возрасту
    manager.sort_employees('age')

    print("\nРаботники после сортировки по возрасту:")
    manager.display_employees()

    # Сортировка по зарплате
    manager.sort_employees('salary')

    print("\nРаботники после сортировки по зарплате:")
    manager.display_employees()