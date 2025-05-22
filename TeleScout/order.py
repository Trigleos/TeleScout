import os, json

def dump_file(path, files, start_index, file_index):
	chats = []
	with open(os.path.join(path, files[start_index]), "r") as f:
		initial_messages = json.load(f)[file_index:]
	start_index += 1
	chats.extend(initial_messages)
	
	if start_index >= len(files):
		return True, start_index, file_index, chats
		
	while(len(chats) < 200):
		if start_index < len(files):
			with open(os.path.join(path, files[start_index]), "r") as f:
				messages = json.load(f)
			if(len(chats) + len(messages) < 200):
				chats.extend(messages)
				start_index += 1
			else:
				file_index = 200 - len(chats)
				chats.extend(messages[:file_index])
		else:
			return True, start_index, file_index, chats
	return False, start_index, file_index, chats
			
def int_filename(elem):
	return int(elem.split(".")[0])


def order(bot_token):
	user_chats_dir = os.path.join(bot_token, "user_chats")
	chats_dir = os.path.join(bot_token, "chats")
	user_chats = os.listdir(user_chats_dir)
	chats = os.listdir(chats_dir)
	channels_dir = os.path.join(bot_token, "channels")
	channels = os.listdir(channels_dir)
	
	for chat in user_chats:
		chat_base_path = os.path.join(user_chats_dir, chat)
		chat_path = os.path.join(chat_base_path, "raw")
		files = os.listdir(chat_path)
		files.sort(key=int_filename)
		dump_path = os.path.join(chat_base_path, "html")
		if not os.path.exists(dump_path):
			os.mkdir(dump_path)
		dump_index = 0
		result = dump_file(chat_path, files, 0, 0)
		while(not result[0]):
			filename = os.path.join(dump_path, str(dump_index) + ".json")
			with open(filename, "w") as f:
				json.dump(result[3], f)
			dump_index += 1
			result = dump_file(chat_path, files, result[1], result[2])
			
		filename = os.path.join(dump_path, str(dump_index) + ".json")
		with open(filename, "w") as f:
			json.dump(result[3], f)
		
	for chat in chats:
		chat_base_path = os.path.join(chats_dir, chat)
		chat_path = os.path.join(chat_base_path, "raw")
		files = os.listdir(chat_path)
		files.sort(key=int_filename)
		dump_path = os.path.join(chat_base_path, "html")
		if not os.path.exists(dump_path):
			os.mkdir(dump_path)
		dump_index = 0
		result = dump_file(chat_path, files, 0, 0)
		while(not result[0]):
			filename = os.path.join(dump_path, str(dump_index) + ".json")
			with open(filename, "w") as f:
				json.dump(result[3], f)
			dump_index += 1
			result = dump_file(chat_path, files, result[1], result[2])
			
		filename = os.path.join(dump_path, str(dump_index) + ".json")
		with open(filename, "w") as f:
			json.dump(result[3], f)
			
	for channel in channels:
		channel_base_path = os.path.join(channels_dir, channel)
		channel_path = os.path.join(channel_base_path, "raw")
		files = os.listdir(channel_path)
		files.sort(key=int_filename)
		dump_path = os.path.join(channel_base_path, "html")
		if not os.path.exists(dump_path):
			os.mkdir(dump_path)
		dump_index = 0
		result = dump_file(channel_path, files, 0, 0)
		while(not result[0]):
			filename = os.path.join(dump_path, str(dump_index) + ".json")
			with open(filename, "w") as f:
				json.dump(result[3], f)
			dump_index += 1
			result = dump_file(channel_path, files, result[1], result[2])
			
		filename = os.path.join(dump_path, str(dump_index) + ".json")
		with open(filename, "w") as f:
			json.dump(result[3], f)
			
			
