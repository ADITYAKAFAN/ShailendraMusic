from os import path

from youtube_dl import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError


ydl_opts = {
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)


def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 60)

    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"❌ Vɩɗɘøs Løɳʛɘɤ Ƭɦɑɳ {DURATION_LIMIT} Ɱɩɳʉʈɘs ƛɤɘ Ɲøʈ Ʌɭɭøωɘɗ, Ƭɦɘ Ƥɤøⱱɩɗɘɗ Vɩɗɘø ɩs {duration} Ɱɩɳʉʈɘs ..."
        )

    ydl.download([url])
    return path.join("downloads", f"{info['id']}.{info['ext']}")
