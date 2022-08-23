import time
import json
from aiogram import Bot, Dispatcher, executor, types
from threading import Timer
from threading import Thread
import os, io, typing
import asyncio
import logging
from app import app
from pytube import YouTube, Search

API_TOKEN = '2120627711:AAHVELyz-B9wmFR_gmYBsN1h7rpsis6vfek'

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["votemute"])
async def votemute(message):
    user_id = message.reply_to_message.from_user.id
    user_name = message.reply_to_message.from_user.first_name
    poll = await bot.send_poll(message.chat.id, "Mute " + user_name, ["+", "-"], is_anonymous=False)
    await asyncio.sleep(15)
    await mutePoll(poll, message)


async def mutePoll(poll, message):
    user = message.reply_to_message.from_user
    chat_id = poll.chat.id
    poll = await bot.stop_poll(chat_id, poll.message_id)
    res = [poll.options[0].voter_count, poll.options[1].voter_count]
    if sum(res) > 0 and res[0] > res[1]:
        mute_time = 300 * (res[0]-res[1])
        await bot.restrict_chat_member(chat_id, user.id, until_date = round(time.time()) + mute_time, can_send_messages = False)
        await bot.send_message(chat_id, "Muted for " + str(int(mute_time/60)) + " minutes", reply_to_message_id=message.message_id)
    else:
        await bot.send_message(chat_id, "Not enough votes", reply_to_message_id=message.message_id)

@dp.message_handler()
async def download_for_me(message):
    if message.chat.type == "private":
        try:
            yt = YouTube(message.text)
        except:
            yt = Search(message.text).results[0]
        buffer = io.BytesIO()
        yt.streams.get_audio_only().stream_to_buffer(buffer)
        buffer.seek(0)
        await bot.send_document(message.chat.id, (yt.title + ".mp3", buffer))
        del buffer

executor.start_polling(dp, skip_updates=True)

app.run(port = int(os.environ.get("PORT", 5000)))