from mysql.connector import connect, Error
categoriesSuitableForStudentByAge = list()

def showAgeCategoriesElectives(update,context):
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
                        for row in cursor.fetchall():
                            categoriesSuitableForStudentByAge.append(row[0])
                            context.bot.send_message(chat_id=update.effective_chat.id,
                                                     text=row[0] + ":\n"
                                                     "Число резервных мест: "+ str(row[1]) + "\n "
                                                     "Возрастная категория: " + str(row[2]) + "-" + str(row[3])
                                                     )
                    if len(categoriesSuitableForStudentByAge) == 0:
                        context.bot.send_message(chat_id=update.effective_chat.id,
                                                 text="К сожалению, под ваш возраст не найден факультатив"
                                                 )
            except Error as e:
                print(e)

        else:
            context.bot.send_message(chat_id=update.effective_chat.id,text="После команды указанны некорректные данные или неверный порядок аргументов")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="не указаны аргументы команды: команда число(возраст)")
