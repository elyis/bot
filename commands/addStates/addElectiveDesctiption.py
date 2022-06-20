from telegram import Update

from config_variable import new_elective, ADD_ELECTIVE_AGE_LIMITS


def addElectiveDescription(update: Update, context):
    query = update.message.text
    while "  " in query:
        query = query.replace("  ", " ")

    new_elective.description = query
    update.message.reply_text(text="Введите возрастные рамки в формате число - число:")
    return ADD_ELECTIVE_AGE_LIMITS

