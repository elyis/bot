from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import host, user, password, db, new_elective


def addElective(update: Update, context):
    query = update.message.text
    if query.lower() == "добавить":
        update.message.reply_text(text="Выбрано: добавить",
                                  reply_markup=ReplyKeyboardRemove())

        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
            ) as connection:
                insertElective = f"INSERT INTO Electives(name,description,init_age,final_age,total_seats)" \
                                 f"values" \
                                 f"('{new_elective.name}','{new_elective.description}', " \
                                 f"{new_elective.init_age}, {new_elective.final_age}," \
                                 f"{new_elective.total_seats})"
                with connection.cursor() as cursor:
                    cursor.execute(insertElective)
                    connection.commit()
        except Error as e:
            print(e)
        return ConversationHandler.END

    elif query.lower() == "отклонить":
        update.message.reply_text(text="Выбрано: отклонение",
                                  reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    elif query.lower() == "/cancel":
        update.message.reply_text("Команда отменена", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    else:
        update.message.reply_text(text="Неизвестная команда, пожалуйста воспользуйтесь вспомогательной клавиатурой")
