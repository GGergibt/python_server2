import instaloader
from database_requests import insert_account_in_database_if_not_exists
import telebot
from sending_files import send_files_to_telegram

bot = telebot.TeleBot("1960290392:AAGWTVdvgqrmRxGbZITJ2RkBD5dpIvL4nO8", parse_mode=None)


def instaling_and_sending_instagram_profiles(chat_id, type_download, call):
    try:
        insta_acs = "insta_accounts"
        text = call.message.text
        text_name = text.lower().split(" ")[0]

        L = instaloader.Instaloader(dirname_pattern=f"{type_download}/{text_name}")
        profile = stories_download(text_name, L)

        if "instagram" in type_download:
            L.download_stories(userids=[profile])
        else:
            L.download_highlights(profile)

        send_files_to_telegram(chat_id, text_name, type_download)
        insert_account_in_database_if_not_exists(chat_id, text_name, insta_acs)

    except instaloader.exceptions.ProfileNotExistsException:
        bot.reply_to(call.message, text="make sure that account actualy exists")


def stories_download(profile: str, L: str):
    L.load_session_from_file(
        "ffvgd2020", "/home/www/.config/instaloader/session-ffvgd2021"
    )
    profile = L.check_profile_id(profile)

    return profile
