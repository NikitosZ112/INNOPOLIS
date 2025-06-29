import logging
import sys
from pathlib import Path
from config.settings import LOG_FILE

def setup_logger(name: str) -> logging.Logger:
    """
    Настройка логгера с записью в файл и выводом в консоль
    (без внешних зависимостей)
    """
    # Создаем папку для логов
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Создаем логгер
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Формат сообщений
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 1. Хендлер для записи в файл (без ротации)
    file_handler = logging.FileHandler(
        filename=LOG_FILE,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # 2. Хендлер для вывода в консоль
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # Очищаем старые хендлеры (если есть)
    logger.handlers.clear()

    # Добавляем хендлеры
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def get_logger(name: str) -> logging.Logger:
    """Получение настроенного логгера"""
    return setup_logger(name)