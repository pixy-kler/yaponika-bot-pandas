import os
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TELEGRAM_TOKEN:
    raise ValueError("Токен не найден в .env!")

FILE_NAME = "students_jp.csv"
logging.basicConfig(level=logging.INFO)

def init_db():
    if not os.path.exists(FILE_NAME):
        columns = ['timestamp', 'tg_username', 'name', 'birthday', 'phone', 
                   'level', 'goal', 'preferred_time', 'status', 'notes', 'source_bot']
        pd.DataFrame(columns=columns).to_csv(FILE_NAME, index=False)
        logging.info(f"База '{FILE_NAME}' создана.")

def save_student(data: Dict[str, Any], source_bot: str):
    df = pd.read_csv(FILE_NAME)
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    data['status'] = 'Новенький (Нужно связаться)'
    data['source_bot'] = source_bot
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    logging.info(f"📝 Данные сохранены из бота: {source_bot}")

init_db()

class RegistrationForm(StatesGroup):
    name = State()
    birthday = State()
    phone = State()
    level = State()
    goal = State()
    preferred_time = State()
    notes = State()

def get_bot_and_dp(token_name: str = "TELEGRAM_TOKEN"):

    token = os.getenv(token_name)
    if not token:
        raise ValueError(f"Токен {token_name} не найден в .env!")
    bot = Bot(token=token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    return bot, dp

async def bot_teacher_analytics(message: types.Message, mode: str = "stats"):
    """Общая функция для /stats и /todo."""
    df = pd.read_csv(FILE_NAME)
    
    if mode == "stats":
        if df.empty:
            await message.answer("📭 В базе пока нет учеников.")
            return

        total = len(df)
        active = len(df[df['status'] != 'Archived'])
        conversion = round((active / total) * 100, 1) if total > 0 else 0

        report = [
            "*Статистика базы:*",
            f"**Всего заявок:** {total}",
            f"**Активных учеников:** {active}",
            f"**Конверсия:** {conversion}%"
        ]
        await message.answer("\n".join(report), parse_mode="Markdown")
    
    elif mode == "todo":
        pending = df[df['status'] == 'Новенький (Нужно связаться)']
        if pending.empty:
            await message.answer("Все заявки обработаны. Отдыхайте!")
            return
        
        reply = ["*Нужно связаться:*\n"]
        for _, row in pending.iterrows():
            reply.append(f"{row['name']}")
            reply.append(f"{row['phone']}")
            reply.append(f"{row['timestamp']}\n")
        await message.answer("\n".join(reply), parse_mode="Markdown")
