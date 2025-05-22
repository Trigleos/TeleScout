from telethon.sync import TelegramClient
from telethon import functions, types

async def download_pic(message_id, bot, location, is_channel=False, channel_id=0):
	if is_channel:
		channel_id = -1000000000000 - channel_id
		message = await bot(functions.channels.GetMessagesRequest(channel=channel_id, id=[message_id]))
	else:
		message = await bot(functions.messages.GetMessagesRequest(id=[message_id]))
	await bot.download_media(message.messages[0].media, location)
	
async def download_doc(message_id, bot, location, is_channel=False, channel_id=0):
	if is_channel:
		channel_id = -1000000000000 - channel_id
		message = await bot(functions.channels.GetMessagesRequest(channel=channel_id, id=[message_id]))
	else:
		message = await bot(functions.messages.GetMessagesRequest(id=[message_id]))
	media = message.messages[0].media.document
	input_document_file = types.InputDocumentFileLocation(id=media.id, access_hash = media.access_hash, file_reference = media.file_reference, thumb_size = '')
	await bot.download_file(input_document_file, file=location)
	
