# 1. Создание каррированных функций:

# def hours_per_day(hours):
#     def calculate_minutes(minutes):
#         return hours * minutes
#     return calculate_minutes
#
# result = hours_per_day(8)(20)
# print(result)
#
# def bonus_percentage(percentage):
#     def calculate_bonus(bonus):
#         return bonus // percentage
#     return calculate_bonus
#
#
# result2 = bonus_percentage(10)(3000)
# print(result2)

# 2. Частичное применение:

# from functools import partial
#
# def net_salary(gross_salary, tax_rate):
#     return gross_salary - (gross_salary * tax_rate)
#
# tax_20 = partial(net_salary, tax_rate=0.20)
# result = tax_20(10.5)
# print(result)
#
# def final_salary(base_salary, bonus):
#     return base_salary + bonus
#
# bonus_500 = partial(final_salary, bonus=500)
# result = bonus_500(3000)
# print(result)

# 3. Композиция функций

# def calculate_hours(hours_per_day, days):
#     return hours_per_day * days
#
# def calculate_gross_salary(hours, hourly_rate):
#     return hours * hourly_rate
#
# def composed_salary_function(hours_per_day, days, hourly_rate):
#     total_calculate_hours = calculate_hours(hours_per_day, days)
#     gross_salary = calculate_gross_salary(hourly_rate, total_calculate_hours)
#     return gross_salary
#
# result = composed_salary_function(8, 20, 25)
# print(result)

# def calculate_net_salary(gross_salary):
#     return gross_salary * 0.80
#
# def apply_bonus(salary, bonus):
#     return salary + bonus
#
#
# def final_salary_composition(gross_salary, bonus):
#     net_salary = calculate_net_salary(gross_salary)
#     return apply_bonus(net_salary, bonus)
#
# result = final_salary_composition(4000, 300)
# print(result)
