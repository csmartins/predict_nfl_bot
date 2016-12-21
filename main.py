import telepot
import asyncio
import telepot.aio
import telepot.aio.helper
import sys
import json
from telepot import glance, message_identifier
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.aio.delegate import (per_chat_id, create_open, pave_event_space, include_callback_query_chat_id)

class NFLPredict(telepot.aio.helper.ChatHandler):

    def __init__(self, *args, **kwargs):
        super(NFLPredict, self).__init__(*args, **kwargs)
        self.current_season = '2016'
        self.current_week = 16

    async def _show_unpredicted_match(self, chat_id, username):
        with open(str(self.current_week) + '/' + username + '.json') as data:
            week = json.load(data)
            for game in week:
                if not game['predicted']:
                    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
                        InlineKeyboardButton(text=game['HomeTeam'], callback_data=game['GameKey'] + '-' + game['HomeTeam']),
                        InlineKeyboardButton(text='Empate', callback_data=game['GameKey'] + '-tie'),
                        InlineKeyboardButton(text=game['AwayTeam'], callback_data=game['GameKey'] + '-' + game['AwayTeam']),]])
                    await self.bot.sendMessage(chat_id, 'Week ' + str(self.current_week), reply_markup=keyboard)
                    return

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        command = msg['text'].lower()
        if command == '/predict':
            await self._show_unpredicted_match(chat_id, msg['from']['username'])

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = glance(msg, flavor='callback_query')
        username = msg['from']['username']
        games = []

        with open(str(self.current_week) + '/' + username + '.json', 'r') as data:
            games = json.load(data)

        query_data = query_data.split('-')
        for game in games:
            if game['GameKey'] == query_data[0]:
                game['predicted'] = True
                game['predict'] = query_data[1]

        with open(str(self.current_week) + '/' + username + '.json', 'w') as data:
            json.dump(games, data)

        await self._show_unpredicted_match(from_id, username)
#
# def do_main():
# 	if len(sys.argv) < 2:
# 		print("Insuficient number of arguments.")
# 		print("Expected: python main.py <TOKEN>")
# 		return

TOKEN = sys.argv[1]
bot = telepot.aio.DelegatorBot(TOKEN, [
    include_callback_query_chat_id(
        pave_event_space())(
            per_chat_id(types=['private']), create_open, NFLPredict, timeout=60)])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())

print("Listening...")
loop.run_forever()

# if __name__ == "__main__":
#     do_main()
