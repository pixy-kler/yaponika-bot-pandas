#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==========================================
# IMPORTS
# ==========================================
import os
import logging
import pandas as pd
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage

# ==========================================
# CONFIGURATION & SECURITY
# ==========================================
load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("ОШИБКА: TELEGRAM_TOKEN не найден в файле .env!")

FILE_NAME = "students_jp.csv"
logging.basicConfig(level=logging.INFO)

# ==========================================
# CORE: DATABASE (Pandas)
# ==========================================
def initialize_database():
    if not os.path.exists(FILE_NAME):
        columns = [
            'timestamp', 'tg_username', 'name', 'birthday', 'phone', 
            'level', 'goal', 'preferred_time', 'status', 'notes'
        ]
        pd.DataFrame(columns=columns).to_csv(FILE_NAME, index=False)
        logging.info(f"База данных '{FILE_NAME}' создана.")

def save_student_record(data: Dict[str, Any]) -> None:
    df = pd.read_csv(FILE_NAME)
    new_record = pd.DataFrame([data])
    df = pd.concat([df, new_record], ignore_index=True)
    df.to_csv(FILE_NAME, index=False)
    logging.info(f"Запись для {data.get('name')} сохранена.")

initialize_database()

# ==========================================
# FSM (Finite State Machine)
# ==========================================
class RegistrationForm(StatesGroup):
    name = State()
    birthday = State()
    phone = State()
    level = State()
    goal = State()
    preferred_time = State()
    notes = State()

bot = Bot(token=TELEGRAM_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# ==========================================
# COMMAND HANDLERS
# ==========================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "*CRM Bot для преподавателя Японики*\n\n"
        "Список команд:\n"
        "`/new` - Зарегистрировать нового студента\n"
        "`/stats` - Посмотреть статистику\n"
        "`/todo` - Лист ожидания (кому нужно позвонить)\n"
        "`/clear` - Отменить регистрацию",
        parse_mode="Markdown"
    )

@dp.message(Command("new"))
async def cmd_new_student(message: types.Message, state: FSMContext):
    await message.answer("*Шаг 1 из 7:* Введите *полное имя студента*:", parse_mode="Markdown")
    await state.set_state(RegistrationForm.name)

@dp.message(Command("clear"))
async def cmd_clear_state(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена.")

# ==========================================
# FSM HANDLERS (Шаги анкеты)
# ==========================================
@dp.message(RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("*Шаг 2 из 7:* Дата рождения (например, 15.08.1995):")
    await state.set_state(RegistrationForm.birthday)

@dp.message(RegistrationForm.birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text.strip())
    await message.answer("*Шаг 3 из 7:* Контактный номер:")
    await state.set_state(RegistrationForm.phone)

@dp.message(RegistrationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer("*Шаг 4 из 7:* Уровень японского (нулевичок, N5, N4, N3, N2, N1):")
    await state.set_state(RegistrationForm.level)

@dp.message(RegistrationForm.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer("*Шаг 5 из 7:* Цель (Работа, стажировка, хобби):")
    await state.set_state(RegistrationForm.goal)

@dp.message(RegistrationForm.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await message.answer("*Шаг 6 из 7:* Предпочтительное время (например, пн, ср 18:00 MSK):")
    await state.set_state(RegistrationForm.preferred_time)

@dp.message(RegistrationForm.preferred_time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(preferred_time=message.text.strip())
    await message.answer("*Шаг 7 из 7:* Дополнительная информация? (Напечатайте 'none', чтобы пропустить):")
    await state.set_state(RegistrationForm.notes)

@dp.message(RegistrationForm.notes)
async def process_notes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['notes'] = message.text.strip()
    data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
    data['status'] = 'Новенький (Нужно связаться)'
    data['tg_username'] = message.from_user.username or "Нет информации"

    save_student_record(data)

    summary = (
        f"*Зарегистрирован!*\n\n"
        f"Имя: {data['name']}\n"
        f"День рождения: {data['birthday']}\n"
        f"Телефон: {data['phone']}\n"
        f"Уровень: {data['level']}\n"
        f"Цель: {data['goal']}\n"
        f"Время: {data['preferred_time']}"
    )
    await message.answer(summary, parse_mode="Markdown")
    await state.clear()

# ==========================================
# ANALYTICS & TODO
# ==========================================
@dp.message(Command("stats"))
async def cmd_analytics(message: types.Message):
    df = pd.read_csv(FILE_NAME)
    if df.empty:
        await message.answer("В базе ещё нет студентов.")
        return

    total = len(df)
    active = len(df[df['status'] != 'Archived'])
    conversion = round((active / total) * 100, 1) if total > 0 else 0

    report_lines = [
        "*Статистика базы:*",
        f"**Всего заявок:** {total}",
        f"**Активных учеников:** {active}",
        f"**Конверсия:** {conversion}%"
    ]
    await message.answer("\n".join(report_lines), parse_mode="Markdown")

@dp.message(Command("todo"))
async def cmd_todo(message: types.Message):
    df = pd.read_csv(FILE_NAME)
    pending = df[df['status'] == 'Новенький (Нужно связаться)']

    if pending.empty:
        await message.answer("Все заявки обработаны. Отдыхайте!")
        return

    reply = ["📞 *Нужно позвонить этим людям:*\n"]
    for _, row in pending.iterrows():
        reply.append(f"{row['name']}")
        reply.append(f"{row['phone']}")
        reply.append(f"{row['timestamp']}\n")

    await message.answer("\n".join(reply), parse_mode="Markdown")

# ==========================================
# APPLICATION ENTRY POINT
# ==========================================
async def main():
    logging.info("Telegram Bot запущен и готов к работе...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен вручную.")
