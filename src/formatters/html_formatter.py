import re
from typing import List

class HTMLFormatter:
    @staticmethod
    def format_to_html(raw_text: str) -> str:
        """Конвертирует текст в HTML по правилам Dental First"""
        # Удаляем лишние пробелы
        text = re.sub(r'\s+', ' ', raw_text).strip()
        
        # Заменяем маркеры списков
        text = re.sub(r'(\d+\.|\•|\-)', '<li>', text)
        
        # Разбиваем на абзацы
        paragraphs = [f"<p>{p.strip()}</p>" for p in text.split('\n') if p.strip()]
        
        return '\n'.join(paragraphs)