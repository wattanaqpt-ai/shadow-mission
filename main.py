from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters
)

from config import TOKEN

# handlers
from handlers.game import startgame
from handlers.join import join
from handlers.mission import mission

from handlers.claim import claim_callback
from handlers.media_handler import media_handler
from handlers.vote import vote_callback

# build app
app = ApplicationBuilder().token(TOKEN).build()

# commands
app.add_handler(
    CommandHandler(
        "startgame",
        startgame
    )
)

app.add_handler(
    CommandHandler(
        "join",
        join
    )
)

app.add_handler(
    CommandHandler(
        "mission",
        mission
    )
)

# claim button
app.add_handler(
    CallbackQueryHandler(
        claim_callback,
        pattern="claim"
    )
)

# vote button
app.add_handler(
    CallbackQueryHandler(
        vote_callback,
        pattern="vote_"
    )
)

# media handler
app.add_handler(
    MessageHandler(
        filters.PHOTO | filters.VIDEO,
        media_handler
    )
)

print("BOT RUNNING...")

# run bot
app.run_polling()