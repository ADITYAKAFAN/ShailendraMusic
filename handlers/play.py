import os
from os import path
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from callsmusic import callsmusic, queues
from callsmusic.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import youtube_dl
from youtube_search import YoutubeSearch
import converter
from downloaders import youtube
from config import DURATION_LIMIT, que
from cache.admins import admins as a
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from helpers.channelmusic import get_chat_id
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw

# plus
chat_id = None
DISABLED_GROUPS = []
useer ="NaN"
def cb_admin_check(func: Callable) -> Callable:
    async def decorator(client, cb):
        admemes = a.get(cb.message.chat.id)
        if cb.from_user.id in admemes:
            return await func(client, cb)
        await cb.answer("Yøʋ Ʌiŋ'ƭ Ʌlløɯɘɗ❗", show_alert=True)
        return

    return decorator

def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight))

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/oda.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")


@Client.on_message(
    command("musicplayer") & ~filters.edited & ~filters.bot & ~filters.private
)
@authorized_users_only
async def hfmm(_, message):
    global DISABLED_GROUPS
    try:
        user_id = message.from_user.id
    except:
        return
    if len(message.command) != 2:
        await message.reply_text(
            "I Øŋɭy Ʀɘƈøʛŋiʐɘ `/musicplayer on` Ʌŋɗ `/musicplayer off` Øŋɭy"
        )
        return
    status = message.text.split(None, 1)[1]
    message.chat.id
    if status in ["ON", "on", "On"]:
        lel = await message.reply("`**🔄 Ƥɤøƈƈɘssɩɳʛ....**`")
        if message.chat.id not in DISABLED_GROUPS:
            await lel.edit("Ɱʋsiƈ Ƥɭɑyɘɽ Aɭɽɘɑɗy Aƈƭiⱱɑƭɘɗ Iŋ Ƭɧis Ƈɧɑƭ")
            return
        DISABLED_GROUPS.remove(message.chat.id)
        await lel.edit(
            f"Ɱʋsiƈ Ƥɭɑyɘɽ Sʋƈƈɘssƒʋɭɭƴ Eŋɑɓɭɘɗ Føɽ Ʋsɘɽs Iŋ Tɧɘ Ƈɧɑƭ {message.chat.title}"
        )

    elif status in ["OFF", "off", "Off"]:
        lel = await message.reply("`**🔄 Ƥɤøƈƈɘssɩɳʛ....**`")

        if message.chat.id in DISABLED_GROUPS:
            await lel.edit("Ɱʋsiƈ Ƥɭɑyɘɽ Aɭɽɘɑɗy Ƭʋɽŋɘɗ Øʃʃ Iŋ Tɧɘ Ƈɧɑƭ")
            return
        DISABLED_GROUPS.append(message.chat.id)
        await lel.edit(
            f"Ɱʋsiƈ Ƥɭɑyɘɽ Sʋƈƈɘssƒʋɭɭƴ Ɗɘɑƈƭiⱱɑƭɘɗ Føɽ Ʋsɘɽs Iŋ Tɧɘ Ƈɧɑƭ {message.chat.title}"
        )
    else:
        await message.reply_text(
            "I Øŋɭy Ʀɘƈøʛŋiʐɘ `/musicplayer on` Ʌŋɗ `/musicplayer off` Øŋɭy"
        )

@Client.on_callback_query(filters.regex(pattern=r"^(cls)$"))
@cb_admin_check
async def m_cb(b, cb):
    global que    
    qeue = que.get(cb.message.chat.id)
    type_ = cb.matches[0].group(1)
    chat_id = cb.message.chat.id
    m_chat = cb.message.chat

    if type_ == "cls":          
        await cb.answer("Ƈløsɘɗ Ɱɘŋʋ")
        await cb.message.delete()

