from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)
from telegram.ext import ContextTypes

from core.rooms import rooms
from core.turns import get_current_master

async def mission(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    user = update.effective_user

    room = rooms.get(chat_id)
    if not room:
        return

    if not room["started"]:
        await update.message.reply_text(
            "❌ เกมยังไม่เริ่ม"
        )
        return

    current_master = get_current_master(room)
    if user.id != current_master["id"]:
        await update.message.reply_text(
            "❌ ยังไม่ใช่ TURN ของคุณ"
        )
        return

    if room["active_mission"]:
        await update.message.reply_text(
            "❌ ยังมี MISSION ค้างอยู่"
        )
        return

    text = " ".join(context.args)
    if not text:
        await update.message.reply_text(
            "/mission ข้อความ"
        )
        return

    room["active_mission"] = {
        "text": text,
        "claimed": False,
        "claimed_by": None,
        "voted_users": [],
        "votes": {
            "pass": 0,
            "fail": 0,
            "funny": 0
        }
    }

    keyboard = [[
        InlineKeyboardButton(
            "🎯 ACCEPT",
            callback_data="claim"
        )
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"🃏 {text}",
        reply_markup=reply_markup
    )