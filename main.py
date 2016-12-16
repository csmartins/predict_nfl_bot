import telepot
import asyncio
import telepot.aio
import random
#from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import (per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)


async def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type != 'text':
        return

    command = msg['text'].lower()
		
    if command == '/predict':
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text='Time de casa', callback_data='casa'),
                    InlineKeyboardButton(text='Empae', callback_data='empate'),
                    InlineKeyboardButton(text='Time visitante', callback_data='visitante'),]])
        await bot.sendMessage(chat_id, 'Week X', reply_markup=keyboard)
		
async def on_callback_query(msg):
	query_id, from_id, query_data = glance(msg, flavor='callback_query')

	print(query_data)

TOKEN = '302874617:AAEG99KVuWLo3SlN9WVxZTR8s496Ftuylg0'
bot = telepot.aio.Bot(TOKEN, [include_callback_query_chat_id(pave_event_space())(per_chat_id(), create_open)])
answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())

print("Listening...")
loop.run_forever()
