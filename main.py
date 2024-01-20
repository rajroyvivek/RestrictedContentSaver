import pyrogram
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant, InviteHashExpired, UsernameNotOccupied
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import time
import os
import threading
import json

with open('config.json', 'r') as f: DATA = json.load(f)
def getenv(var): return os.environ.get(var) or DATA.get(var, None)

bot_token = getenv("TOKEN") 
api_hash = getenv("HASH") 
api_id = getenv("ID")
bot = Client("mybot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

ss = getenv("STRING")
if ss is not None:
	acc = Client("myacc" ,api_id=api_id, api_hash=api_hash, session_string=ss)
	acc.start()
else: acc = None

# download status
def downstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as downread:
			txt = downread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Downloaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# upload status
def upstatus(statusfile,message):
	while True:
		if os.path.exists(statusfile):
			break

	time.sleep(3)      
	while os.path.exists(statusfile):
		with open(statusfile,"r") as upread:
			txt = upread.read()
		try:
			bot.edit_message_text(message.chat.id, message.id, f"__Uploaded__ : **{txt}**")
			time.sleep(10)
		except:
			time.sleep(5)


# progress writter
def progress(current, total, message, type):
	with open(f'{message.id}{type}status.txt',"w") as fileup:
		fileup.write(f"{current * 100 / total:.1f}%")


# start command
#@bot.on_message(filters.command(["start"]))
#def send_start(client: pyrogram.client.Client, message: pyrogram.types.messages_and_media.message.Message):
#	bot.send_message(message.chat.id, f"**__👋 Hi** **{message.from_user.mention}**, **I am Save Restricted Bot, I can send you restricted content by it's post link__**\n\n{USAGE}",
#	reply_markup=InlineKeyboardMarkup([[ InlineKeyboardButton("🌐 Update Channel", url="https://t.me/Movies_X_Store")]]), reply_to_message_id=message.id)



@bot.on_message(filters.private & filters.command("start"))
def start(client, message):
    client.send_message(
        message.chat.id,
        "Send Me Bot Token To Check It's Valid Or Not."
    )

@bot.on_message(filters.text & filters.private)
def check_token(client, message):
    token = message.text
    if 1 == 1:
        client.send_message(message.chat.id, " Plz Wait Baby I'm Checking This Token...")
        new_bot = Client("newbotcheck", api_id=api_id, api_hash=api_hash, bot_token=token)
        new_bot.start()
        client.send_message(message.chat.id, f="Boom Valid Token 💥 {token}")
    else:
        client.send_message(message.chat.id, "Invalid bot token!")



# get the type of message
def get_message_type(msg: pyrogram.types.messages_and_media.message.Message):
	try:
		msg.document.file_id
		return "Document"
	except: pass

	try:
		msg.video.file_id
		return "Video"
	except: pass

	try:
		msg.animation.file_id
		return "Animation"
	except: pass

	try:
		msg.sticker.file_id
		return "Sticker"
	except: pass

	try:
		msg.voice.file_id
		return "Voice"
	except: pass

	try:
		msg.audio.file_id
		return "Audio"
	except: pass

	try:
		msg.photo.file_id
		return "Photo"
	except: pass

	try:
		msg.text
		return "Text"
	except: pass


USAGE = """**FOR PUBLIC CHATS**

**__just send post/s link__**

**FOR PRIVATE CHATS**

**__first send invite link of the chat (unnecessary if the account of string session already member of the chat)
then send post/s link__**

**FOR BOT CHATS**

**__send link with** '/b/', **bot's username and message id, you might want to install some unofficial client to get the id like below__**

```
https://t.me/b/botusername/4321
```

**MULTI POSTS**

**__send public/private posts link as explained above with formate "from - to" to send multiple messages like below__**

```
https://t.me/xxxx/1001-1010

https://t.me/c/xxxx/101 - 120
```

**__note that space in between doesn't matter__**
"""


# infinty polling
bot.run()
