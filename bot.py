import os
import asyncio
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

load_dotenv()
# Render-дегі GEMINI_API_KEY-ді қолдану
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Ең сенімді модель нұсқасы
model = genai.GenerativeModel('gemini-1.5-flash-latest')

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

@dp.message()
async def chat_handler(message: types.Message):
    try:
        # Gemini-ге сұраныс жіберу
        response = model.generate_content(message.text)
        if response.text:
            await message.answer(response.text)
        else:
            await message.answer("Gemini жауап бермеді (Empty response).")
    except Exception as e:
        # Нақты қате кодын Telegram-ға шығару
        error_msg = str(e)
        await message.answer(f"Техникалық қате: {error_msg[:100]}")

async def main():
    # Ботты қосу
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
