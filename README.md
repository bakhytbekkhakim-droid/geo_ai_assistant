# Geo AI Assistant (Telegram Bot - Python)

An AI-powered Telegram assistant bot built with Python, utilizing the Google Gemini API for generating responses. This project also includes a FastAPI-based admin panel to manage the bot's core prompt.

## Features

*   **Telegram Integration:** Responds to user messages via a Telegram bot.
*   **AI-Powered Responses:** Uses Google Gemini API (`gemini-1.5-flash-latest`) for generating conversational replies.
*   **Admin Panel:** A web-based interface (FastAPI) to dynamically update the bot's main prompt, allowing for easy customization of its persona or knowledge base.
*   **Database Integration:** Uses SQLite (`database.db`) to store the bot's prompt settings.

## Setup Instructions

Follow these steps to get your Geo AI Assistant up and running.

### 1. Clone the Repository

```bash
git clone https://github.com/bakhytbekkhakim-droid/geo_ai_assistant.git
cd geo_ai_assistant
```

### 2. Create and Configure `.env` File

Create a file named `.env` in the root directory of the project. This file will store your API keys and other sensitive information. You can use the provided `.env.example` as a template.

```ini
# .env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"
ADMIN_USERNAME="admin_user"
ADMIN_PASSWORD="admin_password"
```

*   **`GEMINI_API_KEY`**: Obtain this from the Google AI Studio.
*   **`BOT_TOKEN`**: Get this from BotFather on Telegram.
*   **`ADMIN_USERNAME`** and **`ADMIN_PASSWORD`**: Set these for your admin panel login. Default values are `admin` and `12345` if not set.

### 3. Install Dependencies

It's highly recommended to use a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python3 bot.py
```

Your Telegram bot should now be running and responding to messages.

### 5. Run the Admin Panel

In a separate terminal, activate your virtual environment and run the admin panel:

```bash
source venv/bin/activate
python3 admin.py
```

The admin panel will be accessible at `http://127.0.0.1:10000` (or `http://0.0.0.0:10000` if deployed). You can log in using the `ADMIN_USERNAME` and `ADMIN_PASSWORD` you set in your `.env` file to update the bot's prompt.

## Project Structure

*   `bot.py`: Main Telegram bot logic.
*   `admin.py`: FastAPI application for the admin panel.
*   `database.py`: (Not directly used in `admin.py` or `bot.py` based on current code, but likely intended for shared DB logic or future expansion).
*   `requirements.txt`: Python dependencies.
*   `templates/index.html`: HTML template for the admin panel.
*   `.env.example`: Example environment variables file.
*   `.gitignore`: Specifies intentionally untracked files to ignore.

## Contributing

Feel free to fork the repository, make improvements, and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is open-source and available under the MIT License. (Add if applicable)
