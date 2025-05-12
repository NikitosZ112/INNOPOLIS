import requests
import csv
from statistics import mean
import os
from dotenv import load_dotenv

# Загрузка API ключа из .env файла
load_dotenv()
API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
if not API_KEY:
    raise ValueError(
        "API ключ OpenWeatherMap не найден. Пожалуйста, создайте .env файл с OPENWEATHERMAP_API_KEY=ваш_ключ")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"


def get_weather_data(city_name):
    """
    Получает данные о погоде для указанного города
    """
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',  # для получения температуры в °C
            'lang': 'ru'  # для получения описания на русском
        }

        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP

        data = response.json()

        # Извлекаем нужные данные
        weather_info = {
            'city': city_name,
            'temperature': data['main']['temp'],
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'description': data['weather'][0]['description'],
            'feels_like': data['main']['feels_like']
        }

        return weather_info

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе данных для города {city_name}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Ошибка при обработке данных для города {city_name}: {e}")
        return None


def analyze_weather_data(weather_data_list):
    """
    Анализирует данные о погоде
    """
    # Фильтруем города, для которых удалось получить данные
    valid_data = [data for data in weather_data_list if data is not None]

    if not valid_data:
        print("Нет данных для анализа")
        return

    # Средняя температура
    avg_temp = mean([data['temperature'] for data in valid_data])

    # Город с максимальной температурой
    hottest_city = max(valid_data, key=lambda x: x['temperature'])

    # Город с минимальной температурой
    coldest_city = min(valid_data, key=lambda x: x['temperature'])

    print("\nАнализ данных о погоде:")
    print(f"Средняя температура среди всех городов: {avg_temp:.1f}°C")
    print(f"Самый теплый город: {hottest_city['city']} ({hottest_city['temperature']}°C)")
    print(f"Самый холодный город: {coldest_city['city']} ({coldest_city['temperature']}°C)")


def save_to_csv(weather_data_list, filename='weather_data.csv'):
    """
    Сохраняет данные о погоде в CSV файл
    """
    # Фильтруем города, для которых удалось получить данные
    valid_data = [data for data in weather_data_list if data is not None]

    if not valid_data:
        print("Нет данных для сохранения")
        return

    # Определяем поля для CSV
    fieldnames = ['city', 'temperature', 'feels_like', 'humidity', 'wind_speed', 'description']

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Записываем заголовки
            writer.writeheader()

            # Записываем данные
            for data in valid_data:
                writer.writerow(data)

        print(f"\nДанные успешно сохранены в файл {filename}")
    except IOError as e:
        print(f"Ошибка при сохранении файла: {e}")


def main():
    cities = ["Москва", "Нью-Йорк", "Токио", "Лондон", "Берлин"]
    weather_data_list = []

    print("Получение данных о погоде...")
    for city in cities:
        print(f"Запрашиваю данные для города: {city}")
        weather_data = get_weather_data(city)
        weather_data_list.append(weather_data)

    # Выводим полученные данные
    print("\nПолученные данные:")
    for data in weather_data_list:
        if data:
            print(
                f"{data['city']}: {data['description']}, {data['temperature']}°C (ощущается как {data['feels_like']}°C), "
                f"влажность {data['humidity']}%, ветер {data['wind_speed']} м/с")

    # Анализируем данные
    analyze_weather_data(weather_data_list)

    # Сохраняем в CSV
    save_to_csv(weather_data_list)


if __name__ == "__main__":
    main()