from telegram.ext import (
    ApplicationBuilder,
    CommandHandler
)

from config import TOKEN

from handlers.game import startgame
from handlers.join import join
from handlers.mission import mission

app = ApplicationBuilder().token(TOKEN).build()

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

print("BOT RUNNING...")

app.run_polling()