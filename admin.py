import os
import sqlite3
from fastapi import FastAPI, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_303_SEE_OTHER
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Шаблондар мен логин мәліметтері
templates = Jinja2Templates(directory="templates")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "12345")

# Мәліметтер қорын дайындау
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY, prompt TEXT)''')
    # Егер кесте бос болса, бастапқы промптты қосу
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO settings (prompt) VALUES (?)", ("Сен география пәнінен көмекшісің.",))
    conn.commit()
    conn.close()

init_db()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # index.html файлын шаблондар папкасынан шақыру
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT prompt FROM settings LIMIT 1")
    prompt = cursor.fetchone()[0]
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "prompt": prompt})

@app.post("/update_prompt")
async def update_prompt(prompt: str = Form(...)):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE settings SET prompt = ? WHERE id = 1", (prompt,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=HTTP_303_SEE_OTHER)

# Render-де жұмыс істеу үшін портты баптау
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10000)
