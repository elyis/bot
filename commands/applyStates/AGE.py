from mysql.connector import connect, Error
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from config_variable import categoriesSuitableForStudentByAge, ELECTIVE, new_learner, host, user, password, db


def showAvailableElectives(update: Update, context) -> int:
    age = 0
    print(update.effective_chat.id)
    if update.message.text.isdigit():
        age = int(update.message.text)
        new_learner.age = age
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
            ) as connection:
                selectElectivesOfCertainAgeCategory = f"SELECT name,reserve_places,init_age,final_age FROM Electives WHERE {age} BETWEEN init_age AND final_age"
                with connection.cursor() as cursor:
                    cursor.execute(selectElectivesOfCertainAgeCategory)
                    categoriesSuitableForStudentByAge.clear()
                    i = 0
                    for row in cursor.fetchall():
                        categoriesSuitableForStudentByAge.append(row[0])
                        places = getAvailablePlacesFromElective(i)
                        if places[0] == 0:
                            pass
                        else:
                            update.message.reply_text(
                                text=str(i + 1) + ":" + row[0] + ":\n"
                                                                 "Число резервных мест: " + str(row[1]) + "\n "
                                                                                                          "Возрастная категория: " + str(
                                    row[2]) + "-" + str(row[3]) + "\n" +
                                     "Свободных мест:" + str(places[0]) + "/" + str(places[1])
                            )
                        i += 1
        except Error as e:
            print(e)

        createBtnsOfElectives(update, context)
        return ELECTIVE

    else:
        update.message.reply_text(text="Указано не число")


# Возвращает кортеж (число свободных мест, максимальное число участников на направление)
def getAvailablePlacesFromElective(index: int) -> (int, int):
    freePlaces = 0
    busy_places = 0
    max_places = 0
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            selectMaxPlaces = f"SELECT total_seats FROM Electives WHERE name = '{categoriesSuitableForStudentByAge[index]}'"
            selectBusyPlaces = f"SELECT COUNT(*) FROM Learners " \
                               f"JOIN Electives " \
                               f"ON Learners.elective_id = Electives.id " \
                               f"WHERE Electives.name = '{categoriesSuitableForStudentByAge[index]}'"

            with connection.cursor() as cursor:
                cursor.execute(selectMaxPlaces)
                max_places = cursor.fetchall()[0][0]

                cursor.execute(selectBusyPlaces)
                busy_places = cursor.fetchall()[0][0]

    except Error as e:
        print(e)
    return (max_places - busy_places, max_places)


def createBtnsOfElectives(update: Update, context):
    if len(categoriesSuitableForStudentByAge) == 0:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="К сожалению, под ваш возраст не найден факультатив"
                                 )
        return ConversationHandler.END
    else:
        btns = [
            [KeyboardButton(text=str(i))] for i in range(1, len(categoriesSuitableForStudentByAge) + 1)
        ]
        reply_markup = ReplyKeyboardMarkup(btns, one_time_keyboard=True)
        update.message.reply_text(reply_markup=reply_markup, text="Факультативы доступные вам: ")

#1025910884
