from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

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
    else:
        update.message.reply_text("Указанно неккоректное ФИО. Пожалуйста,введите ФИО ребенка полностью:")
