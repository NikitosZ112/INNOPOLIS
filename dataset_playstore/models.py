import pandas as pd

# Загрузка датасета
df = pd.read_csv('googleplaystore.csv')

# 1. Вывести первые 10 строк датасета
print("1. Первые 10 строк датасета:")
print(df.head(10))
print("\n")

# 2. Вывести случайные 5 строк датасета
print("2. Случайные 5 строк датасета:")
print(df.sample(5))
print("\n")

# 3. Вывести количество строк и столбцов
print("3. Количество строк и столбцов:")
print(f"Строк: {df.shape[0]}, Столбцов: {df.shape[1]}")
print("\n")

# 4. Вывести данные о количестве пропущенных значений
print("4. Количество пропущенных значений:")
print(df.isnull().sum())
print("\n")

# 5. Отбросить из датафрейма строки с пропущенными значениями и снова вывести для проверки
df_cleaned = df.dropna()
print("5. Данные после удаления пропущенных значений:")
print("Количество пропущенных значений после очистки:")
print(df_cleaned.isnull().sum())
print("\n")

# 6. Найти самый большой и самый маленький рейтинги, а также среднее значение рейтинга
print("6. Анализ рейтингов:")
print(f"Максимальный рейтинг: {df_cleaned['Rating'].max()}")
print(f"Минимальный рейтинг: {df_cleaned['Rating'].min()}")
print(f"Средний рейтинг: {df_cleaned['Rating'].mean()}")
print("\n")

# 7. Вывести первые 10 приложений с рейтингом не ниже 4.9
high_rating_apps = df_cleaned[df_cleaned['Rating'] >= 4.9].head(10)
print("7. Первые 10 приложений с рейтингом не ниже 4.9:")
print(high_rating_apps[['App', 'Rating']])
print("\n")

# 8. Вывести 5 самых часто скачиваемых приложений
# Сначала преобразуем столбец Installs в числовой формат
df_cleaned['Installs'] = df_cleaned['Installs'].str.replace('+', '').str.replace(',', '').astype(int)
top_downloaded = df_cleaned.sort_values('Installs', ascending=False).head(5)
print("8. 5 самых часто скачиваемых приложений:")
print(top_downloaded[['App', 'Installs']])