from mysql.connector import connect, Error
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import CHOOSE_RM, host, user, password, db

electives = list()
learners = list()
select_el = ""

#Список всех факультативов с клавиатурой выборки
def rmMenu(update: Update, context):
    i = 0
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            selectNamesElectives = f"SELECT name FROM Electives"
            electives.clear()
            with connection.cursor() as cursor:
                cursor.execute(selectNamesElectives)
                for row in cursor.fetchall():
                    electives.append(row[0])
                    update.message.reply_text(text=f"{str(i + 1)}: {row[0]}")
                    i += 1

    except Error as e:
        print(e)

    btns = [
        [KeyboardButton(text=str(j))] for j in range(1, len(electives) + 1)
    ]

    update.message.reply_text("Выберите факультатив:",
                              reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))

    return CHOOSE_RM

