from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

from commands.removeStates.removeMenu import electives
from config_variable import DISTRIBUTOR


def chooseRm(update: Update, context):
    query = update.message.text
    if query.isdigit():
        if int(query) in range(1, len(electives) + 1):
            global select_el
            select_el = electives[int(query) - 1]
            update.message.reply_text(reply_markup=ReplyKeyboardRemove(), text=f"Выбран: {select_el}")

            btns = [
                [KeyboardButton(text="Удалить учащегося")],
                [KeyboardButton(text="Удалить электив")],
                [KeyboardButton(text="Выбрать электив")],
                [KeyboardButton(text="Завершить удаление")]
            ]

            update.message.reply_text(text="Выберите действие:",
                                      reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
            return DISTRIBUTOR

        else:
            update.message.reply_text(text="Число не относится к номерам элективов")
    else:
        update.message.reply_text(text="Введено не число")