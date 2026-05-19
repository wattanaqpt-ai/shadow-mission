from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import (
    rooms,
    create_room
)

async def startgame(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id

    if chat_id in rooms:

        await update.message.reply_text(
            "❌ มีเกมอยู่แล้ว"
        )
        return

    create_room(chat_id)

    await update.message.reply_text(

        "🎭 SHADOW MISSION\n\n"
        "/join master\n"
        "/join slave"
    )