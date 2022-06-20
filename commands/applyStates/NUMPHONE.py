from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

from config_variable import RESULT, new_learner


# Подтверждение телефона и запрос на показ конечной формы
def enterPhoneNum(update: Update, context):
    new_learner[update.effective_chat.id].phoneNum = update.message.text
    update.message.reply_text("Номер принят")

    btns = [
        [KeyboardButton(text="Да")],
        [KeyboardButton(text="Нет")]
    ]

    update.message.reply_text(text="Показать заполненную заявку?",
                              reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
    return RESULT
