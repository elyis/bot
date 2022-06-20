
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from commands.removeStates.choose_rm import showLearner
from commands.removeStates.removeMenu import rmMenu
from commands.removeStates.remove_elective import removeElective
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
    else:
        update.message.reply_text(text="Удаление завершенно", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
