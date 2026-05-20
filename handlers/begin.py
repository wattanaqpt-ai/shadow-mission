from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import rooms
from core.turns import get_current_master

async def begin(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    room = rooms.get(chat_id)

    if not room:
        return

    if len(room["masters"]) == 0:
        await update.message.reply_text("❌ ไม่มี MASTER")
        return

    if len(room["slaves"]) == 0:
        await update.message.reply_text("❌ ไม่มี SLAVE")
        return

    room["started"] = True

    current_master = get_current_master(room)

    msg = await update.message.reply_text(
        f"🎭 GAME START\n\n"
        f"👑 TURN: {current_master['name']}\n\n"
        f"/mission ..."
    )

    room["message_ids"].append(msg.message_id)
