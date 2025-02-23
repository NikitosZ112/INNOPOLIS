import asyncio
import aiohttp
import re
import aiofiles

# Константы
URLS = [
    "https://q-parser.ru/catalog/platffin",
    "https://www.python.org/"
]
MAX_RETRIES = 3

# fetch: Загружает страницу асинхронно. Обрабатывает ошибки и реализует повторные попытки в случае сбоя.
async def fetch(url, session):
    for attempt in range(MAX_RETRIES):
        try:
            async with session.get(url) as response:
                response.raise_for_status()  # Проверка на ошибки HTTP
                return await response.text()
        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            print(f"Ошибка при загрузке {url}: {e}, попытка {attempt + 1}")
            await asyncio.sleep(1)  # Ожидание перед повторной попыткой
    return None

# parse_html: Извлекает заголовки и ссылки из HTML-кода с помощью регулярных выражений.
async def parse_html(html):
    # Пример извлечения заголовков и ссылок с использованием регулярных выражений
    titles = re.findall(r'<h1.*?>(.*?)</h1>', html, re.DOTALL)
    links = re.findall(r'href="(http[^\"]+)"', html)

    return titles, links

# save_data: Сохраняет извлеченные данные в файл асинхронно.
async def save_data(data, filename):
    async with aiofiles.open(filename, mode='w', encoding='utf-8') as f:
        await f.write(data)

# scrape: Основная функция для загрузки страницы, парсинга HTML и сохранения данных.
async def scrape(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(url, session)
        if html:
            titles, links = await parse_html(html)
            data_to_save = f"Titles:\n{titles}\nLinks:\n{links}\n"
            await save_data(data_to_save, f"{url.split('/')[-1]}.txt")

# main: Запускает асинхронные задачи для всех URL-адресов.
async def main():
    tasks = [scrape(url) for url in URLS]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
