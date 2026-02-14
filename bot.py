import os
import asyncio
import logging
import sqlite3
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Логтарды қосу (қателерді көру үшін)
logging.basicConfig(level=logging.INFO)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Gemini баптау (ең тұрақты модель атымен)
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_system_prompt():
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT prompt FROM settings LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else "Сен география пәнінен көмекшісің."
    except Exception as e:
        logging.error(f"DB қатесі: {e}")
        return "Сен география пәнінен көмекшісің."

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Сәлем! Мен География пәнінен AI көмекшімін. Сұрағыңызды қойсаңыз болады.")

@dp.message()
async def chat_handler(message: types.Message):
    system_prompt = get_system_prompt()
    user_input = message.text
    
    try:
        # Gemini-ге сұраныс жіберу (түзетілген формат)
        response = model.generate_content(f"Инструкция: {system_prompt}\n\nПайдаланушы: {user_input}")
        
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Кешіріңіз, Gemini жауап бере алмады.")
            
    except Exception as e:
        logging.error(f"Gemini қатесі: {e}")
        # Егер қате шықса, нақты қандай қате екенін көру үшін:
        await message.answer(f"Қате орын алды: {str(e)[:50]}...")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
