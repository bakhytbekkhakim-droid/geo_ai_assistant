import aiosqlite

DB_NAME = "chat_history.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""CREATE TABLE IF NOT EXISTS history (
            user_id INTEGER,
            role TEXT,
            content TEXT
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS blocked_users (
            user_id INTEGER PRIMARY KEY
        )""")
        await db.execute("""CREATE TABLE IF NOT EXISTS prompt (
            id INTEGER PRIMARY KEY,
            content TEXT
        )""")
        await db.commit()

async def save_message(user_id, role, content):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT INTO history (user_id, role, content) VALUES (?, ?, ?)",
            (user_id, role, content)
        )
        await db.commit()

async def get_history(user_id, limit=10):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT role, content FROM history WHERE user_id=? ORDER BY rowid DESC LIMIT ?",
            (user_id, limit)
        )
        rows = await cursor.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]

async def is_blocked(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT 1 FROM blocked_users WHERE user_id=?", (user_id,)
        )
        return await cursor.fetchone() is not None

async def get_prompt():
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT content FROM prompt WHERE id=1"
        )
        row = await cursor.fetchone()
        return row[0] if row else "Сен жеке AI көмекшісің."

async def set_prompt(content):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO prompt (id, content) VALUES (1, ?)",
            (content,)
        )
        await db.commit()
