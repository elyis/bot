from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

from commands.removeStates.removeMenu import electives, learners
from config_variable import DISTRIBUTOR, host, user, password, db


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
                print(count)
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
