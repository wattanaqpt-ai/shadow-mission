from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import rooms

async def chat_filter(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not update.message:
        return

    if update.message.text and update.message.text.startswith("/"):
        return

    chat_id = update.effective_chat.id
    user = update.effective_user

    room = rooms.get(chat_id)

    if not room:
        return

    if not room["started"]:
        return

    players = room["masters"] + room["slaves"]

    allowed = False

    for p in players:

        if p["id"] == user.id:
            allowed = True
            break

    if not allowed:

        try:
            await update.message.delete()
        except:
            pass