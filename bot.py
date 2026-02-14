import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from openai import OpenAI
from database import save_message, get_history, is_blocked, get_prompt, init_db

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

asyncio.run(init_db())

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("🤖 Жеке AI көмекші іске қосылды!")

@dp.message()
async def ai_handler(message: types.Message):
    user_id = message.from_user.id

    if await is_blocked(user_id):
        return

    await save_message(user_id, "user", message.text)
    history = await get_history(user_id)
    system_prompt = await get_prompt()

    messages = [{"role": "system", "content": system_prompt}] + history

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    reply = response.choices[0].message.content
    await save_message(user_id, "assistant", reply)
    await message.answer(reply)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
