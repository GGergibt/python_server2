import telebot
from telebot import types

bot = telebot.TeleBot("1960290392:AAGWTVdvgqrmRxGbZITJ2RkBD5dpIvL4nO8", parse_mode=None)


CLICKED_BY = []

# Handler for command: '/btn_test'
@bot.message_handler(commands=["btn_test"])
def command_1(msg):
    cid = msg.chat.id
    mid = msg.message_id
    uid = msg.from_user.id

    if msg.chat.type != "private":
        click_kb = types.InlineKeyboardMarkup()
        click_button = types.InlineKeyboardButton("CLICK HERE", callback_data="clicked")
        click_kb.row(click_button)
        bot.send_message(
            cid,
            "<b>Hey friend...</b>",
            parse_mode="HTML",
            reply_markup=click_kb,
            disable_web_page_preview=True,
        )
    else:
        bot.send_message(cid, "Use me in groups, please.", reply_to_message_id=mid)


@bot.callback_query_handler(func=lambda call: call.data == "clicked")
def command_click_inline(call):
    cid = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id

    if uid not in CLICKED_BY:
        CLICKED_BY.append(uid)
        click_kb_edited = types.InlineKeyboardMarkup()
        click_edited = types.InlineKeyboardButton(
            "CLICK HERE ({} clicks)".format(len(CLICKED_BY)), callback_data="clicked"
        )
        click_kb_edited.row(click_edited)
        bot.edit_message_text(
            "<b>Hey friend...</b>",
            cid,
            mid,
            reply_markup=click_kb_edited,
            parse_mode="HTML",
        )
        bot.answer_callback_query(
            call.id, text="Thanks for click me {}.".format(call.from_user.first_name)
        )
    else:
        bot.answer_callback_query(call.id, text="You already clicked this button!")
