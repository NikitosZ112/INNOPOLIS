import sys
import os 
import gspread
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
from dotenv import load_dotenv
from src.utils.google_sheets import GoogleSheetClient
from oauth2client.service_account import ServiceAccountCredentials
from src.utils.logger import get_logger
from src.generators.yandex_gpt import YandexGPTGenerator
from src.formatters.html_formatter import HTMLFormatter
from src.parser.ozon_parser import init_webdriver, get_mainpage_cards, get_searchpage_cards, get_product_info

sys.path.append(str(Path(__file__).parent.parent))
load_dotenv()
logger = get_logger(__name__)
BASE_DIR = Path(__file__).parent 
GOOGLE_CREDS_PATH = BASE_DIR / "config" / "credentials.json"
SPREADSHEET_ID = os.getenv('SPREADSHEET_KEY')

@dataclass
class Product:
    id: str
    name: str
    url: str

class OzonParser:
    def __init__(self):
        self.driver = init_webdriver()
    
    def get_product_data(self, url: str) -> Dict:
        """Получает данные товара с Ozon"""
        try:
            product_id, full_name, description, price, rating, rating_counter, image_url = get_product_info(url)
            
            return {
                'name': full_name,
                'description': description,
                'price': price,
                'rating': rating,
                'rating_count': rating_counter,
                'image_url': image_url,
                'url': url
            }
        except Exception as e:
            logger.error(f"Ошибка парсинга товара: {str(e)}")
            return None
    
    def get_main_page_products(self) -> List[Dict]:
        """Получает товары с главной страницы Ozon"""
        try:
            products = get_mainpage_cards(self.driver, "https://www.ozon.ru")
            return [{
                'id': pid,
                'name': data['full_name'],
                'url': data['url'],
                'price': data['price'],
                'rating': data['rating']
            } for product in products for pid, data in product.items()]
        except Exception as e:
            logger.error(f"Ошибка парсинга главной страницы: {str(e)}")
            return []
    
    def get_search_results(self, query: str) -> List[Dict]:
        """Получает результаты поиска по запросу"""
        try:
            url = f"https://www.ozon.ru/search/?text={query}&from_global=true"
            products = get_searchpage_cards(self.driver, url)
            return [{
                'id': pid,
                'name': data['full_name'],
                'url': data['url'],
                'price': data['price'],
                'rating': data['rating']
            } for product in products for pid, data in product.items()]
        except Exception as e:
            logger.error(f"Ошибка парсинга поиска: {str(e)}")
            return []
    
    def close(self):
        self.driver.quit()

def get_products_to_process() -> List[Product]:
    """Список товаров с Ozon для обработки"""
    parser = OzonParser()
    try:
        # Получаем товары с главной страницы
        main_products = parser.get_main_page_products()[:3]
        
        # Получаем результаты поиска
        search_products = []
        for query in ["белая+рубашка", "RTX+4090"]:
            search_products.extend(parser.get_search_results(query)[:1])
        
        return [
            Product(
                id=f"OZ-{i}",
                name=product['name'],
                url=product['url']
            ) for i, product in enumerate(main_products + search_products, 1)
        ]
    finally:
        parser.close()

def prepare_gpt_prompt(product_data: Dict) -> str:
    """Формирует текст для GPT на основе данных Ozon"""
    prompt_parts = [
        f"Название товара: {product_data['name']}",
        f"\nЦена: {product_data.get('price', 'не указана')}",
        f"\nРейтинг: {product_data.get('rating', 'не указан')}",
        "\nОписание товара:\n" + product_data['description'] if product_data.get('description') else "",
    ]
    return "\n".join(filter(None, prompt_parts))

def process_products(products: List[Product]) -> List[Dict]:
    """Полный цикл обработки товаров"""
    parser = OzonParser()
    generator = YandexGPTGenerator()
    formatter = HTMLFormatter()
    results = []

    for product in products:
        try:
            logger.info(f"▶ Начало обработки товара {product.id}: {product.name}")
            
            # Парсинг данных с сайта
            product_data = parser.get_product_data(product.url)
            if not product_data:
                logger.warning(f"⚠ Не удалось получить данные для {product.url}")
                continue

            # Подготовка и генерация описания
            prompt_text = prepare_gpt_prompt(product_data)
            generated = generator.generate_description(product.name, prompt_text)
            
            if not generated.get('description'):
                raise ValueError("❌ GPT не сгенерировал описание")

            # Форматирование результата
            html_description = formatter.format_to_html(generated['description'])
            result = {
                'id': product.id,
                'name': product.name,
                'original_description': product_data.get('description', ''),
                'generated_description': html_description,
                'price': product_data.get('price', 'не указана'),
                'rating': product_data.get('rating', 'не указан'),
                'url': product.url,
                'status': 'success',
                'model': generated.get('model', 'yandexgpt')
            }
            results.append(result)
            logger.info(f"✅ Успешно обработан товар {product.name}")

        except Exception as e:
            logger.error(f"❌ Ошибка обработки товара {product.name}: {str(e)}")
            results.append({
                'id': product.id,
                'name': product.name,
                'url': product.url,
                'status': f'error: {str(e)}'
            })

    return results

if __name__ == "__main__":
    try:
        logger.info("=== 🚀 Запуск парсинга Ozon ===")
        print(f"🔄 Рабочая директория: {Path.cwd()}")
        print(f"🔄 Путь к credentials: {GOOGLE_CREDS_PATH}")
        print(f"🔄 Файл существует: {GOOGLE_CREDS_PATH.exists()}")
        print(f"🔄 ID таблицы: {SPREADSHEET_ID}")
        
        # Получаем список товаров
        products = get_products_to_process()
        logger.info(f"📦 Найдено товаров: {len(products)}")
        
        # Обрабатываем товары
        results = process_products(products)
        success_count = len([r for r in results if r.get('status') == 'success'])
        
        # Сохраняем результаты
        if success_count > 0:
            GoogleSheetClient().append_data(results)
            logger.info(f"💾 Успешно сохранено {success_count}/{len(products)} товаров")
        else:
            logger.error("❌ Нет данных для сохранения")
            sys.exit(1)
            
    except Exception as e:
        logger.critical(f"💥 Критическая ошибка: {str(e)}", exc_info=True)
        sys.exit(1)