import pytest
from lesson_three.employee import EmployeeAccounting


def test_add_employee():
    manager = EmployeeAccounting()

    # Проверка добавления работника
    manager.add_employee("Иванов", 30, 50000)
    assert len(manager.employees) == 1

    # Проверка обработки ошибки при некорректных данных
    with pytest.raises(ValueError):
        manager.add_employee("Петров", "двадцать пять", 60000)


def test_sort_employees():
    manager = EmployeeAccounting()

    # Добавление работников для тестирования сортировки
    manager.add_employee("Иванов", 30, 50000)
    manager.add_employee("Петров", 25, 60000)
    manager.add_employee("Сидоров", 35, 55000)

    # Сортировка по фамилии
    manager.sort_employees('last_name')
    assert manager.employees[0].last_name == "Иванов"

    # Сортировка по возрасту
    manager.sort_employees('age')
    assert manager.employees[0].age == 25

    # Проверка обработки ошибки при некорректном ключе сортировки
    with pytest.raises(KeyError):
        manager.sort_employees('неизвестный_ключ')


def test_display_employees(capsys):
    manager = EmployeeAccounting()

    # Проверка вывода при пустом списке работников
    manager.display_employees()

    captured = capsys.readouterr()

    assert "Список работников пуст." in captured.out