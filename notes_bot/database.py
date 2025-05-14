import asyncpg
from config import DB_CONFIG

class Database:
    def __init__(self):
        self.pool = None

    async def create_pool(self):
        self.pool = await asyncpg.create_pool(**DB_CONFIG)
        await self._create_tables()

    async def _create_tables(self):
        async with self.pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS notes (
                    id SERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL,
                    note_text TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            ''')

    async def add_note(self, user_id: int, note_text: str):
        async with self.pool.acquire() as conn:
            await conn.execute(
                'INSERT INTO notes (user_id, note_text) VALUES ($1, $2)',
                user_id, note_text
            )

    async def get_notes(self, user_id: int):
        async with self.pool.acquire() as conn:
            return await conn.fetch(
                'SELECT id, note_text FROM notes WHERE user_id = $1 ORDER BY created_at DESC',
                user_id
            )

    async def delete_note(self, user_id: int, note_id: int):
        async with self.pool.acquire() as conn:
            return await conn.execute(
                'DELETE FROM notes WHERE user_id = $1 AND id = $2',
                user_id, note_id
            ) == 'DELETE 1'

# Создаем глобальный экземпляр базы данных
db = Database()