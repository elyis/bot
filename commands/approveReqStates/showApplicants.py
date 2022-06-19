from mysql.connector import connect, Error
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from config_variable import host, user, password, db, APPLICANTS_MENU

electivesIdName = list()
applicants = list()


def showApplicants(update: Update, context):
    gender = "мужской"
    electiveName = ""
    index = 1
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            countApplicants = 0
            selectCountApplicants = "SELECT COUNT(*) FROM Applicants"
            selectApplicants = "SELECT name,surname,patronymic,gender,phoneNum,elective_id FROM Applicants"
            selectElectives = "SELECT id,name FROM Electives"
            electivesIdName.clear()
            applicants.clear()

            with connection.cursor() as cursor:
                cursor.execute(selectCountApplicants)
                countApplicants = cursor.fetchall()[0][0]

                if countApplicants == 0:
                    update.message.reply_text(text="Поступающих нет")
                    return ConversationHandler.END

                else:
                    cursor.execute(selectElectives)
                    for row in cursor.fetchall():
                        electivesIdName.append((row[0], row[1]))

                    cursor.execute(selectApplicants)
                    for row in cursor.fetchall():
                        if row[3] == 1:
                            gender = "женский"

                        for elec in electivesIdName:
                            if row[5] == elec[0]:
                                electiveName = elec[1]
                        applicants.append((row[0], row[1], row[2], row[3], row[4], row[5]))

                        update.message.reply_text(text=f"{index}:ФИО:{row[0]} {row[1]} {row[2]}\n"
                                                       f"Пол: {gender}\n"
                                                       f"Номер телефона: {row[4]}\n"
                                                       f"Заявка подана на '{electiveName}'")
                        index += 1

    except Error as e:
        print(e)

    btns = [
        [KeyboardButton(text=str(j))] for j in range(1, len(applicants) + 1)
    ]
    update.message.reply_text(text="Выберите поступающего:",
                              reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
    return APPLICANTS_MENU
