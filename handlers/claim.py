from telegram import Update
from telegram.ext import ContextTypes
from core.rooms import rooms

async def claim_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    user = query.from_user

    room = rooms.get(chat_id)
    if not room:
        return

    mission = room["active_mission"]
    if not mission:
        return

    if mission["claimed"]:
        await query.answer(
            "❌ มีคนรับแล้ว",
            show_alert=True
        )
        return

    mission["claimed"] = True
    mission["claimed_by"] = user.id

    room["scores"][user.id] = room["scores"].get(
        user.id,
        {"name": user.first_name, "count": 0}
    )
    room["scores"][user.id]["count"] += 1

    await query.edit_message_text(
        "🎭 MISSION CLAIMED\n\n"
        "⏳ ส่งรูปหรือคลิป"
    )