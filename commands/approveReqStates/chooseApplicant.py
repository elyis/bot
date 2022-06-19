from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup

from commands.approveReqStates.showApplicants import applicants
from config_variable import ACCEPT_MENU
from config_variable import host, user, password, db

selectApplicant = tuple()
isSelect = False


def chooseApplicant(update: Update, context):
    query = update.message.text
    if query.isdigit():
        if int(query) in range(1, len(applicants) + 1):
            global selectApplicant
            selectApplicant = selectApplicant + applicants[int(query) - 1]
            global isSelect
            isSelect = True
            print(selectApplicant)
            update.message.reply_text(text=f"Выбран: {selectApplicant[0]} {selectApplicant[1]} {selectApplicant[2]}",
                                      reply_markup=ReplyKeyboardRemove())

            btns = [
                [KeyboardButton(text="Одобрить")],
                [KeyboardButton(text="Отклонить")],
                [KeyboardButton(text="Завершить")]
            ]
            update.message.reply_text(text="Отклонить или одобрить заявку?",
                                      reply_markup=ReplyKeyboardMarkup(btns, one_time_keyboard=True))
            return ACCEPT_MENU
        else:
            update.message.reply_text(text="Число вне диапазона")

    else:
        update.message.reply_text(text="Введенно не число")


def acceptMenu(update: Update, context):
    query = update.message.text
    print(selectApplicant)
    if isSelect:
        if query.lower() == "одобрить":
            try:
                with connect(
                        host=host,
                        user=user,
                        password=password,
                        database=db
                ) as connection:
                    deleteApplicant = f"DELETE FROM Applicants " \
                                      f"WHERE name = '{selectApplicant[0]}' AND " \
                                      f"surname = '{selectApplicant[1]}' AND " \
                                      f"patronymic = '{selectApplicant[2]}' AND " \
                                      f"gender = {selectApplicant[3]} AND " \
                                      f"phoneNum = '{selectApplicant[4]}' AND " \
                                      f"elective_id = {selectApplicant[5]} "
                    print(deleteApplicant)
                    insertLearner = f"INSERT INTO Learners(name,surname,patronymic,gender,phone_number,elective_id)" \
                                    f"VALUES ('{selectApplicant[0]}'," \
                                    f"'{selectApplicant[1]}'," \
                                    f"'{selectApplicant[2]}'," \
                                    f"1," \
                                    f"'{selectApplicant[4]}'," \
                                    f"{selectApplicant[5]})"
                    with connection.cursor() as cursor:
                        cursor.execute(deleteApplicant)
                        cursor.execute(insertLearner)
                        connection.commit()
            except Error as e:
                print(e)