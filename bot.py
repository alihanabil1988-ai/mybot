import asyncio
import os
import json
import socket
from aiohttp import TCPConnector
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from dotenv import load_dotenv


# =========================
# TOKEN
# =========================

load_dotenv()

TOKEN = os.environ.get("TOKEN")

if not TOKEN:
    raise ValueError("TOKEN табылмады! .env файлын тексер.")


dp = Dispatcher()


# =========================
# USERS.JSON
# =========================

FILE_NAME = "users.json"


def load_users():
    """users.json файлынан қолданушыларды жүктеу."""

    if not os.path.exists(FILE_NAME):
        return {}

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)

    except (json.JSONDecodeError, FileNotFoundError):
        return {}


def save_users():
    """Қолданушыларды users.json файлына сақтау."""

    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(
            users,
            file,
            ensure_ascii=False,
            indent=4
        )


users = load_users()


# =========================
# КНОПКАЛАР
# =========================

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💾 Сохранить данные"),
            KeyboardButton(text="👤 Мой профиль")
        ],
        [
            KeyboardButton(text="❓ Помощь")
        ]
    ],
    resize_keyboard=True
)


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: types.Message):

    await message.answer(
        "Привет! 👋\n\n"
        "Выбери кнопку:",
        reply_markup=keyboard
    )


# =========================
# СОХРАНИТЬ ДАННЫЕ
# =========================

@dp.message(lambda message: message.text == "💾 Сохранить данные")
async def save_start(message: types.Message):

    user_id = str(message.from_user.id)

    if user_id not in users:
        users[user_id] = {
            "name": None,
            "movie": None
        }

    save_users()

    await message.answer(
        "👤 Напиши своё имя:"
    )


# =========================
# ПОЛУЧАЕМ ИМЯ
# =========================

@dp.message(
    lambda message:
    str(message.from_user.id) in users
    and users[str(message.from_user.id)]["name"] is None
)
async def get_name(message: types.Message):

    user_id = str(message.from_user.id)

    users[user_id]["name"] = message.text

    save_users()

    await message.answer(
        "🎬 Теперь напиши свой любимый фильм:"
    )


# =========================
# ПОЛУЧАЕМ ФИЛЬМ
# =========================

@dp.message(
    lambda message:
    str(message.from_user.id) in users
    and users[str(message.from_user.id)]["movie"] is None
)
async def get_movie(message: types.Message):

    user_id = str(message.from_user.id)

    users[user_id]["movie"] = message.text

    save_users()

    user = users[user_id]

    await message.answer(
        "✅ Данные сохранены!\n\n"
        f"👤 Имя: {user['name']}\n"
        f"🎬 Любимый фильм: {user['movie']}",
        reply_markup=keyboard
    )


# =========================
# МОЙ ПРОФИЛЬ
# =========================

@dp.message(lambda message: message.text == "👤 Мой профиль")
async def profile(message: types.Message):

    user_id = str(message.from_user.id)

    user = users.get(user_id)

    if not user:
        await message.answer(
            "❌ Данные ещё не сохранены.\n\n"
            "Нажми 💾 Сохранить данные"
        )
        return

    if not user.get("name") or not user.get("movie"):
        await message.answer(
            "❌ Данные ещё не заполнены полностью.\n\n"
            "Нажми 💾 Сохранить данные"
        )
        return

    await message.answer(
        "👤 МОЙ ПРОФИЛЬ\n\n"
        f"Имя: {user['name']}\n"
        f"🎬 Любимый фильм: {user['movie']}"
    )


# =========================
# ПОМОЩЬ
# =========================

@dp.message(lambda message: message.text == "❓ Помощь")
async def help_command(message: types.Message):

    await message.answer(
        "❓ ПОМОЩЬ\n\n"
        "💾 Сохранить данные — сохранить имя и фильм.\n\n"
        "👤 Мой профиль — посмотреть свои данные.\n\n"
        "❓ Помощь — показать эту инструкцию."
    )


# =========================
# ЗАПУСК БОТА
# =========================

async def main():
    connector = TCPConnector(family=socket.AF_INET)
    session = AiohttpSession(connector=connector)
    bot = Bot(token=TOKEN, session=session)

    print("Бот запущен!")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())