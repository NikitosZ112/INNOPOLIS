import pandas as pd

# 1. Загрузка датасета
day_df = pd.read_csv('day.csv')

# 2. Изучение данных
print("Первые 5 строк датасета:")
print(day_df.head(5))
print("\nНазвания столбцов:")
print(day_df.columns.tolist())
print("\nПропущенные значения:")
print(day_df.isnull().sum())

# 3. Итерирование по строкам и подсчет аренды в выходные/будни
weekend_total = 0
weekday_total = 0

for index, row in day_df.iterrows():
    if row['weekday'] == 0 or row['weekday'] == 6:  # 0 - воскресенье, 6 - суббота
        weekend_total += row['cnt']
    else:
        weekday_total += row['cnt']

print(f"\nОбщее количество аренд в выходные: {weekend_total}")
print(f"Общее количество аренд в будни: {weekday_total}")

# 4. Преобразование категориальных переменных
season_dummies = pd.get_dummies(day_df['season'], prefix='season')
day_df = pd.concat([day_df, season_dummies], axis=1)
print("\nПосле преобразования категориальных переменных:")
print(day_df.head(2))

# 5. Группировка по месяцам и среднее количество аренд
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
monthly_avg = day_df.groupby(day_df['dteday'].dt.month)['cnt'].mean()
print("\nСреднее количество аренд по месяцам:")
print(monthly_avg)

# 6. Обработка пропущенных значений
if day_df.isnull().sum().sum() > 0:
    day_df_filled = day_df.fillna(day_df.mean(numeric_only=True)) 
    day_df_dropped = day_df.dropna()
    
    print("\nПосле обработки пропущенных значений:")
    print("Заполнено средними:")
    print(day_df_filled.isnull().sum())
    print("\nУдалены строки с пропусками:")
    print(day_df_dropped.isnull().sum())
else:
    print("\nПропущенных значений не обнаружено")