import math

def summa(a, b):
    """Функция для сложения двух чисел."""
    return a + b

def sub(a, b):
    """Функция для вычитания двух чисел."""
    return a - b

def mult(a, b):
    """Функция для умножения двух чисел."""
    return a * b

def div(a, b):
    """Функция для деления двух чисел."""
    if b == 0:
        raise ZeroDivisionError("Ошибка: деление на ноль!")
    return a / b

def sqrt(a):
    """Функция для вычисления квадратного корня."""
    if a < 0:
        raise ValueError("Ошибка: квадратный корень из отрицательного числа!")
    return math.sqrt(a)

def power(a, b):
    """Функция для вычисления степени."""
    return a ** b

def main():
    try:
        print("Доступные операции:")
        print("+ : Сложение")
        print("- : Вычитание")
        print("* : Умножение")
        print("/ : Деление")
        print("sqrt : Квадратный корень")
        print("power : Возведение в степень")

        operator = input("Введите оператор: ")

        if operator == "+":
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            result = summa(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif operator == "-":
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            result = sub(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif operator == "*":
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            result = mult(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif operator == "/":
            num1 = float(input("Введите первое число: "))
            num2 = float(input("Введите второе число: "))
            result = div(num1, num2)
            print(f"{num1} / {num2} = {result}")
        elif operator == "sqrt":
            num = float(input("Введите число для вычисления квадратного корня: "))
            result = sqrt(num)
            print(f"Квадратный корень из {num} = {result}")
        elif operator == "power":
            num1 = float(input("Введите основание: "))
            num2 = float(input("Введите показатель степени: "))
            result = power(num1, num2)
            print(f"{num1} в степени {num2} = {result}")
        else:
            print("Ошибка: неверный оператор!")
    except ZeroDivisionError as e:
        print(e)
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
