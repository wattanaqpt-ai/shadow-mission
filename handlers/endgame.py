from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from core.rooms import rooms

async def endgame(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    chat_id = update.effective_chat.id
    room = rooms.get(chat_id)

    if not room:
        await update.message.reply_text("❌ ไม่มีเกมในห้องนี้")
        return

    if not room["started"]:
        await update.message.reply_text("❌ เกมยังไม่เริ่ม")
        return

    room["endgame_votes"] = {"yes": [], "no": []}

    keyboard = [[
        InlineKeyboardButton("✅ ยอมแพ้", callback_data="endvote_yes"),
        InlineKeyboardButton("❌ สู้ต่อ", callback_data="endvote_no"),
    ]]

    await update.message.reply_text(
        "🏳️ มีการเสนอยุติเกม!\n\n"
        "ฝั่ง Slave โหวตกันเลย",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def endgame_vote_callback(
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

    slave_ids = [s["id"] for s in room["slaves"]]
    if user.id not in slave_ids:
        await query.answer("❌ เฉพาะ Slave เท่านั้น", show_alert=True)
        return

    votes = room["endgame_votes"]
    vote_type = query.data.replace("endvote_", "")

    votes["yes"] = [v for v in votes["yes"] if v != user.id]
    votes["no"] = [v for v in votes["no"] if v != user.id]

    votes[vote_type].append(user.id)

    yes_count = len(votes["yes"])
    no_count = len(votes["no"])
    total_slaves = len(room["slaves"])
    majority = total_slaves // 2 + 1

    await query.edit_message_text(
        f"🏳️ โหวตยุติเกม\n\n"
        f"✅ ยอมแพ้: {yes_count}\n"
        f"❌ สู้ต่อ: {no_count}\n"
        f"(ต้องการ {majority} เสียง)",
        reply_markup=query.message.reply_markup
    )

    if yes_count >= majority:
        scores = room.get("scores", {})
        sorted_scores = sorted(
            scores.values(),
            key=lambda x: x["count"],
            reverse=True
        )

        score_text = ""
        for i, s in enumerate(sorted_scores, start=1):
            score_text += f"{i}. {s['name']} — {s['count']} ภารกิจ\n"

        if not score_text:
            score_text = "ไม่มีใครทำภารกิจเลย\n"

        await context.bot.send_message(
            chat_id=chat_id,
            text=(
                f"🏁 GAME OVER — ฝั่ง Slave ยอมแพ้!\n\n"
                f"🎯 สถิติภารกิจ\n{score_text}\n"
                f"——————————\n"
                f"ขอบคุณทุกคนที่ร่วมเล่น!"
            )
        )

        del rooms[chat_id]