import exfil
import order
import summary
import transform
import os
import sys

def exfiltrate_bot(api_id, api_hash, bot_token, exfiltrate_again, start_index = 0, end_index = 200, chat_id=None):
	if os.path.exists("./bot.session"):
		os.remove("bot.session")
	if exfiltrate_again:
		print("Exfiltrating messages")
		exfil.exfil(api_id, api_hash, bot_token, start_index, end_index, chat_id)
	print("Ordering messages")
	order.order(bot_token)
	print("Creating summary")
	summary.summary(api_id, api_hash, bot_token)
	print("Creating HTML chat logs")
	transform.transform(api_id, api_hash, bot_token)
	print("Finished")
	print("Extracted chat logs can be found in the", bot_token, "folder")
	
api_id = #API ID
api_hash = #API Hash
bot_token = #Bot token
start_message_index = #Index of first message
end_message_index = #Index of last message

exfiltrate_bot(api_id, api_hash, bot_token, True, start_message_index, end_message_index)
