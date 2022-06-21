from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import categoriesSuitableForStudentByAge, FULLNAME, new_learner


# Сохраняет выбранный факультатив и перебрасывает на форму ввода ФИО
def saveSelectedElective(update: Update, context):
    query = update.message.text

    if query.isdigit():
        if int(query) in range(1, len(categoriesSuitableForStudentByAge) + 1):
            new_learner[update.effective_chat.id].elective = categoriesSuitableForStudentByAge[int(query) - 1]
            update.message.reply_text("Введите ФИО ребенка полностью:", reply_markup=ReplyKeyboardRemove())
            return FULLNAME

        else:
            update.message.reply_text("Введено значение не являющееся индексом доступных элективов. Пожалуйста, введите число из доступных")

    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(
            "Регистрация отменена", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    else:
        update.message.reply_text("Введен текст, пожалуйста, введите число:")
