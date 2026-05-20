import asyncio

from core.rooms import rooms
from core.turns import next_master, get_current_master

async def auto_delete(
    context,
    chat_id,
    message_id
):
    await asyncio.sleep(120)

    try:
        await context.bot.delete_message(
            chat_id=chat_id,
            message_id=message_id
        )
    except:
        pass

    room = rooms.get(chat_id)
    if not room:
        return

    if not room["active_mission"]:
        return

    room["active_mission"] = None
    next_master(room)

    current_master = get_current_master(room)

    msg = await context.bot.send_message(
        chat_id=chat_id,
        text=(
            f"⏰ หมดเวลา — MISSION ถูกยกเลิก\n\n"
            f"👑 TURN: {current_master['name']}\n\n"
            f"พิมพ์ /mission ข้อความ"
        )
    )

    room["message_ids"].append(msg.message_id)
