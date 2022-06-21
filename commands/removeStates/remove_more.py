from mysql.connector import connect, Error
from telegram import Update, KeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from config_variable import host, user, password, db, DISTRIBUTOR, learners


# Удаление выбранного учащегося из электива
def removeMore(update: Update, context):
    query = update.message.text
    if query.isdigit():
        if int(query) in range(1, len(learners) + 1):

            try:
                with connect(
                        host=host,
                        user=user,
                        password=password,
                        database=db
                ) as connection:
                    result = learners[int(query) - 1].split(" ")
                    deleteLearner = f"DELETE FROM Learners " \
                                    f"WHERE name = '{result[0]}' and surname = '{result[1]}' and " \
                                    f"patronymic = '{result[2]}' and phone_number = '{result[3]}'"

                    with connection.cursor() as cursor:
                        cursor.execute(deleteLearner)
                        connection.commit()

            except Error as e:
                print(e)

            update.message.reply_text(text="Удалить еще человека?", reply_markup=ReplyKeyboardRemove())

            btns = [
                [KeyboardButton(text="Удалить учащегося")],
                [KeyboardButton(text="Удалить электив")],
                [KeyboardButton(text="Выбрать электив")],
                [KeyboardButton(text="Завершить удаление")]
            ]

            update.message.reply_text("Выберите действие:",
                                      reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
            return DISTRIBUTOR
        else:
            update.message.reply_text(text="Число не является индексом ученика. Пожалуйста, введите индекс ученика")

    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(text="Действие отменено", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    else:
        update.message.reply_text(text="Введено не число. Пожалуйста, введите индекс ученика")