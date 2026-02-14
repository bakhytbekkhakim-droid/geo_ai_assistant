import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Ең көп таралған тұрақты модель
model = genai.GenerativeModel('gemini-pro')

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"3-нұсқа қатесі: {str(e)[:50]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
