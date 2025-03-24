def summa(a, b):
    return a + b

def sub(a, b):
    return a - b

def mult(a, b):
    return a * b

def div(a, b):
    if b == 0:
        raise ZeroDivisionError("Ошибка: деление на ноль!")
    return a / b

def main():
    try:
        num1 = float(input("Введите первое число: "))
        operator = input("Введите оператор (+, -, *, /): ")
        num2 = float(input("Введите второе число: "))

        if operator == "+":
            result = summa(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif operator == "-":
            result = sub(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif operator == "*":
            result = mult(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif operator == "/":
            result = div(num1, num2)
            print(f"{num1} / {num2} = {result}")
        else:
            print("Ошибка: неверный оператор!")
    except ZeroDivisionError as e:
        print(e)

if __name__ == "__main__":
    main()
