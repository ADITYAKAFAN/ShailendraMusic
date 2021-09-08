from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
import sira
import tgcalls
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.filters import command, other_filters
from callsmusic import callsmusic


@Client.on_message(command("pause") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'paused'
    ):
        await message.reply_text("**🚫 Ɲøʈɦɩɳʛ ɩs Ƥɭɑƴɩɳʛ ❗️**")
    else:
        callsmusic.pytgcalls.pause_stream(message.chat.id)
        await message.reply_text("**▶️ ️Sʋƈƈɘssƒʋɭɭƴ Ƥɑʋsɘɗ ❗**")


@Client.on_message(command("resume") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if (
            message.chat.id not in callsmusic.pytgcalls.active_calls
    ) or (
            callsmusic.pytgcalls.active_calls[message.chat.id] == 'playing'
    ):
        await message.reply_text("**🚫 Ɲøʈɦɩɳʛ ɩs Ƥɑʋsɘɗ ❗**")
    else:
        callsmusic.pytgcalls.resume_stream(message.chat.id)
        await message.reply_text("**⏸ ️Sʋƈƈɘssƒʋɭɭƴ Ʀɘsʋɱɘɗ ❗**")


@Client.on_message(command("stop") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**🚫 Ɲøʈɦɩɳʛ ɩs Sʈɤɘɑɱɩɳʛ ❗**")
    else:
      try:
        callsmusic.queues.clear(message.chat.id)
      except QueueEmpty:
        pass

      callsmusic.pytgcalls.leave_group_call(message.chat.id)
      await message.reply_text("**❌ Sʋƈƈɘssƒʋɭɭƴ Sʈøƥƥɘɗ Sʈɤɘɑɱɩɳʛ ❗**")


@Client.on_message(command("skip") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.pytgcalls.active_calls:
        await message.reply_text("**🚫 Ɲøʈɦɩɳʛ ɩs Ƥɭɑƴɩɳʛ ʈø Sƙɩƥ ❗**")
    else:
        callsmusic.queues.task_done(message.chat.id)

        if callsmusic.queues.is_empty(message.chat.id):
            callsmusic.pytgcalls.leave_group_call(message.chat.id)
        else:
            callsmusic.pytgcalls.change_stream(
                message.chat.id,
                callsmusic.queues.get(message.chat.id)["file"]
            )

        await message.reply_text("**⏩ Sʋƈƈɘssƒʋɭɭƴ Sƙɩƥƥɘɗ Ƭɦɘ Søɳʛ ❗**")

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_text(f"- Sƙɩƥƥɘɗ **{Sƙɩƥ[0]}**\n- Ɲøw Ƥɭɑƴɩɳʛ **{qeue[0][0]}**")


@Client.on_message(filters.command("reload"))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(
                filter="administrators"
            )
        ),
    )

    await message.reply_text("✅️ **Ʌɗɱiŋ Lisʈ** Is **Ʋƥɗɑʈɘɗ**")
