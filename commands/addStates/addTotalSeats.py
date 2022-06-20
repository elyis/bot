from telegram import Update, KeyboardButton, ReplyKeyboardMarkup

from config_variable import new_elective, ADD_ELECTIVE


def addTotalSeats(update: Update, context):
    query = update.message.text
    if query.isdigit():
        new_elective.total_seats = int(query)

        btns = [
            [KeyboardButton(text="Добавить")],
            [KeyboardButton(text="Отменить")]
        ]
        update.message.reply_text(text=f"Добавить электив?\n"
                                       f"Наименование: {new_elective.name}\n"
                                       f"Описание: {new_elective.description}\n"
                                       f"Возрастная категория: {new_elective.init_age} - {new_elective.final_age}\n"
                                       f"Число мест: {new_elective.total_seats}",
                                  reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
        return ADD_ELECTIVE
    else:
        update.message.reply_text("Введено не число, возможно имеются лишние пробелы")
