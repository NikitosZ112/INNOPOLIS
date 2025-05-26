import asyncpg
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        """Создает пул подключений к базе данных."""
        try:
            self.pool = await asyncpg.create_pool(**DB_CONFIG)
            await self._create_tables()
        except Exception as e:
            print(f"Ошибка при создании пула подключений: {e}")

    async def _create_tables(self):
        """Создает таблицы, если они не существуют."""
        async with self.pool.acquire() as conn:
            # Проверяем существование таблицы payments
            table_exists = await conn.fetchval(
                "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'payments')"
            )
            if not table_exists:
                await conn.execute('''
                    CREATE TABLE payments (
                        id SERIAL PRIMARY KEY,
                        user_id integer NOT NULL REFERENCES users(id),
                        order_id integer REFERENCES orders(id),
                        amount integer NOT NULL,
                        status varchar(20) NOT NULL DEFAULT 'pending',
                        payment_date timestamp DEFAULT CURRENT_TIMESTAMP,
                        transaction_id varchar(50)
                    )
                ''')

    async def execute(self, query, *args):
        """Выполняет SQL-запрос, который изменяет данные."""
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    async def fetch(self, query, *args):
        """Выполняет SQL-запрос, который возвращает данные."""
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchval(self, query, *args):
        """Выполняет SQL-запрос, который возвращает одно значение."""
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)