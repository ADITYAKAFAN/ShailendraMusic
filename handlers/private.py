from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""**🙋‍ Ɦɘɭɭø, I ɑɱ ɑɳ Ʌɗⱱɑɳƈɘɗ Ƥrɘɱɩʋɱ Ɱʉsɩƈ Ƥɭɑƴɘr Ɓøʈ Ƈrɘɑʈɘɗ Ɓƴ [Sɧɑiɭɘɳɗɽɑ](t.me/Shailendra34). I Ƈɑɳ Ƥɭɑƴ Ɱʉsɩƈ ɩɳ Yøʋr Ƭɘɭɘʛrɑɱ Ɠrøuƥ Vøɩƈɘ Ƈɦɑʈ...**"
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "➕ Ʌɗɗ Ɱɘ ʈø Yøʋɤ Ɠɤøʋƥ ➕", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
                [
                    InlineKeyboardButton(
                        "🌐 Ʋƥɗɑʈɘs", url=f"https://t.me/MODMENUMAKING"), 
                    InlineKeyboardButton(
                        "💬 Sʋƥƥøɽƭ", url=f"https://t.me/YAARO_KI_YAARII")
                ],[
                    InlineKeyboardButton(
                        "🤖 Øωɳɘɤ 🤖", url=f"https://t.me/Shailendra34")
                  ]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""** ✅ Ɱʋsɩƈ Ɓøʈ ɩs Øŋɭɩɳɘ**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔥 Ʋƥɗɑʈɘs 🔥", url=f"https://t.me/MODMENUMAKING")
                ]
            ]
        )
   )


