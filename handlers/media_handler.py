import asyncio

from telegram import Update
from telegram.ext import ContextTypes, filters

from core.rooms import rooms
from core.media import auto_delete

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

    # รับเฉพาะคน claim
    if user.id != mission["claimed_by"]:
        return

    # PHOTO
    if update.message.photo:

        file_id = update.message.photo[-1].file_id

        # ลบต้นฉบับ
        await update.message.delete()

        # repost
        repost = await context.bot.send_photo(
            chat_id=chat_id,
            photo=file_id,
            caption=(
                "🎭 MISSION RESPONSE\n"
                "⏳ Auto delete in 2 minutes"
            )
        )

    # VIDEO
    elif update.message.video:

        file_id = update.message.video.file_id

        await update.message.delete()

        repost = await context.bot.send_video(
            chat_id=chat_id,
            video=file_id,
            caption=(
                "🎭 MISSION RESPONSE\n"
                "⏳ Auto delete in 2 minutes"
            )
        )

    else:
        return

    # save repost id
    mission["media_message_id"] = repost.message_id

    # auto delete
    asyncio.create_task(
        auto_delete(
            context,
            chat_id,
            repost.message_id
        )
    )

    # เปิด vote
    await start_vote(
        context,
        chat_id
    )