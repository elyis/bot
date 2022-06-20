from telegram import Update

from config_variable import new_elective, ADD_ELECTIVE_DESCRIPTION


def enterElectiveName(update: Update, context):
    query = update.message.text
    while "  " in query:
        query = query.replace("  ", " ")

    new_elective.name = query
    update.message.reply_text(text="Введите описание электива:")
    return ADD_ELECTIVE_DESCRIPTION
