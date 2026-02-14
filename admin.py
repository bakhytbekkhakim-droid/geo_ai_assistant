from fastapi import FastAPI, Request, Depends, HTTPException, status, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from database import set_prompt, init_db
import aiosqlite, os
import asyncio

asyncio.run(init_db())

app = FastAPI()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()

ADMIN_USER = os.getenv("ADMIN_USER")
ADMIN_PASS = os.getenv("ADMIN_PASS")

def auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Қате логин немесе пароль",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/")
async def dashboard(request: Request, username: str = Depends(auth)):
    async with aiosqlite.connect("chat_history.db") as db:
        cursor = await db.execute("SELECT COUNT(DISTINCT user_id) FROM history")
        users = await cursor.fetchone()
        cursor = await db.execute("SELECT COUNT(*) FROM history")
        messages = await cursor.fetchone()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users[0],
        "messages": messages[0]
    })

@app.get("/prompt")
async def edit_prompt(request: Request, username: str = Depends(auth)):
    async with aiosqlite.connect("chat_history.db") as db:
        cursor = await db.execute("SELECT content FROM prompt WHERE id=1")
        row = await cursor.fetchone()
        current = row[0] if row else ""
    return templates.TemplateResponse("prompt.html", {
        "request": request,
        "current": current
    })

@app.post("/prompt")
async def update_prompt(request: Request, new_prompt: str = Form(...), username: str = Depends(auth)):
    await set_prompt(new_prompt)
    return RedirectResponse("/prompt", status_code=303)
