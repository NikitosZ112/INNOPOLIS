import requests
import json
from config.settings import YANDEX_FOLDER_ID
from src.utils.yandex_auth import YandexAuth
from src.utils.logger import get_logger

logger = get_logger(__name__)

class YandexGPTGenerator:
    def __init__(self):
        """Инициализация генератора через HTTP API"""
        self.api_url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
        self.model_uri = "gpt://b1gqvj2h1dj7qcf3vq2r/yandexgpt-lite/latest"  # Замените на ваш model_uri
        
    def generate_description(self, product_name: str, base_text: str) -> dict:
        """
        Генерирует SEO-описание товара через Yandex GPT HTTP API
        
        Аргументы:
            product_name: Название товара
            base_text: Базовый текст для генерации
            
        Возвращает:
            Словарь с результатом:
            - description: сгенерированный текст
            - model: используемая модель
            - status: статус выполнения
        """
        try:
            # Получаем IAM-токен
            iam_token = YandexAuth.get_iam_token()
            if not iam_token:
                raise ValueError("Не удалось получить IAM токен")
            
            # Формируем заголовки запроса
            headers = {
                "Authorization": f"Bearer {iam_token}",
                "x-folder-id": YANDEX_FOLDER_ID,
                "Content-Type": "application/json"
            }
            
            # Формируем тело запроса
            payload = {
                "modelUri": self.model_uri,
                "completionOptions": {
                    "stream": False,
                    "temperature": 0.7,
                    "maxTokens": 2000
                },
                "messages": [
                    {
                        "role": "user",
                        "text": f"Сгенерируй SEO-описание для {product_name} на основе: {base_text}"
                    }
                ]
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            result = response.json()
            if not result.get("result", {}).get("alternatives"):
                raise ValueError("Нет вариантов ответа в результате")
                
            return {
                "description": result["result"]["alternatives"][0]["message"]["text"],
                "model": "yandexgpt-lite",
                "status": "success"
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка HTTP запроса: {str(e)}")
            return {
                "description": "",
                "model": "yandexgpt-lite",
                "status": f"HTTP error: {str(e)}"
            }
        except Exception as e:
            logger.error(f"Ошибка генерации: {str(e)}", exc_info=True)
            return {
                "description": "",
                "model": "error",
                "status": str(e)
            }