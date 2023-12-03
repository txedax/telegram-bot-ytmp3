import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from pytube import YouTube
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


@dp.message()
async def echo_handler(message: types.Message) -> None:
    yt = YouTube(message.text)
    video = yt.streams.filter(only_audio=True).first()
    output_file = video.download(output_path="downloads")
    new_file = output_file.replace(".mp4", ".mp3")
    os.rename(output_file, new_file)

    audio = FSInputFile(new_file)

    try:
        await bot.send_audio(chat_id=message.chat.id, audio=audio)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
