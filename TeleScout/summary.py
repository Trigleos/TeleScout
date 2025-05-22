from telethon.sync import TelegramClient
from telethon import functions, types
from telethon.tl.types import ChatForbidden

import json, os

async def get_user(user_id, bot):
	return await bot(functions.users.GetFullUserRequest(id=user_id))

async def get_chat(chat_id, bot):
	return await bot(functions.messages.GetFullChatRequest(chat_id=chat_id))
	
async def get_channel(channel_id, bot):
	return await bot(functions.channels.GetFullChannelRequest(channel=channel_id))

def create_user_chat_summary(user_chat, path):
	user_chat_summary = {}
	user = user_chat.users[0]
	user_chat_summary["id"] = user.id
	user_chat_summary["first_name"] = user.first_name
	user_chat_summary["last_name"] = user.last_name
	user_chat_summary["username"] = user.username
	path = os.path.join(path, str(user.id))
	path = os.path.join(path, "summary.json")
	if not os.path.exists(path):
		with open(path, "w") as f:
			json.dump(user_chat_summary, f)
		
	

def create_chat_summary(chat, path):
	chat_summary = {}
	users = chat.users
	chat_summary["about"] = chat.full_chat.about
	chat = chat.chats[0]
	chat_summary["id"] = chat.id
	chat_summary["title"] = chat.title
	if not isinstance(chat, ChatForbidden):
		chat_summary["date"] = chat.date.strftime("%d/%m/%Y %H:%M:%S")
	else:
		chat_summary["date"] = None
	chat_summary["users"] = {}
	for user in users:
		chat_summary["users"][user.id] = {}
		chat_summary["users"][user.id]["username"] = user.username
		chat_summary["users"][user.id]["first_name"] = user.first_name
		chat_summary["users"][user.id]["last_name"] = user.last_name
	path = os.path.join(path, str(chat.id))
	path = os.path.join(path, "summary.json")
	if not os.path.exists(path):
		with open(path, "w") as f:
			json.dump(chat_summary, f)
			
def create_channel_summary(channel, path):
	channel_summary = {}
	users = channel.users
	channel_summary["about"] = channel.full_chat.about
	channel = channel.chats[0]
	channel_summary["id"] = channel.id
	channel_summary["title"] = channel.title
	if not isinstance(channel, ChatForbidden):
		channel_summary["date"] = channel.date.strftime("%d/%m/%Y %H:%M:%S")
	else:
		channel_summary["date"] = None
	channel_summary["users"] = {}
	for user in users:
		channel_summary["users"][user.id] = {}
		channel_summary["users"][user.id]["username"] = user.username
		channel_summary["users"][user.id]["first_name"] = user.first_name
		channel_summary["users"][user.id]["last_name"] = user.last_name
	path = os.path.join(path, str(channel.id))
	path = os.path.join(path, "summary.json")
	if not os.path.exists(path):
		with open(path, "w") as f:
			json.dump(channel_summary, f)
	
	

async def create_summary(bot, bot_token):
	high_level_summary = {}
	user_chats_dir = os.path.join(bot_token, "user_chats")
	chats_dir = os.path.join(bot_token, "chats")
	channels_dir = os.path.join(bot_token, "channels")
	user_chats = os.listdir(user_chats_dir)
	chats = os.listdir(chats_dir)
	channels = os.listdir(channels_dir)
	
	me = await bot.get_me()
	high_level_summary["id"] = me.id
	high_level_summary["username"] = me.username
	high_level_summary["first_name"] = me.first_name
	high_level_summary["last_name"] = me.last_name
	high_level_summary["user_chats"] = {}
	high_level_summary["chats"] = {}
	high_level_summary["channels"] = {}
	
	for user_chat in user_chats:
		full_user = await get_user(int(user_chat), bot)
		high_level_summary["user_chats"][user_chat] = full_user.users[0].username
		create_user_chat_summary(full_user, user_chats_dir)
	
	for chat in chats:
		full_chat = await get_chat(int(chat), bot)
		high_level_summary["chats"][chat] = full_chat.chats[0].title
		create_chat_summary(full_chat, chats_dir)
		
	for channel in channels:
		full_channel = await get_channel(int(channel), bot)
		high_level_summary["channels"][channel] = full_channel.chats[0].title
		create_channel_summary(full_channel, channels_dir)
		

	path = os.path.join(bot_token, "summary.json")
	with open(path, "w") as f:
		json.dump(high_level_summary, f)
		


def summary(api_id, api_hash, bot_token):
	bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
	
	with bot:
		bot.loop.run_until_complete(create_summary(bot, bot_token))
		


