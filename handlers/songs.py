# Veez Music Bot (https://t.me/veezmusicbot)

import os
import aiohttp
import asyncio
import json
import sys
import time
from youtubesearchpython import SearchVideos
from pyrogram import filters, Client
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

@Client.on_message(filters.command("song") & ~filters.edited)
async def song(client, message):
    cap = "**🎵 Ƭɦɩs Søɳʛ ɩs Ʋƥɭøɑɗɘɗ Ɓƴ [Sɧɑiɭɘɳɗɽɑ](https://t.me/Shailendra34)...**"
    url = message.text.split(None, 1)[1]
    rkp = await message.reply("**🔎 Fɩɳɗɩɳʛ Yøʋr Søɳʛ...**")
    if not url:
        await rkp.edit("**🎶 Ɲøʈɦɩɳʛ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Ƙɘƴωøɤɗ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("**🎶 Ɲøʈɦɩɳʛ Føʋɳɗ, Ƭɤƴ Ʌɳøʈɦɘɤ Ƙɘƴωøɤɗ øɤ Ɱɑƴɓɘ Sƥɘɭɭ ɩʈ Ƥɤøƥɘɤɭƴ.**")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("**📥 Ɗøωŋɭøɑɗɩɳʛ Yøʋɤ Søɳʛ...**")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`Ƭɧɘ Ɗøɯŋløɑɗ Ƈøŋƭɘŋƭ Ɯɑs Ƭøø Sɧøɤƭ.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Viɗɘø Is Ɲøƭ Ʌⱱɑilɑɓlɘ Fɤøɱ Yøʋɤ Ɠɘoʛɤɑƥɧiƈ Løƈɑƭiøŋ Ɗʋɘ Ƭø Ɠɘoʛɤɑƥɧiƈ Ʀɘsƭɤiƈƭiøŋs Iɱƥøsɘɗ Ɓy Ʌ Ɯɘɓsiƭɘ.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("**👉 Ʌɳøʈɦɘɤ Ɗøωŋɭøɑɗ ɩs ɩɳ Ƥɤøʛɤɘss, Ƭɤƴ Ʌʛɑɩɳ Ʌƒʈɘɤ Søɱɘʈɩɱɘ...**")
        return
    except PostProcessingError:
        await rkp.edit("**❌ Eɤɤøɤ ❌**")
        return
    except UnavailableVideoError:
        await rkp.edit("Ɱɘɗiɑ Is Ɲøƭ Ʌⱱɑilɑɓlɘ Iŋ Ƭɧɘ Ʀɘɋʋɘsƭɘɗ Føɤɱɑƭ")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("Ƭɧɘɤɘ Ɯɑs Ʌŋ Eɤɤøɤ Ɗʋɤiŋʛ Iŋʆø Exƭɤɑƈƭiøŋ")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("**📤 Ʋƥɭøɑɗɩɳʛ Yøʋɤ Søɳʛ ...**") #Shailendra34
        lol = "./etc/thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  #Shailendra34
        await rkp.delete()
