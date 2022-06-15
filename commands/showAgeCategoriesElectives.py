from mysql.connector import connect, Error

categoriesSuitableForStudentByAge = list()


def showAgeCategoriesElectives(update, context):
    age = 0
    if context.args:
        if context.args[0].isdigit():
            age = int(context.args[0])

            try:
                with connect(
                        host="localhost",
                        user="root",
                        password="root",
                        database="it_cub"
                ) as connection:
                    selectElectivesOfCertainAgeCategory = f"SELECT name,reserve_places,init_age,final_age FROM Electives WHERE {age} BETWEEN init_age AND final_age"
                    # f"FROM Electives" \
                    # f"WHERE {age} BETWEEN init_age AND final_age "
                    with connection.cursor() as cursor:
                        cursor.execute(selectElectivesOfCertainAgeCategory)
                        categoriesSuitableForStudentByAge.clear()
                        i = 0
                        for row in cursor.fetchall():
                            categoriesSuitableForStudentByAge.append(row[0])
                            places = numOfPlaces(i)
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=row[0] + ":\n"
                                                    "Число резервных мест: " + str(row[1]) + "\n "
                                                    "Возрастная категория: " + str(row[2]) + "-" + str(row[3]) + "\n" +
                                                    "Свободных мест:" + str(places[0]) + "/" + str(places[1])
                                                     )
                            i += 1
                    if len(categoriesSuitableForStudentByAge) == 0:
                        context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text="К сожалению, под ваш возраст не найден факультатив"
                                                 )
            except Error as e:
                print(e)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="После команды указанны некорректные данные или неверный порядок аргументов")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="не указаны аргументы команды: команда число(возраст)")


# Возвращает кортеж (число свободных мест, максимальное число участников на направление)
def numOfPlaces(index: int):
    freePlaces = 0
    busy_places = 0
    max_places = 0
    try:
        with connect(
                host="localhost",
                user="root",
                password="root",
                database="it_cub"
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
