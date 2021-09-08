from pyrogram import Client, filters
from handlers import check_heroku

@Client.on_message(filters.command('restart') & filters.user{SUDO_USERS}) 
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_text("Sɧɑilɘŋɗɤɑ Ɱʋsiƈs →→ Ʀɘsƭɑɤƭiŋʛ")
    hap.restart()
