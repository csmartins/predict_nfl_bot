import telepot
import asyncio
import telepot.aio
import telepot.aio.helper
import sys
import json
import os
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
                        InlineKeyboardButton(text=game['AwayTeam'], callback_data=game['GameKey'] + '-' + game['AwayTeam']),]])
                    await self.bot.sendMessage(chat_id, 'Away @ Home', reply_markup=keyboard)
                    return
            await self.bot.sendMessage(chat_id, "You're finished!")

    async def _show_users_predictions(self, chat_id):
        users = os.listdir(str(self.current_week))
        predicts = ''
        for user in users:
            if user != 'week-16.json':
                with open(str(self.current_week) + '/' + user) as user_file:
                    user_prediction = json.load(user_file)
                    user_predict = ''
                    for game in user_prediction:
#                        print(user_predict)
                        user_predict = user_predict + game['AwayTeam'] + ' @ ' + game['HomeTeam'] + ': ' + (game['predict'] if game['predicted'] else 'UNKNOWN ') + '\n'

                    username = user.split('.')                
                    predicts = predicts + '@' + username[0] + ' predicts \n' + user_predict + '\n'
        await self.bot.sendMessage(chat_id, 'WEEK ' + str(self.current_week) + ' PREDICTIONS\n' + predicts)

    async def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)

        if content_type != 'text':
            return

        command = msg['text'].lower()
        if command == '/predict':
            await self.bot.sendMessage(chat_id, 'WEEK ' + str(self.current_week))
            await self._show_unpredicted_match(chat_id, msg['from']['username'])
        if command == '/show':
            await self._show_users_predictions(chat_id)                

    async def on_callback_query(self, msg):
        query_id, from_id, query_data = glance(msg, flavor='callback_query')
        username = msg['from']['username']
        games = []

        with open(str(self.current_week) + '/' + username + '.json', 'r') as data:
            games = json.load(data)

        if query_data != '':
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
            per_chat_id(types=['private', 'group']), create_open, NFLPredict, timeout=300)])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())

print("Listening...")
loop.run_forever()

# if __name__ == "__main__":
#     do_main()
