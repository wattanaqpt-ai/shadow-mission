from telegram import Update
from telegram.ext import ContextTypes

from core.rooms import rooms

async def join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    user = update.effective_user

    # ไม่มีห้อง
    if chat_id not in rooms:

        await update.message.reply_text(
            "❌ ยังไม่ได้เริ่มเกม\nใช้ /startgame ก่อน"
        )
        return

    # ไม่มี argument
    if not context.args:

        await update.message.reply_text(
            "ใช้:\n/join master\nหรือ\n/join player"
        )
        return

    role = context.args[0].lower()

    room = rooms[chat_id]

    player = {
        "id": user.id,
        "name": user.first_name
    }

    # กัน join ซ้ำ
    all_users = room["masters"] + room["players"]

    for u in all_users:

        if u["id"] == user.id:

            await update.message.reply_text(
                "⚠️ คุณเข้าร่วมแล้ว"
            )
            return

    # join role
    if role == "master":

        room["masters"].append(player)

    elif role == "player":

        room["players"].append(player)

    else:

        await update.message.reply_text(
            "❌ ใช้ได้แค่ master หรือ player"
        )
        return

    # สร้างข้อความรายชื่อ
    masters_text = ""

    for i, m in enumerate(room["masters"], start=1):

        masters_text += f"{i}. {m['name']}\n"

    players_text = ""

    for i, p in enumerate(room["players"], start=1):

        players_text += f"{i}. {p['name']}\n"

    # ส่งผล
    await update.message.reply_text(

        f"👑 MASTERS\n"
        f"{masters_text}\n"
        f"━━━━━━━━━━\n\n"
        f"🎮 PLAYERS\n"
        f"{players_text}"
    )