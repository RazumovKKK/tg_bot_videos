import os

import asyncio

import logging

from request import Get_Requests

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message



from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(F.text)
async def get_theme_news(message:Message):

    string = Get_Requests.make_request(message.text)
    await message.answer(str(string))



async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot Exit")
