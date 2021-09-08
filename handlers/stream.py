from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import BOT_NAME as bn, DURATION_LIMIT, UPDATES_CHANNEL, AUD_IMG, QUE_IMG, GROUP_SUPPORT
from helpers.filters import command, other_filters
from helpers.decorators import errors
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(command("stream") & other_filters)
@errors
async def stream(_, message: Message):

    lel = await message.reply("**🔄 Ƥɤøƈƈɘssɩɳʛ ...**")
    sender_id = message.from_user.id
    sender_name = message.from_user.first_name

    keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="✨ Ɠɤøʋƥ",
                        url=f"https://t.me/YAARO_KI_YAARII"),
                    InlineKeyboardButton(
                        text="🌻 Ƈɧɑŋŋɘl",
                        url=f"https://t.me/{UPDATES_CHANNEL}")
                ]
            ]
        )

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Ɱʋsɩƈ Vɩɗɘøs Løɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʉʈɘs ƛɤɘ Ɲøʈ Ʌɭɭøωɘɗ ʈø Ƥɭɑƴ... ❗"
            )

        file_name = get_file_name(audio)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    elif url:
        file_path = await converter.convert(youtube.download(url))
    else:
        return await lel.edit_text("Yøʋ Ɗiɗ Ɲøƭ Ɠiⱱɘ Ɱɘ Ʌʋɗiø Filɘ Øɤ Yøʋƭʋⱱɘ Liŋƙ Ƭø Sƭɤɘɑɱ❗")

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo=f"{QUE_IMG}",
        reply_markup=keyboard,
        caption=f"#⃣  Yøʋɤ Ʀɘɋʋɘsƭɘɗ Søŋʛ Ɯɑs Ʌɗɗɘɗ Ƭø *𝐪𝐮𝐞𝐮𝐞* Ʌƭ Ƥøsiƭiøŋ {position} ❗\n\n⚡ __𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 [Sɧɑilɘŋɗɤɑ Ɱʋsiƈs](https://t.me/Yaaro_ki_yaarii)__")
        return await lel.delete()
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        costumer = message.from_user.mention
        await message.reply_photo(
        photo=f"{AUD_IMG}",
        reply_markup=keyboard,
        caption=f"🎧 **Ɲøɯ Ƥlɑyiŋʛ** Ʌ Søŋʛ Ʀɘɋʋɘsƭɘɗ Ɓy {costumer} ❗\n\n⚡ __𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐛𝐲 [Sɧɑilɘŋɗɤɑ Ɱʋsiƈs](https://t.me/Yaaro_ki_yaarii)__"
        )
        return await lel.delete()
