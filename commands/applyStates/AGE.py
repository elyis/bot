from mysql.connector import connect, Error
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from classes import newLearners
from config_variable import categoriesSuitableForStudentByAge, ELECTIVE, new_learner, host, user, password, db


current_elective = ""


# Получает возраст ребенка и создает выборку факультетов под его возраст
def showAvailableElectives(update: Update, context) -> int:
    age = 0
    elective_id = 0
    if update.message.text.isdigit():
        new_learner[update.effective_chat.id] = newLearners()
        age = int(update.message.text)
        new_learner[update.effective_chat.id].age = age
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
            ) as connection:
                selectElectivesOfCertainAgeCategory = f"SELECT name,init_age,final_age, id,description " \
                                                      f"FROM Electives WHERE {age} " \
                                                      f"BETWEEN init_age AND final_age"

                with connection.cursor() as cursor:
                    cursor.execute(selectElectivesOfCertainAgeCategory)
                    categoriesSuitableForStudentByAge.clear()
                    i = 0
                    electives = cursor.fetchall()
                    for row in electives:
                        global current_elective
                        current_elective = row[0]
                        places = getAvailablePlacesFromElective()
                        if places[0] == 0:
                            pass
                        else:
                            categoriesSuitableForStudentByAge.append(row[0])
                            selectCountPeopleInLine = f"SELECT count(*) FROM Applicants WHERE elective_id = {row[3]}"
                            cursor.execute(selectCountPeopleInLine)
                            countPeopleInLine = cursor.fetchall()[0][0]
                            update.message.reply_text(
                                text=f"{str(i + 1)}:{row[0]}\n"
                                     f"Возрастная категория:  {str(row[1])} - {str(row[2])}\n"
                                     f"Свободных мест:  {str(places[0])}/{str(places[1])}\n"
                                     f"Число человек в очереди:  {countPeopleInLine}\n\n"
                                     f"Описание: {row[4]}"
                            )
                            i += 1
        except Error as e:
            print(e)

        if len(categoriesSuitableForStudentByAge) == 0:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="К сожалению, под ваш возраст не найден факультатив.\n Команда завершена"
                                     )
            return ConversationHandler.END

        else:
            btns = [
                [KeyboardButton(text=str(j))] for j in range(1, len(categoriesSuitableForStudentByAge) + 1)
            ]
            reply_markup = ReplyKeyboardMarkup(btns, one_time_keyboard=True)
            update.message.reply_text(reply_markup=reply_markup, text="Факультативы доступные вам: ")
        return ELECTIVE


    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(
            "Регистрация отменена", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    else:
        update.message.reply_text(text="Указано не число. Пожалуйста, введите число из доступных")


# Возвращает кортеж (число свободных мест, максимальное число участников на направление)
def getAvailablePlacesFromElective() -> (int, int):
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
            selectMaxPlaces = f"SELECT total_seats FROM Electives WHERE name = '{current_elective}'"
            selectBusyPlaces = f"SELECT COUNT(*) FROM Learners " \
                               f"JOIN Electives " \
                               f"ON Learners.elective_id = Electives.id " \
                               f"WHERE Electives.name = '{current_elective}'"

            with connection.cursor() as cursor:
                cursor.execute(selectMaxPlaces)
                max_places = cursor.fetchall()[0][0]

                cursor.execute(selectBusyPlaces)
                busy_places = cursor.fetchall()[0][0]

    except Error as e:
        print(e)
    return max_places - busy_places, max_places

# 1025910884
