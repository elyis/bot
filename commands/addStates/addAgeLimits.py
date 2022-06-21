from telegram import Update
from telegram.ext import ConversationHandler

from config_variable import new_elective, ADD_ELECTIVE_TOTAL_SEATS


def addAgeLimits(update: Update, context):
    query = update.message.text

    if query.lower() == "/cancel":
        update.message.reply_text("Команда отменена")
        return ConversationHandler.END

    else:
        while " " in query:
            query = query.replace(" ", "")
        query = query.split("-")

        if len(query) == 2:
            if query[0].isdigit() and query[1].isdigit():
                new_elective.init_age = int(query[0])
                new_elective.final_age = int(query[1])
                update.message.reply_text(text="Введите максимальное количество человек в группе:")
                return ADD_ELECTIVE_TOTAL_SEATS
            else:
                update.message.reply_text("Одно из чисел является текстом. Пожалуйста, введите в формате 'число - "
                                          "число'")
        else:
            update.message.reply_text("Введен неверный формат. Пожалуйста, введите в формате 'число - число'")

