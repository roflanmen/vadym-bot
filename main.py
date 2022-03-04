import time
import json
import telebot
from threading import Timer
from telebot.types import Poll
from threading import Thread
from flask import Flask, request, send_from_directory
import os

bot = telebot.TeleBot("2120627711:AAHVELyz-B9wmFR_gmYBsN1h7rpsis6vfek")

@bot.message_handler(commands=["votemute"])
def votemute(message):
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    poll = bot.send_poll(message.chat.id, "Mute " + user_name, ["+", "-"], is_anonymous=False)
    t = Timer(45.0, mutePoll, [poll, message])
    t.start()


def mutePoll(poll, message):
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
    
@bot.message_handler(commands=["unmute"])
def unmute(message):
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    poll = bot.send_poll(message.chat.id, "Unmute " + user_name, ["+", "-"], is_anonymous=False)
    t = Timer(45.0, unmutePoll, [poll, message])
    t.start()

def unmutePoll(poll, message):
    user = message.reply_to_message.from_user
    chat_id = poll.chat.id
    poll = bot.stop_poll(chat_id, poll.message_id)
    res = [poll.options[0].voter_count, poll.options[1].voter_count]
    if sum(res) > 0 and res[0] > res[1]:
        f = open('data.json')
        data = json.load(f)
        f.close()
        try:
            del data[str(user.id)]
        except:
            pass
        f = open('data.json', 'w')
        json.dump(data, f)
        f.close()
        try:
            bot.restrict_chat_member(chat_id, user.id, can_send_messages = True, can_send_media_messages = True, can_send_polls = True, can_send_other_messages = True, can_add_web_page_previews = True)
        except:
            pass
        bot.reply_to(message, "Unmuted")
    else:
        bot.reply_to(message, "Not enough votes")

@bot.message_handler(commands=["add_target"])
def addTarget(message):
    if message.from_user.id == 690294790:
        f = open(os.path.join(os.path.dirname(__file__), 'web') + '/targets.txt')
        data = json.load(f)
        f.close()
        data.append(message.text.split()[-1])
        bot.reply_to(message, "\n".join(data))
        f = open(os.path.join(os.path.dirname(__file__), 'web') + '/targets.txt', 'w')
        json.dump(data, f)
        f.close()

@bot.message_handler(commands=["clear"])
def clear(message):
    if message.from_user.id == 690294790:
        f = open(os.path.join(os.path.dirname(__file__), 'web') + '/targets.txt', 'w')
        json.dump([], f)
        f.close()
        bot.reply_to(message, "Cleared")

Thread(target=bot.infinity_polling).start()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web')

app.run(port = int(os.environ.get("PORT", 5000)))