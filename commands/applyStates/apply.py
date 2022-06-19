from telegram import Update

from config_variable import AGE


def apply(update: Update, context):
    update.message.reply_text(text="Введите возраст ребенка:")
    return AGE
