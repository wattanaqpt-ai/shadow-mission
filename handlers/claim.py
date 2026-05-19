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

    # มีคนรับแล้ว
    if mission["claimed"]:

        await query.answer(
            "❌ มีคนรับแล้ว",
            show_alert=True
        )
        return

    # lock mission
    mission["claimed"] = True
    mission["claimed_by"] = user.id

    await query.edit_message_text(
        f"🎭 MISSION CLAIMED\n\n"
        f"⏳ รอส่งรูป/คลิป"
    )