import asyncio
import logging
import sys
import os

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import FSInputFile
from dotenv import load_dotenv
from yt_dlp import YoutubeDL

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
dp = Dispatcher()
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)


def download_mp3(url):
    current_directory = os.getcwd()

    ydl_opts = {
        "outtmpl": current_directory + "/downloads/%(title)s.%(ext)s",
        "format": "m4a/bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
            }
        ],
    }

    ydl = YoutubeDL(ydl_opts)
    info = ydl.extract_info(url, download=True)
    title = info.get("title", "Title is not available.")

    return title


@dp.message()
async def echo_handler(message: types.Message) -> None:
    audio_title = download_mp3(message.text)

    audio = FSInputFile(f"downloads/{audio_title}.mp3")

    try:
        await bot.send_audio(chat_id=message.chat.id, audio=audio)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
