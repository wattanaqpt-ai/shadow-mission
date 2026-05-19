import asyncio

from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import rooms
from core.media import auto_delete

from handlers.vote import start_vote

async def media_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    user = update.effective_user

    room = rooms.get(chat_id)

    if not room:
        return

    mission = room["active_mission"]

    if not mission:
        return

    if user.id != mission["claimed_by"]:
        return

    repost = None

    if update.message.photo:

        file_id = update.message.photo[-1].file_id

        await update.message.delete()

        repost = await context.bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption="🎭 MISSION RESPONSE",
            protect_content=True
        )

    elif update.message.video:

        file_id = update.message.video.file_id

        await update.message.delete()

        repost = await context.bot.send_video(
            chat_id=chat_id,
            video=file_id,
            caption="🎭 MISSION RESPONSE",
            protect_content=True
        )

    else:
        return

    asyncio.create_task(
        auto_delete(
            context,
            chat_id,
            repost.message_id
        )
    )

    await start_vote(
        context,
        chat_id
    )