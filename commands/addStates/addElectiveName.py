from telegram import Update
from telegram.ext import ConversationHandler

from config_variable import new_elective, ADD_ELECTIVE_DESCRIPTION


def enterElectiveName(update: Update, context):
    query = update.message.text
    while "  " in query:
        query = query.replace("  ", " ")

    if query.lower() == "/cancel":
        update.message.reply_text("Команда отменена")
        return ConversationHandler.END

    else:
        new_elective.name = query
        update.message.reply_text(text="Введите описание электива:")
        return ADD_ELECTIVE_DESCRIPTION
