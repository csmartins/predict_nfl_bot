import telepot
import asyncio
import telepot.aio

async def on_chat_message(msg):
	content_type, chat_type, chat_id = telepot.glance(msg)
	print('Chat:', content_type, chat_type, chat_id)

	if command == '/roll':
		bot.sendMessage(chat_id, random.randint(1,6))

bot = telepot.aio.Bot('302874617:AAEG99KVuWLo3SlN9WVxZTR8s496Ftuylg0')
answerer = telepot.aio.helper.Answerer(bot)

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop({'chat': on_chat_message}))

print("Listening...")
loop.run_forever()
