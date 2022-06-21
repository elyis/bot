from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import NUMPHONE, new_learner, GENDER


#Ввод ФИО и выбор пола ребенка
def enterFullName(update: Update, context):
    fullname = update.message.text
    while "  " in fullname:
        fullname = fullname.replace("  ", " ")
    fullname = fullname.split(" ")

    if len(fullname) == 3:
        new_learner[update.effective_chat.id].setFullname(fullname)

        btns = [
            [KeyboardButton(text="Мужской")],
            [KeyboardButton(text="Женский")]
        ]
        update.message.reply_text(text="Выберите пол ребенка:",
                                  reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
        return GENDER

    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(
            "Регистрация отменена", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    else:
        update.message.reply_text("Указанно неккоректное ФИО. Пожалуйста,введите ФИО ребенка полностью:")
