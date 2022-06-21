from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import NUMPHONE, new_learner


# Определение пола человека и запрос на ввод российского номера
def enterGender(update: Update, context):
    query = update.message.text
    if query.lower() in ("мужской", "м"):
        new_learner[update.effective_chat.id].gender = 0
        submitPhoneInputForm(update, context)
        return NUMPHONE

    elif query.lower() in ("женский", "ж"):
        new_learner[update.effective_chat.id].gender = 1
        submitPhoneInputForm(update, context)
        return NUMPHONE

    elif query.lower() == "/cancel":
        update.message.reply_text(
            "Регистрация отменена", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    else:
        update.message.reply_text(text="Указан неверный пол.Пожалуйста, введите мужской или женский")


def submitPhoneInputForm(update: Update, context):
    update.message.reply_text("Принято\nФорматы доступных номеров телефона:", reply_markup=ReplyKeyboardRemove())
    update.message.reply_text("+79261234567\n"
                              "89261234567\n"
                              "79261234567\n"
                              "+7 926 123 45 67\n"
                              "8(926)123-45-67\n"
                              "123-45-67\n"
                              "9261234567\n"
                              "79261234567\n"
                              "(495)1234567\n"
                              "(495) 123 45 67\n"
                              "89261234567\n"
                              "8-926-123-45-67\n"
                              "8 927 1234 234\n"
                              "8 927 12 12 888\n"
                              "8 927 12 555 12\n"
                              "8 927 123 8 123\n")
    update.message.reply_text("Введите номер телефона:")