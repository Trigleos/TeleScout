import os, json, shutil
from telethon.sync import TelegramClient
from telethon import functions, types
import file_extraction

async def get_user(user_id, bot):
	return await bot(functions.users.GetFullUserRequest(id=user_id))


def prepare(bot_token):
	assets_dir = os.path.join(bot_token, "assets")
	

	if not os.path.exists(assets_dir):
		os.mkdir(assets_dir)

	style_file = "templates/style.css"
	script_file = "templates/script.js"

	shutil.copy(style_file, assets_dir)
	shutil.copy(script_file, assets_dir)

	user_chats_dir = os.path.join(bot_token, "user_chats")
	chats_dir = os.path.join(bot_token, "chats")
	channels_dir = os.path.join(bot_token, "channels")
	return chats_dir, user_chats_dir, channels_dir



def prepare_base_template(index, chat_summary, length, is_user):
	with open("templates/chat.html") as f:
		base_template = f.read()
	if not is_user:
		base_template = base_template.replace("#TITLE", chat_summary["title"])
	else:
		if chat_summary["username"] != None:
			base_template = base_template.replace("#TITLE", chat_summary["username"])
		elif chat_summary["first_name"] != None:
			base_template = base_template.replace("#TITLE", chat_summary["first_name"])
		else:
			base_template = base_template.replace("#TITLE", str(chat_summary["id"]))
			
		
	if index == 0 and length == 1:
		base_template = base_template.replace("#START", "").replace("#END", "")
			
	elif index == 0:
		with open("templates/next_button.html") as f:
			next_button = f.read()
		next_file = "./" + str(index + 1) + ".html"
		next_button = next_button.replace("#NEXT", next_file)
		base_template = base_template.replace("#END", next_button)
		base_template = base_template.replace("#START", "")
			
	elif index == length - 1:
		with open("templates/previous_button.html") as f:
			previous_button = f.read()
		previous_file = "./" + str(index - 1) + ".html"
		previous_button = previous_button.replace("#PREVIOUS", previous_file)
		base_template = base_template.replace("#START", previous_button)
		base_template = base_template.replace("#END", "")
		
	else:
		with open("templates/next_button.html") as f:
			next_button = f.read()
		next_file = "./" + str(index + 1) + ".html"
		next_button = next_button.replace("#NEXT", next_file)
		base_template = base_template.replace("#END", next_button)
			
		with open("templates/previous_button.html") as f:
			previous_button = f.read()
		previous_file = "./" + str(index - 1) + ".html"
		previous_button = previous_button.replace("#PREVIOUS", previous_file)
		base_template = base_template.replace("#START", previous_button)
		
	return base_template

async def prepare_picture(bot, message, message_template, chat_files_path, is_channel):
	chat_pictures_path = os.path.join(chat_files_path, "pictures")
	if not os.path.exists(chat_pictures_path):
		os.mkdir(chat_pictures_path)
	pic_name = str(message["id"]) + ".jpg"
	pic_location = os.path.join(chat_pictures_path, pic_name)
	if is_channel:
		await file_extraction.download_pic(message["id"], bot, pic_location, is_channel, message["from_id"])
	else:
		await file_extraction.download_pic(message["id"], bot, pic_location)
	with open("templates/divs/pic_div.html", "r") as f:
		image_template = f.read()
	pictures_folder = "../files/pictures"
	pic_location = os.path.join(pictures_folder, pic_name)
	image_template = image_template.replace("#SRC", pic_location)
	message_template = message_template.replace("#MEDIA", image_template)
	return message_template
	
