from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import TOKEN

from handlers.game import startgame
from handlers.join import join
from handlers.begin import begin
from handlers.mission import mission
from handlers.claim import claim_callback
from handlers.media_handler import media_handler
from handlers.vote import vote_callback
from handlers.chat_filter import chat_filter
from handlers.endgame import endgame, endgame_vote_callback

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("startgame", startgame))
app.add_handler(CommandHandler("join", join))
app.add_handler(CommandHandler("begin", begin))
app.add_handler(CommandHandler("mission", mission))
app.add_handler(CommandHandler("endgame", endgame))

app.add_handler(CallbackQueryHandler(claim_callback, pattern="claim"))
app.add_handler(CallbackQueryHandler(vote_callback, pattern="vote_"))
app.add_handler(CallbackQueryHandler(endgame_vote_callback, pattern="endvote_"))

app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, media_handler))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_filter))

print("BOT RUNNING...")
app.run_polling()