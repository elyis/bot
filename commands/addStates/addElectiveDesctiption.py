from telegram import Update
from telegram.ext import ConversationHandler

from config_variable import new_elective, ADD_ELECTIVE_AGE_LIMITS


def addElectiveDescription(update: Update, context):
    query = update.message.text
    while "  " in query:
        query = query.replace("  ", " ")

    if query.lower() == "/cancel":
        update.message.reply_text("Команда отменена")
        return ConversationHandler.END
    else:
        new_elective.description = query
        update.message.reply_text(text="Введите возрастные рамки в формате число - число:")
        return ADD_ELECTIVE_AGE_LIMITS

