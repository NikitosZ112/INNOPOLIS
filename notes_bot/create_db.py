import asyncpg
import asyncio
import os
from dotenv import load_dotenv

async def test_connection(db_config):
    """Проверяет соединение с базой данных"""
    try:
        conn = await asyncpg.connect(**db_config)
        await conn.close()
        return True, None
    except Exception as e:
        return False, str(e)

async def create_tables(db_config):
    """Создает таблицы в базе данных"""
    try:
        conn = await asyncpg.connect(**db_config)
        await conn.execute('''
            CREATE TABLE IF NOT EXISTS notes (
                id SERIAL PRIMARY KEY,
                user_id BIGINT NOT NULL,
                note_text TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            )
        ''')
        await conn.close()
        return True, "Таблицы успешно созданы!"
    except Exception as e:
        return False, f"Ошибка при создании таблиц: {str(e)}"

async def setup_database():
    """Основная функция настройки базы данных"""
    load_dotenv()

    # Получаем параметры подключения
    db_config = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'database': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD')
    }

    # Проверяем заполненность всех параметров
    missing = [k for k, v in db_config.items() if not v]
    if missing:
        print(f"Ошибка: Не указаны следующие параметры в .env файле: {', '.join(missing)}")
        return

    # Проверяем корректность порта
    try:
        db_config['port'] = int(db_config['port'])
    except ValueError:
        print("Ошибка: Порт должен быть числом")
        return

    print("Проверяем подключение к серверу PostgreSQL...")
    
    # Проверяем подключение к серверу (к системной базе postgres)
    server_config = db_config.copy()
    server_config['database'] = 'postgres'
    connected, error = await test_connection(server_config)
    
    if not connected:
        print(f"Ошибка подключения к серверу PostgreSQL: {error}")
        print("\nВозможные причины:")
        print(f"1. Неправильный хост: {db_config['host']}")
        print(f"2. Неправильный порт: {db_config['port']}")
        print(f"3. Неправильный пользователь: {db_config['user']}")
        print(f"4. Неправильный пароль: {'*' * len(db_config['password']) if db_config['password'] else 'не указан'}")
        print("5. Сервер PostgreSQL не запущен")
        print("6. Проблемы с сетевым подключением")
        return

    print("Подключение к серверу PostgreSQL успешно!")

    # Проверяем существование базы данных
    try:
        # Пробуем подключиться к указанной базе данных
        connected, error = await test_connection(db_config)
        if connected:
            print(f"База данных '{db_config['database']}' уже существует")
        else:
            # Если базы нет, создаем ее
            print(f"База данных '{db_config['database']}' не существует, создаем...")
            conn = await asyncpg.connect(**server_config)
            await conn.execute(f"CREATE DATABASE {db_config['database']}")
            await conn.close()
            print(f"База данных '{db_config['database']}' успешно создана!")
    except Exception as e:
        print(f"Ошибка при создании базы данных: {str(e)}")
        return

    # Создаем таблицы
    success, message = await create_tables(db_config)
    print(message)

if __name__ == '__main__':
    asyncio.run(setup_database())