async def prepare_audio(bot, message, message_template, chat_files_path, is_channel):
	chat_audio_path = os.path.join(chat_files_path, "audio")
	if not os.path.exists(chat_audio_path):
		os.mkdir(chat_audio_path)
	if message["media"]["type"] == "audio/ogg":
		audio_name = str(message["id"]) + ".ogg"
	elif message["media"]["type"] == "audio/wav":
		audio_name = str(message["id"]) + ".wav"
	audio_location = os.path.join(chat_audio_path, audio_name)
	if is_channel:
		await file_extraction.download_doc(message["id"], bot, audio_location, is_channel, message["from_id"])
	else:
		await file_extraction.download_doc(message["id"], bot, audio_location)
	with open("templates/divs/audio_div.html", "r") as f:
		audio_template = f.read()
	audio_folder = "../files/audio"
	audio_location = os.path.join(audio_folder, audio_name)
	audio_template = audio_template.replace("#SRC", audio_location)
	message_template = message_template.replace("#MEDIA", audio_template)
	
	return message_template

async def prepare_video(bot, message, message_template, chat_files_path, is_channel):
	chat_video_path = os.path.join(chat_files_path, "video")
	if not os.path.exists(chat_video_path):
		os.mkdir(chat_video_path)
	if message["media"]["type"] == "video/mp4":
		video_name = str(message["id"]) + ".mp4"
	elif message["media"]["type"] == "video/x-msvideo":
		video_name = str(message["id"]) + ".avi"
	video_location = os.path.join(chat_video_path, video_name)
	if is_channel:
		await file_extraction.download_doc(message["id"], bot, video_location, is_channel, message["from_id"])
	else:
		await file_extraction.download_doc(message["id"], bot, video_location)
	
	with open("templates/divs/video_div.html", "r") as f:
		video_template = f.read()
	video_folder = "../files/video"
	video_location = os.path.join(video_folder, video_name)
	video_template = video_template.replace("#SRC", video_location)
	message_template = message_template.replace("#MEDIA", video_template)
	
	return message_template
	
async def prepare_image(bot, message, message_template, chat_files_path, is_channel):
	chat_image_path = os.path.join(chat_files_path, "images")
	if not os.path.exists(chat_image_path):
		os.mkdir(chat_image_path)
	if message["media"]["type"] == "image/webp":
		image_name = str(message["id"]) + ".webp"
	elif message["media"]["type"] == "image/jpeg":
		image_name = str(message["id"]) + ".jpg"
	image_location = os.path.join(chat_image_path, image_name)
	if is_channel:
		await file_extraction.download_doc(message["id"], bot, image_location, is_channel, message["from_id"])
	else:
		await file_extraction.download_doc(message["id"], bot, image_location)
	
	with open("templates/divs/pic_div.html", "r") as f:
		image_template = f.read()
	image_folder = "../files/images"
	image_location = os.path.join(image_folder, image_name)
	image_template = image_template.replace("#SRC", image_location)
	message_template = message_template.replace("#MEDIA", image_template)
	return message_template

async def prepare_media(bot, message, message_template, chat_base_path, is_channel):
	chat_files_path = os.path.join(chat_base_path, "files")
	if not os.path.exists(chat_files_path):
		os.mkdir(chat_files_path)
	
	if message["media"]["type"] == "picture":
		message_template = await prepare_picture(bot, message, message_template, chat_files_path, is_channel)
	elif message["media"]["type"] == "audio/ogg" or message["media"]["type"] == "audio/wav":
		message_template = await prepare_audio(bot, message, message_template, chat_files_path, is_channel)
	elif message["media"]["type"] == "video/mp4" or message["media"]["type"] == "video/x-msvideo":
		message_template = await prepare_video(bot, message, message_template, chat_files_path, is_channel)
	elif message["media"]["type"] == "application/x-tgsticker":
		#message_template = await prepare_animated_sticker(bot, message, message_template, chat_files_path)
		message_template = message_template.replace("#MEDIA", "Animated Sticker")
	elif message["media"]["type"] == "image/webp" or message["media"]["type"] == "image/jpeg":
		message_template = await prepare_image(bot, message, message_template, chat_files_path, is_channel)
	else:
		message_template = message_template.replace("#MEDIA", (message["media"]["type"] + ":" + str(message["id"])))
	return message_template

	
