from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from commands.removeStates.choose_rm import showLearner, removeElective
from commands.removeStates.removeMenu import rmMenu
from config_variable import REMOVE_MORE, CHOOSE_RM


def distibutor(update: Update, context):
    query = update.message.text

    if query.lower() == "удалить учащегося":
        update.message.reply_text(reply_markup=ReplyKeyboardRemove(), text="Выбранно: удаление учащегося")
        if showLearner(update, context):
            return REMOVE_MORE
        else:
            rmMenu(update, context)
            return CHOOSE_RM

    elif query.lower() == "выбрать электив":
        if rmMenu(update, context) == CHOOSE_RM:
            return CHOOSE_RM

    elif query.lower() == "удалить электив":
        removeElective(update, context)
        return CHOOSE_RM

    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    else:
        update.message.reply_text(text="Введенно неизвестное действие. Пожалуйста, выберите из списка",)
