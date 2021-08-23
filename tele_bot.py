from __future__ import unicode_literals
from typing import cast
import telegram, logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
from os import listdir
from os.path import isfile, join
import os

# context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
TOKEN: str = ""
bot = telegram.Bot(token=TOKEN)
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

PATH: str = os.getcwd()

ydl_mp3 = {
    "outtmpl": PATH + "/mp3/%(id)s.%(ext)s",
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}
ydl_vid = {"format": "136", "outtmpl": PATH + "/vid/%(id)s.%(ext)s"}
# 137: 1080p
# 136: 720p
# 135: 480p
# 134: 360p
# 133: 240p


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Welcome to ProWily MP3 Bot\nTo convert Youtube video to MP3 file just write ".p3 URL"',
    )


def echo(update, context):

    context.bot.send_message(chat_id=update.effective_chat.id, text="Wait Please")

    file = ""
    url: str = update.message.text
    if ".mp3" in url:
        url = url.replace(".mp3 ", "")
        with youtube_dl.YoutubeDL(ydl_mp3) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            file = f"{info.get('id', None)}.mp3"
        context.bot.send_audio(
            chat_id=update.effective_chat.id, audio=open(f"{PATH}/mp3/{file}", "rb")
        )

    elif ".mp4" in update.message.text:
        url = url.replace(".mp4 ", "")
        with youtube_dl.YoutubeDL(ydl_vid) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            file = f"{info.get('id', None)}.mp4"
        try:
            bot.send_video(
                chat_id=update.message.chat_id,
                video=open(f"{PATH}/vid/{file}", "rb"),
                supports_streaming=True,
            )
        except telegram.error.NetworkError:
            context.bot.send_message(chat_id=update.effective_chat.id, text="")

    # os.remove(file)
    context.bot.send_message(chat_id=update.effective_chat.id, text="")


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


print(bot.get_me())
updater.start_polling()
