import telebot
from telebot import types
import requests
# from youtube_dl import YoutubeDL
import instaloader
import os
import yt_dlp
# from database_requestes import cursor, insert_account_in_database_if_not_exists, selecting_accounts_if_exists
from database_requests import cursor, selecting_accounts_if_exists, insert_account_in_database_if_not_exists, selecting_download_count_if_exists

bot = telebot.TeleBot("1960290392:AAGWTVdvgqrmRxGbZITJ2RkBD5dpIvL4nO8", parse_mode=None)

bestvideo = "best[height<=1080]"
best = "best"
text_url = ""

@bot.message_handler(commands=["start", "help"])
def starting(message):
    bot.reply_to(message, "send to me youtube link")

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
        
    insta_acs = selecting_accounts_if_exists(cursor, chat_id, select_column)
    insta_counts = selecting_download_count_if_exists(cursor, chat_id, select_column)

    download_count = []
    not_none_check = []
    # if insta_acs:
    for names in  insta_counts:
        for name_account in names:
            download_count.append(name_account)


    count = -1
    for insta_profile in insta_acs:
        for name_account in insta_profile:
            if name_account != None:
                count += 1
                print(count)
                keyboard = types.InlineKeyboardMarkup()
                btn_to_download = types.InlineKeyboardButton(text=name_account, callback_data=callback_data)
                keyboard.add(btn_to_download)
                bot.reply_to(message, text=f'{name_account} has been downloaded {download_count[count]} times', reply_markup=keyboard)


            else:
                not_none_check.append(name_account)

    if len(not_none_check) == len(insta_acs):
        bot.reply_to(message, text=f"make sure that you are save {select_column}")



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
        res = video_downloader(text_url, bestvideo, "youtube")
        sending_file(res, chat_id)

    elif call.data == "audio":
        res = video_downloader(text_url, "bestaudio", "youtube")
        sending_file(res, chat_id)
    elif call.data == "stories":
        insta_acs = "insta_accounts"
        text = call.message.text 
        text_name = text.split(" ")[0]
        print(text_name)
        
        L = instaloader.Instaloader(dirname_pattern=f"instagram/{text_name}")
        profile = stories_download(text_name, L)
        L.download_stories(userids=[profile])
        send_files_to_telegram(chat_id, text_name, "instagram")
        i = insert_account_in_database_if_not_exists(cursor, chat_id, text_name, insta_acs)
        # return insta_text
        # print(i)
    elif call.data == "TT_profile":
        tt_acs = "tt_accounts"
        # print(text_name)
        text = call.message.text 
        text_name = text.split(" ")[0]
        # text_name = text_url
        res = video_downloader(f"https://www.tiktok.com/@{text_name}", best, f"tt_profile/{text_url}")
        send_files_to_telegram(chat_id, text_name, "../django_server/django_ggrksok/media/tt_profile")

        i = insert_account_in_database_if_not_exists(cursor, chat_id, text_name, tt_acs)
    elif call.data == "TT":
        res = video_downloader(text_url, best, "tiktok")
        # video_response(chat_id, res, "media/tiktok")
        bot.send_video(chat_id, open(f"../django_server/django_ggrksok/media/tiktok/{res}", "rb"))

    elif call.data == "highlights":
        L = instaloader.Instaloader(dirname_pattern=f"highlights/{text_url}")
        profile = stories_download(text_url, L)
        L.download_highlights(profile)
        send_files_to_telegram(chat_id, text_url, "highlights")




def video_response(chat_id, text_url, directory):
    folder = f"./{directory}/{text_url}"
    bot.send_video(chat_id, open(f"{folder}", "rb"))

def send_files_to_telegram(chat_id, text_url, directory):
    folder = f"./{directory}/{text_url}"
    print(folder)
    for r, m, d in os.walk(folder):
        for file in sorted(d):
            if ".jpg" in file:
                bot.send_photo(chat_id, open(f"{folder}/{file}", "rb"))
            elif ".mp4" in file:
                bot.send_video(chat_id, open(f"{folder}/{file}", "rb"))



def sending_file(res, chat_id):
    req = f"https://ggrksok.fun/media/youtube/{res}"
    keyboard = types.InlineKeyboardMarkup()
    url_bin = types.InlineKeyboardButton(
        text="Load", url=req, reply_markup=keyboard
    )
    keyboard.add(url_bin)
    bot.send_message(chat_id, text="Load", reply_markup=keyboard)



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

def stories_download(profile: str, L: str):
    L.load_session_from_file("ffvgd2021", "/home/www/.config/instaloader/session-ffvgd2021")
    profile = L.check_profile_id(profile)
    
    return  profile


    


bot.polling()
