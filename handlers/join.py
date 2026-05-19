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

        await update.message.reply_text(
            "❌ ใช้ /startgame ก่อน"
        )
        return

    if not context.args:

        await update.message.reply_text(
            "/join master\nหรือ\n/join slave"
        )
        return

    role = context.args[0].lower()

    room = rooms[chat_id]

    player = {
        "id": user.id,
        "name": user.first_name
    }

    all_users = room["masters"] + room["slaves"]

    for u in all_users:

        if u["id"] == user.id:

            await update.message.reply_text(
                "⚠️ เข้าร่วมแล้ว"
            )
            return

    if role == "master":

        room["masters"].append(player)

    elif role == "slave":

        room["slaves"].append(player)

    else:

        await update.message.reply_text(
            "❌ master/slave เท่านั้น"
        )
        return

    masters_text = ""

    for i, m in enumerate(room["masters"], start=1):

        masters_text += f"{i}. {m['name']}\n"

    slaves_text = ""

    for i, s in enumerate(room["slaves"], start=1):

        slaves_text += f"{i}. {s['name']}\n"

    await update.message.reply_text(

        f"👑 MASTERS\n"
        f"{masters_text}\n"
        f"━━━━━━━━━━\n\n"
        f"⛓ SLAVES\n"
        f"{slaves_text}"
    )