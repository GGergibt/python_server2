import yt_dlp
from telebot import types
import telebot
import os

# def video_response(chat_id, text_url, directory, bot):
#     folder = f"./{directory}/{text_url}"
#     bot.send_video(chat_id, open(f"{folder}", "rb"))

bot = telebot.TeleBot("1960290392:AAGWTVdvgqrmRxGbZITJ2RkBD5dpIvL4nO8", parse_mode=None)


def video_downloader(url: str, query_format, folder):
    ydl_opts = {
        "format": query_format,
        "outtmpl": f"../django_server/django_ggrksok/media/{folder}/%(id)s.%(ext)s",
        "noplaylist": True,
        "extract-audio": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        video_id = info_dict.get("id")
        video_ext = info_dict.get("ext")
    file_response = f"{video_id}.{video_ext}"
    return file_response


def sending_file(res, chat_id):
    req = f"https://ggrksok.fun/media/youtube/{res}"
    keyboard = types.InlineKeyboardMarkup()
    url_bin = types.InlineKeyboardButton(text="Load", url=req, reply_markup=keyboard)
    keyboard.add(url_bin)
    bot.send_message(chat_id, text="Load", reply_markup=keyboard)


def send_files_to_telegram(chat_id, text_url, directory):
    folder = f"./{directory}/{text_url}"
    print(folder)
    for r, m, d in os.walk(folder):
        for file in sorted(d):
            if ".jpg" in file:
                bot.send_photo(chat_id, open(f"{folder}/{file}", "rb"))
            elif ".mp4" in file:
                bot.send_video(chat_id, open(f"{folder}/{file}", "rb"))
