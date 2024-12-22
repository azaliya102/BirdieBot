from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
import openai
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
tg_token = os.getenv("TELEGRAM_BOT_TOKEN")

openai.api_key = api_key

bot = Bot(token=tg_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start_handler(message: types.Message):
    await message.answer("Привет! Напиши что-нибудь, и я отвечу с помощью ChatGPT.")

@dp.message_handler()
async def chatgpt_handler(message: types.Message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты — полезный помощник."},
                {"role": "user", "content": message.text},
            ]
        )
        await message.answer(response['choices'][0]['message']['content'])
    except Exception as e:
        await message.answer(f"Ошибка: {e}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
