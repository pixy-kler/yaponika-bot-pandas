"""
bot_teacher.py - Адаптер для преподавателя (Telegram)
Использует общее ядро из core.py
"""

import asyncio
import logging

from core import (
    get_bot_and_dp, save_student, RegistrationForm, 
    bot_teacher_analytics
)
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

bot, dp = get_bot_and_dp(token_name="TELEGRAM_TOKEN")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "*Бот преподавателя японского языка*\n\n"
        "Список команд:\n"
        "`/new` - Зарегистрировать нового ученика (анкета)\n"
        "`/stats` - Посмотреть общую статистику по базе\n"
        "`/todo` - Список новых заявок, кому нужно позвонить\n"
        "`/clear` - Отменить текущую регистрацию",
        parse_mode="Markdown"
    )

@dp.message(Command("new"))
async def cmd_new_student(message: types.Message, state: FSMContext):
    await message.answer("*Шаг 1 из 7:* Введите *полное имя* ученика:", parse_mode="Markdown")
    await state.set_state(RegistrationForm.name)

@dp.message(Command("clear"))
async def cmd_clear_state(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Регистрация отменена.")

@dp.message(RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("*Шаг 2 из 7:* Дата рождения (например, 15.08.1995):")
    await state.set_state(RegistrationForm.birthday)

@dp.message(RegistrationForm.birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text.strip())
    await message.answer("*Шаг 3 из 7:* Контактный номер телефона:")
    await state.set_state(RegistrationForm.phone)

@dp.message(RegistrationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer("*Шаг 4 из 7:* Уровень японского языка (нулевичок, N5, N4, N3, N2, N1):")
    await state.set_state(RegistrationForm.level)

@dp.message(RegistrationForm.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer("*Шаг 5 из 7:* Цель обучения (Работа, стажировка, хобби, сдача JLPT):")
    await state.set_state(RegistrationForm.goal)

@dp.message(RegistrationForm.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await message.answer("*Шаг 6 из 7:* Предпочтительное время для занятий (например, пн/ср 18:00 МСК):")
    await state.set_state(RegistrationForm.preferred_time)

@dp.message(RegistrationForm.preferred_time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(preferred_time=message.text.strip())
    await message.answer("*Шаг 7 из 7 (Последний):* Дополнительные пожелания или комментарии (или напишите 'none'):")
    await state.set_state(RegistrationForm.notes)

@dp.message(RegistrationForm.notes)
async def process_notes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['notes'] = message.text.strip()
    data['tg_username'] = message.from_user.username or "Нет информации"
    
    save_student(data, source_bot="TEACHER_BOT")
    
    summary = (
        f"*Анкета ученика сохранена!*\n\n"
        f"Имя: {data['name']}\n"
        f"Дата рождения: {data['birthday']}\n"
        f"Телефон: {data['phone']}\n"
        f"Уровень: {data['level']}\n"
        f"Цель: {data['goal']}\n"
        f"Время: {data['preferred_time']}\n"
        f"Примечания: {data['notes']}"
    )
    await message.answer(summary, parse_mode="Markdown")
    
    await state.clear()

@dp.message(Command("stats"))
async def cmd_analytics(message: types.Message):
    await bot_teacher_analytics(message)

@dp.message(Command("todo"))
async def cmd_todo_list(message: types.Message):
    await bot_teacher_analytics(message, mode="todo")

async def main():
    logging.info("Бот преподавателя запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())