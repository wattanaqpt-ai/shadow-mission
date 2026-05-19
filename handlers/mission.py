from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ContextTypes
)

from core.rooms import rooms
from core.missions import create_mission
from core.turns import get_current_master

async def mission(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    chat_id = update.effective_chat.id
    user = update.effective_user

    if chat_id not in rooms:
        return

    room = rooms[chat_id]

    if room["mission_lock"]:

        await update.message.reply_text(
            "⚠️ มีภารกิจอยู่แล้ว"
        )
        return

    current_master = get_current_master(room)

    if user.id != current_master["id"]:

        await update.message.reply_text(
            "❌ ไม่ใช่ turn ของคุณ"
        )
        return

    text = " ".join(context.args)

    mission_data = create_mission(
        text,
        user.id
    )

    room["active_mission"] = mission_data
    room["mission_lock"] = True

    keyboard = [
        [
            InlineKeyboardButton(
                "🎯 ACCEPT",
                callback_data="claim"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    await update.message.reply_text(
        f"🃏 NEW MISSION\n\n📜 {text}",
        reply_markup=reply_markup
    )