async def prepare_message(bot, message, summary, is_user, is_channel, chat_base_path):
	if is_user and not message["bot_message"]:
		with open("templates/messages/curr_message.html", "r") as f:
			message_template = f.read()
	else:
		with open("templates/messages/for_message.html", "r") as f:
			message_template = f.read()
	message_template = message_template.replace("#TIME", message["date"])
	
	if is_user or is_channel:
		message_template = message_template.replace("#SENDER", "")
	
	else:
		sender_id = message["from_id"]
		if str(sender_id) not in summary["users"].keys():
			try:
				full_user = await get_user(sender_id, bot)
				user = full_user.users[0]
				print("Found User", user.id)
				summary["users"][str(user.id)] = {}
				summary["users"][str(user.id)]["username"] = user.username
				summary["users"][str(user.id)]["first_name"] = user.first_name
				summary["users"][str(user.id)]["last_name"] = user.last_name
			except ValueError:
				pass
		
		if str(sender_id) in summary["users"].keys():
			user = summary["users"][str(sender_id)]
			if user["username"] != None:
				message_template = message_template.replace("#SENDER", user["username"])
			elif user["first_name"] != None:
				message_template = message_template.replace("#SENDER", user["first_name"])
			elif user["last_name"] != None:
				message_template = message_template.replace("#SENDER", user["last_name"])
			else:
				message_template = message_template.replace("#SENDER", str(sender_id))
		else:
			message_template = message_template.replace("#SENDER", str(sender_id))
		
	if message["media"] == None:
		message_text = message["message"].replace("\n", "<br>")
		message_template = message_template.replace("#TEXT", message_text)
		message_template = message_template.replace("#MEDIA", "")
	else:
		message_text = message["message"].replace("\n", "<br>")
		message_template = message_template.replace("#TEXT", message_text)
		message_template = await prepare_media(bot, message, message_template, chat_base_path, is_channel)
	
	return message_template



async def populate_template(bot, base_template, input_filename, summary, is_user, is_channel, chat_base_path):
	with open(input_filename, "r") as f:
		messages = json.load(f)
	for i in range(len(messages)):
		message_html = await prepare_message(bot, messages[i], summary, is_user, is_channel, chat_base_path)
		
		if i != len(messages) - 1:
			message_html += "\n#MESSAGE"
		base_template = base_template.replace("#MESSAGE", message_html)
	return base_template
		

async def transform_chat(bot, chat_base_path, is_user, is_channel):
	chat_html_path = os.path.join(chat_base_path, "html")
	with open(os.path.join(chat_base_path, "summary.json"), "r") as f:
		chat_summary = json.load(f)	
	
	files = os.listdir(chat_html_path)
	files = [file for file in files if file.endswith(".json")]
	for i in range(len(files)):
		base_template = prepare_base_template(i, chat_summary, len(files), is_user)
		input_filename = str(i) + ".json"
		input_filename = os.path.join(chat_html_path, input_filename)
		final_html = await populate_template(bot, base_template, input_filename, chat_summary, is_user, is_channel, chat_base_path)
		output_filename = str(i) + ".html"
		output_filename = os.path.join(chat_html_path, output_filename)
		with open(output_filename, "w") as f:
			f.write(final_html)
		os.remove(input_filename)
	with open(os.path.join(chat_base_path, "summary.json"), "w") as f:
		json.dump(chat_summary, f)


async def transform_chats(bot_token, bot):
	
	chats_dir, user_chats_dir, channels_dir = prepare(bot_token)
	user_chats = os.listdir(user_chats_dir)
	chats = os.listdir(chats_dir)
	channels = os.listdir(channels_dir)
	
	
	for chat in chats:
		chat_base_path = os.path.join(chats_dir, chat)
		await transform_chat(bot, chat_base_path, False, False)
		
	for channel in channels:
		channel_base_path = os.path.join(channels_dir, channel)
		await transform_chat(bot, channel_base_path, False, True)
	
	for user_chat in user_chats:
		chat_base_path  = os.path.join(user_chats_dir, user_chat)
		await transform_chat(bot, chat_base_path, True, False)
	
		
		
def transform(api_id, api_hash, bot_token):		
	bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
	with bot:
		bot.loop.run_until_complete(transform_chats(bot_token, bot))
	
		
	



