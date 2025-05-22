from telethon.sync import TelegramClient
from telethon import functions, types

import json, os, time
	
def extract_message_fields_user(message):
	message_store = {}
	message_store["id"] = message.id
	message_store["date"] = message.date.strftime("%d/%m/%Y %H:%M:%S")
	message_store["message"] = message.message
	
	if message.media != None and not isinstance(message.media, types.MessageMediaWebPage):
		message_store["media"] = extract_media_fields(message.media)
	else:
		message_store["media"] = None
			
	if message.from_id != None:
		message_store["bot_message"] = 1
	else:
		message_store["bot_message"] = 0
		
	if message.fwd_from != None:
		if message.fwd_from.from_id != None:
			if isinstance(message.fwd_from.from_id, types.PeerUser):
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.user_id}
			else:
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.channel_id}
		else:
			message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":None}
	else:
		message_store["fwd"] = None
			
	if message.reply_to != None:
		message_store["reply_to_message_id"] = message.reply_to.reply_to_msg_id
	else:
		message_store["reply_to_message_id"] = None
		
	return message_store
	
def extract_message_fields_chat(message):
	message_store = {}
	message_store["id"] = message.id
	message_store["date"] = message.date.strftime("%d/%m/%Y %H:%M:%S")
	message_store["message"] = message.message
	message_store["from_id"] = message.from_id.user_id
	
	if message.media != None and not isinstance(message.media, types.MessageMediaWebPage):
		message_store["media"] = extract_media_fields(message.media)
	else:
		message_store["media"] = None
		
	if message.fwd_from != None:
		if message.fwd_from.from_id != None:
			if isinstance(message.fwd_from.from_id, types.PeerUser):
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.user_id}
			else:
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.channel_id}
		else:
			message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":None}
	else:
		message_store["fwd"] = None
		
	if message.reply_to != None:
		message_store["reply_to_message_id"] = message.reply_to.reply_to_msg_id
	else:
		message_store["reply_to_message_id"] = None
		
	return message_store
	
def extract_message_fields_channel(message):
	message_store = {}
	message_store["id"] = message.id
	message_store["date"] = message.date.strftime("%d/%m/%Y %H:%M:%S")
	message_store["message"] = message.message
	message_store["from_id"] = message.peer_id.channel_id
	if message.media != None and not isinstance(message.media, types.MessageMediaWebPage):
		message_store["media"] = extract_media_fields(message.media)
	else:
		message_store["media"] = None
	if message.fwd_from != None:
		if message.fwd_from.from_id != None:
			if isinstance(message.fwd_from.from_id, types.PeerUser):
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.user_id}
			else:
				message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":message.fwd_from.from_id.channel_id}
		else:
			message_store["fwd"] = {"date":message.fwd_from.date.strftime("%d/%m/%Y %H:%M:%S"), "from_id":None}
	else:
		message_store["fwd"] = None
	
	if message.reply_to != None:
		message_store["reply_to_message_id"] = message.reply_to.reply_to_msg_id
	else:
		message_store["reply_to_message_id"] = None
		
	return message_store
	
def extract_media_fields(media):
	media_store = {}
	
	if isinstance(media, types.MessageMediaDocument):
		media_store["type"] = media.document.mime_type
		media_store["size"] = media.document.size
	else:
		media_store["type"] = "picture"
	return media_store
	
def dump_messages(user_chats, chats, channels, dump_dir, index):
	if not os.path.exists(dump_dir):
		os.mkdir(dump_dir)
	user_chats_dir = os.path.join(dump_dir, "user_chats")
	chats_dir = os.path.join(dump_dir, "chats")
	channels_dir = os.path.join(dump_dir, "channels")
	
	if not os.path.exists(user_chats_dir):
		os.mkdir(user_chats_dir)
	if not os.path.exists(chats_dir):
		os.mkdir(chats_dir)
	if not os.path.exists(channels_dir):
		os.mkdir(channels_dir)
	
	for chat in list(user_chats.keys()):
		user_chat_dir = os.path.join(user_chats_dir, str(chat))
		if not os.path.exists(user_chat_dir):
			os.mkdir(user_chat_dir)
		user_chat_dir = os.path.join(user_chat_dir, "raw")
		if not os.path.exists(user_chat_dir):
			os.mkdir(user_chat_dir)
		chat_file = os.path.join(user_chat_dir, str(index) + ".json")
		with open(chat_file, "w") as f:
			json.dump(user_chats[chat], f)
			
	for chat in list(chats.keys()):
		chat_dir = os.path.join(chats_dir, str(chat))
		if not os.path.exists(chat_dir):
			os.mkdir(chat_dir)
		chat_dir = os.path.join(chat_dir, "raw")
		if not os.path.exists(chat_dir):
			os.mkdir(chat_dir)
		chat_file = os.path.join(chat_dir, str(index) + ".json")
		with open(chat_file, "w") as f:
			json.dump(chats[chat], f)
	
	for channel in list(channels.keys()):
		channel_dir = os.path.join(channels_dir, str(channel))
		if not os.path.exists(channel_dir):
			os.mkdir(channel_dir)
		channel_dir = os.path.join(channel_dir, "raw")
		if not os.path.exists(channel_dir):
			os.mkdir(channel_dir)
		channel_file = os.path.join(channel_dir, str(index) + ".json")
		with open(channel_file, "w") as f:
			json.dump(channels[channel], f)


async def one_run(index, bot, bot_token, channel_id):
	ids = [i for i in range(200*index,200*(index+1))]
	user_chats = {}
	chats = {}
	channels = {}
	if channel_id != None:
		channel = await bot(functions.channels.GetFullChannelRequest(channel=channel_id))
		result = await bot(functions.channels.GetMessagesRequest(channel=channel_id, id=ids))
	else:
		result = await bot(functions.messages.GetMessagesRequest(id=ids))
	for message in result.messages:
		if message.media == None and message.message == None:
			continue
			
		peer_id = message.peer_id
		if isinstance(peer_id, types.PeerUser):
			user_id = peer_id.user_id
		
			if (user_id not in user_chats):
				user_chats[user_id] = []
				
			user_chats[user_id].append(extract_message_fields_user(message))
		elif isinstance(peer_id, types.PeerChat):
			chat_id = peer_id.chat_id
			
			if (chat_id not in chats):
				chats[chat_id] = []
				
			chats[chat_id].append(extract_message_fields_chat(message))
		elif isinstance(peer_id, types.PeerChannel):
			channel_id = peer_id.channel_id
			
			if (channel_id not in channels):
				channels[channel_id] = []
				
			channels[channel_id].append(extract_message_fields_channel(message))
		else:
			print("Error:", message.id)
			
	dump_messages(user_chats, chats, channels, bot_token, index)


async def extract_all_messages(bot, start_index, last_index, bot_token, chat_id):
	start_set = start_index // 200
	end_set = last_index // 200 + 1
	for i in range(start_set, end_set):
		await one_run(i, bot, bot_token, chat_id)
		percentage = round(((100 * ((i+1) * 200 - start_index))/(last_index-start_index)), 2)
		print("Extraction reached " + str(percentage) + "%")
		time.sleep(10)


def exfil(api_id, api_hash, bot_token, start_index, end_index, chat_id=None):
	bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
	
	with bot:
		bot.loop.run_until_complete(extract_all_messages(bot, start_index, end_index, bot_token, chat_id))
		

