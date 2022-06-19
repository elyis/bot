from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler


def cancel(update: Update, context) -> int:
    update.message.reply_text(
        "Регистрация отменена", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END