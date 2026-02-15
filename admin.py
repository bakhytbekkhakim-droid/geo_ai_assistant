import os
import sqlite3
import asyncio
import threading
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from aiogram import Bot, Dispatcher, types
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# --- БОТ БӨЛІМІ ---
API_KEY = os.getenv("GEMINI_API_KEY")
BOT_TOKEN = os.getenv("BOT_TOKEN")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_db_prompt():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT prompt FROM settings LIMIT 1")
    res = cursor.fetchone()
    conn.close()
    return res[0] if res else "Сен география пәнінен көмекшісің."

@dp.message()
async def chat(message: types.Message):
    system_prompt = get_db_prompt()
    try:
        response = model.generate_content(f"{system_prompt}\n\nСұрақ: {message.text}")
        await message.answer(response.text)
    except Exception as e:
        await message.answer(f"Қате: {str(e)[:50]}")

async def run_bot():
    await bot.delete_webhook(drop_pending_updates=True) # Conflict-ті болдырмау үшін
    await dp.start_polling(bot)

# --- ВЕБ-СЕРВЕР БӨЛІМІ ---
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.on_event("startup")
async def startup_event():
    # Ботты бөлек ағында (background) қосу
    loop = asyncio.get_event_loop()
    loop.create_task(run_bot())

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    prompt = get_db_prompt()
    return templates.TemplateResponse("index.html", {"request": request, "prompt": prompt})

@app.post("/update_prompt")
async def update_prompt(prompt: str = Form(...)):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE settings SET prompt = ? WHERE id = 1", (prompt,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
