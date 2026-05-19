from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import ContextTypes

from core.rooms import rooms
from core.turns import next_master, get_current_master

async def start_vote(
    context,
    chat_id
):
    keyboard = [
        [
            InlineKeyboardButton(
                "✅ PASS",
                callback_data="vote_pass"
            ),
            InlineKeyboardButton(
                "❌ FAIL",
                callback_data="vote_fail"
            ),
            InlineKeyboardButton(
                "😂 FUNNY",
                callback_data="vote_funny"
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=chat_id,
        text="🗳 RESULT?",
        reply_markup=reply_markup
    )

async def vote_callback(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    await query.answer()

    chat_id = query.message.chat.id
    room = rooms.get(chat_id)

    if not room:
        return

    mission = room["active_mission"]
    if not mission:
        return

    vote_type = query.data.replace("vote_", "")
    mission["votes"][vote_type] += 1

    votes = mission["votes"]
    text = (
        "🗳 CURRENT VOTES\n\n"
        f"✅ PASS: {votes['pass']}\n"
        f"❌ FAIL: {votes['fail']}\n"
        f"😂 FUNNY: {votes['funny']}"
    )

    await query.edit_message_text(text)

    total = votes["pass"] + votes["fail"] + votes["funny"]

    if total >= 3:
        room["active_mission"] = None
        next_master(room)

        current_master = get_current_master(room)

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🔄 NEXT MISSION\n\n"
                f"👑 TURN: {current_master['name']}\n\n"
                f"พิมพ์ /mission ข้อความ"
            )
        )