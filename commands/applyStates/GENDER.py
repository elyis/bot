from telegram import Update, ReplyKeyboardRemove

from config_variable import NUMPHONE, new_learner


# Определение пола человека и запрос на ввод российского номера
def enterGender(update: Update, context):
    if update.message.text.lower() in ("мужской", "м"):
        new_learner[update.effective_chat.id].gender = 0
    else:
        new_learner[update.effective_chat.id].gender = 1

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
    return NUMPHONE
