from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

from config_variable import ADD_ELECTIVE_NAME


def addNameElective(update: Update, context):
    update.message.reply_text("Введите наименование нового факультатива:")
    return ADD_ELECTIVE_NAME
