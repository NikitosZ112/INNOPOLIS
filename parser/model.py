import requests
from bs4 import BeautifulSoup
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class WikipediaH3Parser:
    def __init__(self, url):
        self.url = url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

    def fetch_page(self):
        """Загрузка HTML-страницы"""
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка при загрузке страницы: {e}")
            return None

    def parse_h3_headings(self, html):
        """Парсинг заголовков h3 из HTML"""
        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        headings = []

        # Находим все заголовки h3
        for h3 in soup.find_all('h3'):
            # Извлекаем текст, очищаем от лишних пробелов
            heading_text = h3.get_text().strip()
            if heading_text:
                headings.append(heading_text)

        return headings

    def save_to_file(self, headings, filename='h3_headings.txt'):
        """Сохранение заголовков в файл"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                for i, heading in enumerate(headings, 1):
                    f.write(f"{i}. {heading}\n")
            logger.info(f"Сохранено {len(headings)} заголовков в файл {filename}")
            return True
        except IOError as e:
            logger.error(f"Ошибка при сохранении файла: {e}")
            return False

    def run(self):
        """Основной метод выполнения парсинга"""
        logger.info(f"Начало парсинга страницы: {self.url}")

        html = self.fetch_page()
        if not html:
            return False

        headings = self.parse_h3_headings(html)
        if not headings:
            logger.warning("Не найдено ни одного заголовка h3")
            return False

        return self.save_to_file(headings)
