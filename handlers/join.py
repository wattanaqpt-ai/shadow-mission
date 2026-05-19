from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import rooms

async def join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in rooms:
        return

    args = context.args

    if not args:
        return

    role = args[0].lower()

    room = rooms[chat_id]

    player = {
        "id": user.id,
        "name": user.first_name
    }

    if role == "master":
        room["masters"].append(player)

    elif role == "player":
        room["players"].append(player)

    else:
        return

    await update.message.reply_text(
        f"✅ {user.first_name} joined as {role}"
    )