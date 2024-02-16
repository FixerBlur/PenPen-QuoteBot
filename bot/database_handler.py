import aiosqlite
import os


class DatabaseHandler:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                    'database', 'database.db')

    async def create_table(self):
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.cursor()
            await cursor.execute('''
                CREATE TABLE IF NOT EXISTS your_table (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    user_id INTEGER,
                    usage_count INTEGER DEFAULT 0
                );
            ''')
            await db.commit()

    async def update_command_usage(self, original_user_id, username=None):
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()

            if username:
                await cursor.execute('SELECT * FROM your_table WHERE user_id=?', (original_user_id,))
                result = await cursor.fetchone()

                if result:
                    await cursor.execute('UPDATE your_table SET username=?, usage_count=? WHERE user_id=?',
                                         (username, result[3] + 1, original_user_id))  # Incrementing usage_count
                else:
                    await cursor.execute('INSERT INTO your_table (user_id, username, usage_count) VALUES (?, ?, ?)',
                                         (original_user_id, username, 1))
            else:
                await cursor.execute('SELECT * FROM your_table WHERE user_id=?', (original_user_id,))
                result = await cursor.fetchone()

                if result:
                    usage_count = result[3] + 1  # Incrementing usage_count
                    await cursor.execute('UPDATE your_table SET usage_count=? WHERE user_id=?',
                                         (usage_count, original_user_id))
                else:
                    usage_count = 1
                    await cursor.execute('INSERT INTO your_table (user_id, usage_count) VALUES (?, ?)',
                                         (original_user_id, usage_count))

            await conn.commit()
