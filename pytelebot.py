import telebot
import requests
from telebot import types
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# from youtube_dl import YoutubeDL

# from database_requestes import cursor, insert_account_in_database_if_not_exists, selecting_accounts_if_exists
from insta_download import instaling_and_sending_instagram_profiles

from sending_files import sending_file, video_downloader, send_files_to_telegram
from sending_link import (
    youtube_downloader,
    get_accounts_and_download_count,
    stored_profiles_for_user_in_db,
)

bot = telebot.TeleBot("1960290392:AAGWTVdvgqrmRxGbZITJ2RkBD5dpIvL4nO8", parse_mode=None)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

bestvideo = "best[height<=1080]"
best = "best"
text_url = ""


@bot.message_handler(commands=["start", "help"])
def starting(message):
    bot.reply_to(
        message,
        "you can download with me:   instagram stories/highlights    youtube video in 1080 or only audio   tiktok profile or tiktok video   to download stories/highlights just send name of instagram profile. remember instagram has no probels. all probels must writing as _  . To download from  youtube, send video''s url. tiktok profile wil be downloaded with name profile, for downloading one video send url. ",
    )


@bot.message_handler(commands=["insta_acs", "tt_acs"])
def starting(message):
    chat_id = message.from_user.id
    insta_text = message.text
    if "/insta_acs" in insta_text:
        select_column = "insta_accounts"
        callback_data = "stories"
    else:
        select_column = "tt_accounts"
        callback_data = "TT_profile"

    api_response_stored_accounts = get_accounts_and_download_count(
        chat_id, select_column
    )
    if not api_response_stored_accounts:
        bot.reply_to(message, text=f"make sure that you are save {select_column}")
    else:
        not_none_check = []

        for account in api_response_stored_accounts:
            keyboard = types.InlineKeyboardMarkup()
            btn_to_download = types.InlineKeyboardButton(
                text=dict(account)["profiles_column"], callback_data=callback_data
            )
            keyboard.add(btn_to_download)
            bot.reply_to(
                message,
                text=f"{dict(account)['profiles_column']} has been downloaded {dict(account)['download_count']} times",
                reply_markup=keyboard,
            )


@bot.message_handler(func=lambda message: True)
def main(message):
    global text_url
    text_url = message.text
    keyboard = types.InlineKeyboardMarkup()
    url_bin = types.InlineKeyboardButton(text="stories", callback_data="stories")
    url_bin2 = types.InlineKeyboardButton(text="Youtube", callback_data="video")
    url_bin3 = types.InlineKeyboardButton(text="YT only audio", callback_data="audio")
    url_bin4 = types.InlineKeyboardButton(text="highlights", callback_data="highlights")
    url_bin5 = types.InlineKeyboardButton(text="TT profile", callback_data="TT_profile")
    url_bin6 = types.InlineKeyboardButton(text="TT video", callback_data="TT")
    keyboard.add(url_bin, url_bin2, url_bin3, url_bin4, url_bin5, url_bin6)
    bot.reply_to(message, text=text_url, reply_markup=keyboard)
    return text_url


@bot.callback_query_handler(func=lambda call: True)
def callback_quer(call):
    chat_id = call.from_user.id
    if call.data == "video":
        key_name = "best"
        youtube_downloader(chat_id, key_name, text_url)
    elif call.data == "audio":
        key_name = "bestaudio"
        youtube_downloader(chat_id, key_name, text_url)
    elif call.data == "stories":
        instaling_and_sending_instagram_profiles(chat_id, "instagram", call)
    elif call.data == "TT_profile":
        tt_acs = "tt_accounts"
        # print(text_name)
        text = call.message.text
        text_name = text.split(" ")[0]
        # text_name = text_url
        res = video_downloader(
            f"https://www.tiktok.com/@{text_name}", best, f"tt_profile/{text_url}"
        )
        send_files_to_telegram(
            chat_id, text_name, "../django_server/django_ggrksok/media/tt_profile"
        )

        i = stored_profiles_for_user_in_db(chat_id, text_name, tt_acs)
    elif call.data == "TT":
        res = video_downloader(text_url, best, "tiktok")
        # video_response(chat_id, res, "media/tiktok")
        bot.send_video(
            chat_id, open(f"../django_server/django_ggrksok/media/tiktok/{res}", "rb")
        )

    elif call.data == "highlights":
        instaling_and_sending_instagram_profiles(chat_id, "highlights", call)


bot.polling()
