import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
# Render-дегі Environment Variables-ден алынады
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Модель аты нақтыланған
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message()
async def chat(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"1-нұсқа қатесі: {str(e)[:50]}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
