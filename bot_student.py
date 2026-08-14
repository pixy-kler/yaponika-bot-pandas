"""
bot_student.py - Адаптер для учеников (Telegram)
Позволяет ученикам самостоятельно оставлять заявки на обучение.
Использует общее ядро из core.py
"""

import asyncio
import logging

from core import get_bot_and_dp, save_student, RegistrationForm
from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

bot, dp = get_bot_and_dp(token_name="STUDENT_TOKEN")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "*Добро пожаловать в Японику!*\n\n"
        "Этот бот поможет нам записать вас на курсы японского языка.\n"
        "Нажмите `/reg`, чтобы заполнить анкету.\n\n"
        "*Важно:* Все ваши данные в безопасности и используются только для связи с вами.",
        parse_mode="Markdown"
    )

@dp.message(Command("reg"))
async def cmd_reg_student(message: types.Message, state: FSMContext):
    await message.answer("*Шаг 1 из 7:* Как вас зовут?:", parse_mode="Markdown")
    await state.set_state(RegistrationForm.name)

@dp.message(Command("clear"))
async def cmd_clear_state(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Анкетирование отменено. Если передумаете, введите `/reg`.")


@dp.message(RegistrationForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text.strip())
    await message.answer("*Шаг 2 из 7:* Ваша дата рождения (например, 15.08.1995):")
    await state.set_state(RegistrationForm.birthday)

@dp.message(RegistrationForm.birthday)
async def process_birthday(message: types.Message, state: FSMContext):
    await state.update_data(birthday=message.text.strip())
    await message.answer("*Шаг 3 из 7:* Ваш номер телефона (для связи с вами):")
    await state.set_state(RegistrationForm.phone)

@dp.message(RegistrationForm.phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text.strip())
    await message.answer("*Шаг 4 из 7:* Ваш уровень японского языка (выберите):\n"
                         "▫️ нулевичок\n"
                         "▫️ N5 (начальный)\n"
                         "▫️ N4 (базовый)\n"
                         "▫️ N3 (средний)\n"
                         "▫️ N2 (выше среднего)\n"
                         "▫️ N1 (продвинутый)")
    await state.set_state(RegistrationForm.level)

@dp.message(RegistrationForm.level)
async def process_level(message: types.Message, state: FSMContext):
    await state.update_data(level=message.text.strip())
    await message.answer("*Шаг 5 из 7:* Какая у вас цель изучения языка?\n"
                         "▫️ Работа в японской компании\n"
                         "▫️ Стажировка в Японии\n"
                         "▫️ Сдача экзамена JLPT\n"
                         "▫️ Хобби / Для души\n"
                         "▫️ Переезд в Японию")
    await state.set_state(RegistrationForm.goal)

@dp.message(RegistrationForm.goal)
async def process_goal(message: types.Message, state: FSMContext):
    await state.update_data(goal=message.text.strip())
    await message.answer("*Шаг 6 из 7:* В какое время вам удобно заниматься?\n"
                         "Напишите дни недели и время (например: *пн/ср 18:00 МСК*):")
    await state.set_state(RegistrationForm.preferred_time)

@dp.message(RegistrationForm.preferred_time)
async def process_time(message: types.Message, state: FSMContext):
    await state.update_data(preferred_time=message.text.strip())
    await message.answer("*Шаг 7 из 7 (Последний):* Есть ли у вас дополнительные пожелания или вопросы?\n"
                         "(Если нет, просто напишите 'нет'):")
    await state.set_state(RegistrationForm.notes)

@dp.message(RegistrationForm.notes)
async def process_notes(message: types.Message, state: FSMContext):
    data = await state.get_data()
    data['notes'] = message.text.strip()
    data['tg_username'] = message.from_user.username or "Не указан"
    
    save_student(data, source_bot="STUDENT_BOT")
    
    summary = (
        f"*Спасибо, {data['name']}!*\n\n"
        f"Ваша заявка успешно отправлена.\n"
        f"Мы свяжемся с вами по номеру: {data['phone']}\n"
        f"В ближайшее время вам напишет наш преподаватель.\n\n"
        f"*Ваши данные:*\n"
        f"Дата рождения: {data['birthday']}\n"
        f"Уровень: {data['level']}\n"
        f"Цель: {data['goal']}\n"
        f"Удобное время: {data['preferred_time']}"
    )
    await message.answer(summary, parse_mode="Markdown")
    
    await state.clear()


async def main():
    logging.info("Бот запущен и готов к приёму заявок!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())