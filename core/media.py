import asyncio

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