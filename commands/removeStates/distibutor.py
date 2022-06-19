from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from commands.removeStates.removeMenu import rmMenu, select_el, learners
from commands.removeStates.remove_elective import removeElective
from config_variable import REMOVE_MORE, CHOOSE_RM, host, user, password, db


def distibutor(update: Update, context):
    query = update.message.text

    if query.lower() == "удалить учащегося":
        update.message.reply_text(reply_markup=ReplyKeyboardRemove(), text="Выбранно: удаление учащегося")
        if showLearner(update, context):
            return REMOVE_MORE
        else:
            rmMenu(update, context)
            return CHOOSE_RM

    elif query.lower() == "выбрать электив":
        if rmMenu(update, context) == CHOOSE_RM:
            return CHOOSE_RM

    elif query.lower() == "удалить электив":
        removeElective(update, context)
        return CHOOSE_RM
    else:
        update.message.reply_text(text="Удаление завершенно", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END


def showLearner(update: Update, context):
    i = 0
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            selectLearners = f"SELECT Learners.name,surname,patronymic,phone_number " \
                             f"FROM Learners JOIN Electives " \
                             f"ON Electives.id = Learners.elective_id " \
                             f"WHERE Electives.name = '{select_el}'"
            selectCountLearners = f"SELECT count(*)" \
                                  f"FROM Learners JOIN Electives " \
                                  f"ON Electives.id = Learners.elective_id " \
                                  f"WHERE Electives.name = '{select_el}'"

            learners.clear()
            with connection.cursor() as cursor:
                cursor.execute(selectCountLearners)
                count = cursor.fetchall()[0][0]
                if count == 0:
                    update.message.reply_text("В данном элективе нет обучающихся",
                                              reply_markup=ReplyKeyboardRemove())
                    return False
                else:
                    cursor.execute(selectLearners)
                    for row in cursor.fetchall():
                        update.message.reply_text(f"{i + 1}: {row[0]} {row[1]} {row[2]} {row[3]}")
                        learners.append(f"{row[0]} {row[1]} {row[2]} {row[3]}")
                        i += 1

    except Error as e:
        print(e)
    btns = [
        [KeyboardButton(text=str(j))] for j in range(1, len(learners) + 1)
    ]

    update.message.reply_text("Учащиеся этого электива:",
                              reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
    return True