import time
import json
import telebot
from threading import Timer
from telebot.types import Poll
from threading import Thread
from flask import Flask, request, send_from_directory
import os, io, typing
from pytube import YouTube

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

# @bot.message_handler(commands=["download"])
@bot.message_handler()
def download_for_me(message):
    if message.chat.id == 690294790:
        yt = YouTube(message.text)
        buffer = io.BytesIO()
        yt.streams.get_audio_only().stream_to_buffer(buffer)
        buffer.seek(0)
        bot.send_document(message.chat.id, buffer, visible_file_name = yt.title + ".mp3")
        del buffer

Thread(target=bot.infinity_polling).start()

app = Flask(__name__,
            static_url_path='', 
            static_folder='web')

app.run(port = int(os.environ.get("PORT", 5000)))