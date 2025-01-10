import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
tg_token = os.getenv("TELEGRAM_BOT_TOKEN")

if api_key is None or tg_token is None:
    raise ValueError("Не найдены переменные окружения OPENAI_API_KEY или TELEGRAM_BOT_TOKEN")

client = OpenAI(api_key=api_key)

bot = Bot(token=tg_token)
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    await message.answer("Привет! Напиши что-нибудь, и я отвечу с помощью ChatGPT.")

@dp.message()
async def chatgpt_handler(message: Message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты — полезный помощник."},
                {"role": "user", "content": message.text},
            ],
        )
        await message.answer(response.choices[0].message.content)
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

async def main():
    dp.message.register(start_handler)
    dp.message.register(chatgpt_handler)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
