import time
import telebot
from threading import Timer
from telebot.types import Poll

bot = telebot.TeleBot("2120627711:AAHVELyz-B9wmFR_gmYBsN1h7rpsis6vfek")

@bot.message_handler(commands=["votemute"])
def votemute(message):
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    poll = bot.send_poll(message.chat.id, "Mute " + user_name, ["+", "-"], is_anonymous=False)
    t = Timer(45.0, checkPoll, [poll, message])
    t.start()


def checkPoll(poll, message):
    user = message.reply_to_message.from_user
    chat_id = poll.chat.id
    poll = bot.stop_poll(chat_id, poll.message_id)
    res = [poll.options[0].voter_count, poll.options[1].voter_count]
    if sum(res) > 0 and res[0] > res[1]:
        mute_time = 300 * (res[0]-res[1])
        bot.restrict_chat_member(chat_id, user.id, until_date = round(time.time()) + mute_time, can_send_messages = False)
        bot.reply_to(message, "Muted for " + str(int(mute_time/60)) + " minutes")
    else:
        bot.reply_to(message, "Not enough votes")
# @bot.message_handler(commands=["votemute"])
# @bot.message_handler(func=lambda message: True)

bot.infinity_polling()