import file_extraction, sys
from telethon.sync import TelegramClient

api_id = #API ID
api_hash = #API Hash

bot_token = #bot token
message_id = #message ID
output_filename = #output filename

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
with bot:
	bot.loop.run_until_complete(file_extraction.download_doc(message_id, bot, output_filename, False))