# play
@Client.on_message(command("play") & filters.group & ~filters.edited & ~filters.forwarded & ~filters.via_bot)
async def play(_, message: Message):
    global que
    global useer
    if message.chat.id in DISABLED_GROUPS:
        return
    lel = await message.reply("**🔄 Ƥɤøƈƈɘssɩɳʛ....**")

    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = "𝐒𝐇𝐀𝐈𝐋𝐄𝐍𝐃𝐑𝐀 𝐕𝐂 𝐏𝐋𝐀𝐘𝐄𝐑"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                await lel.edit(
                        "<b>Ʀɘɱɘɱɓɘɽ Ƭø Ʌɗɗ Hɘɭƥɘɽ Ƭø Yøʋɽ Ɠɽøʋƥ</b>",
                    )
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>🤖 Ʌʈ Fɩɤsʈ Ʌɗɗ Ɱɘ ƛs Ʌɗɱɩɳ Øƒ Yøʋɤ Ɠɤøʋƥ ❗️</b>",
                    )
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**🤖 Ɱʋsɪƈ Ʌssɩsʈɑɳƈɘ Jøɩɳɘɗ Yøʋɤ Ɠɤøʋƥ ❗️**"
                    )
                    await lel.edit(
                        "</b>**🤖 Ɱʋsɪƈ Ʌssɩsʈɑɳƈɘ Jøɩɳɘɗ Yøʋɤ Ɠɤøʋƥ ❗️**",
                    )

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🤖 Fɭøøɗ Eɤɤøɤ - Ɱɑɳʋɑɭɭƴ Ʌɗɗ Ɱʋsɪƈ Ʌssɩsʈɑɳƈɘ ʈø Yøʋɤ Ɠɤøʋƥ øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ...</b>")
    try:
        await USER.get_chat(chid)
        # lmoa = await client.get_chat_member(chid,wew)
    except:
        await lel.edit(
            f"<i>🤖 Ɱʋsɪƈ Ʌssɩsʈɑɳƈɘ Ɲøʈ ɩɳ Yøʋɤ Ɠɤøʋƥ...\nƤɭɘasɘ Ʌɗɗ ɩʈ  Ɱɑɳɳʋɑɭɭƴ Øɤ Ƈøɳʈɑƈʈ ʈø Ɱʋsɩƈ Ɓøʈ Øωɳɘɤ... </i>")
        return

    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ Ɱʋsɩƈ Vɩɗɘøs Løɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʉʈɘs ƛɤɘ Ɲøʈ Ʌɭɭøωɘɗ ʈø Ƥɭɑƴ... ❗"
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/eb72b6980a246049baeb7.png"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "📖 Ƥlɑylisƭ", callback_data="playlist"
                    ),
                    InlineKeyboardButton("🎭 Ʋƥɗɑƭɘs Ƈɧɑŋŋɘl 🔥", url='t.me/MODMENUMAKING'),
                ],
                [InlineKeyboardButton(text="❎ Ƈløsɘ", callback_data="cls"),
                ],
                [lnlineKeyboardButton(text="✅ Øɯŋɘɤ", url=f" https://t.me/Shailendra34") 
            ]
        )


        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60

            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "☯ Sʋƥƥøɤƭ", url='t.me/YAARO_KI_YAARII'
                        ),
                        InlineKeyboardButton(
                            "🎭 Ʋƥɗɑƭɘs Ƈɧɑŋŋɘl 🔥", url='t.me/MODMENUMAKING'
                        ),
                    ],
                    [
                        InlineKeyboardButton(
                            text="❌ Ƈløsɘ", callback_data="cls"
                        ), 
                        lnlineKeyboardButton(text="✅ Ƈøŋƭɑƈƭ Øɯŋɘɤ", url=f" https://t.me/Shailendra34") 
                    ],
                ]
            )

        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/eb72b6980a246049baeb7.png"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="YouTube 🎬", url='https://youtube.com'
                        )
                    ]
                ]
            )

        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ Ɱʋsɩƈ Vɩɗɘøs Løɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʉʈɘs ƛɤɘ Ɲøʈ Ʌɭɭøωɘɗ ʈø Ƥɭɑƴ... ❗")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("**🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**")
        await lel.edit("**🔎 Sɘɑɤƈɦɩɳʛ...**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("**🔄 Ƥɤøƈƈɘssɩɳʛ...**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60

        except Exception as e:
            await lel.edit(
                "**🎶 Søɳʛ Ɲøʈ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Søɳʛ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**"
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Sʋƥƥøɤƭ", url='t.me/YAARO_KI_YAARII'),
                    InlineKeyboardButton("Ʋƥɗɑƭɘs", url='t.me/MODMENUMAKING'),
                ],
                [InlineKeyboardButton(text="❌ Ƈløsɘ", callback_data="cls")],
            ]
        )


        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ Ɱʋsɩƈ Vɩɗɘøs Løɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʉʈɘs ƛɤɘ Ɲøʈ Ʌɭɭøωɘɗ ʈø Ƥɭɑƴ... ❗")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)
        file_path = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.pytgcalls.active_calls:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**🎵 Søŋʛ:** {}\n**🕒 Ɗʋɤɑƭiøŋ:** {} ɱiɳ\n**👤 Ʌɗɗɘɗ Ɓy:** {}\n\n**#⃣ Qʋɘʋɘɗ Ƥøsiƭiøŋ:** {}".format(
        title, duration, message.from_user.mention(), position,
        ),
        reply_markup=keyboard)
    else:
        callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**🎵 Søŋʛ:** {}\n**🕒 Ɗʋɤɑƭiøŋ:** {} min\n**👤 Ʌɗɗɘɗ Ɓy:** {}\n\n**▶️ Ɲøɯ Ƥlɑyiŋʛ Ʌƭ `{}`...**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )

    os.remove("final.png")
    return await lel.delete()
