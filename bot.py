import os
import asyncio
import logging
import sqlite3
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Айнымалыларды жүктеу
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Gemini баптау
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Деректер қорынан промпт алу функциясы
def get_system_prompt():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT prompt FROM settings LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Сен география пәнінен көмекшісің."
    except:
        return "Сен география пәнінен көмекшісің."

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Сәлем! Мен География пәнінен AI көмекшімін. Сұрағыңызды қойсаңыз болады.")

@dp.message()
async def chat_handler(message: types.Message):
    system_prompt = get_system_prompt()
    user_input = message.text
    
    try:
        # Gemini-ге сұраныс жіберу
        response = model.generate_content(f"{system_prompt}\n\nПайдаланушы сұрағы: {user_input}")
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Қате: {e}")
        await message.answer("Кешіріңіз, сұранысты өңдеу кезінде қате шықты.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
