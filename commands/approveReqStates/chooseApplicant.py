from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler

from commands.approveReqStates.showApplicants import applicants
from config_variable import ACCEPT_MENU
from config_variable import host, user, password, db

selectApplicant = tuple()

#Сохранение выбранного поступающего и меню выбора действия над ним
def chooseApplicant(update: Update, context):
    query = update.message.text
    if query.isdigit():
        if int(query) in range(1, len(applicants) + 1):

            global selectApplicant
            temp_list = list(selectApplicant)
            temp_list.clear()
            selectApplicant = tuple(temp_list)

            selectApplicant = selectApplicant + applicants[int(query) - 1]
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

    elif update.message.text.lower() == "/cancel":
        update.message.reply_text(
            "Команда отмененна", reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    else:
        update.message.reply_text(text="Введенно не число")


#Обработка действия над выбранным поступающим
def acceptMenu(update: Update, context):
    query = update.message.text
    electiveName = ""
    if query.lower() == "одобрить":
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
            ) as connection:
                selectElectiveName = f"select name FROM Electives WHERE id = {selectApplicant[5]}"
                deleteApplicant = f"DELETE FROM Applicants " \
                                  f"WHERE name = '{selectApplicant[0]}' AND " \
                                  f"surname = '{selectApplicant[1]}' AND " \
                                  f"patronymic = '{selectApplicant[2]}' AND " \
                                  f"gender = {selectApplicant[3]} AND " \
                                  f"phoneNum = '{selectApplicant[4]}' AND " \
                                  f"elective_id = {selectApplicant[5]} "

                insertLearner = f"INSERT INTO Learners(name,surname,patronymic,gender,phone_number,elective_id)" \
                                f"VALUES ('{selectApplicant[0]}'," \
                                f"'{selectApplicant[1]}'," \
                                f"'{selectApplicant[2]}'," \
                                f"{selectApplicant[3]}," \
                                f"'{selectApplicant[4]}'," \
                                f"{selectApplicant[5]})"
                with connection.cursor() as cursor:
                    cursor.execute(deleteApplicant)
                    cursor.execute(insertLearner)
                    cursor.execute(selectElectiveName)
                    electiveName = cursor.fetchall()[0][0]
                    connection.commit()
        except Error as e:
            print(e)

        update.message.reply_text(text="Заявка одобрена", reply_markup=ReplyKeyboardRemove())
        context.bot.send_message(chat_id=selectApplicant[6], text=f"Заявка принята для "
                                                                  f"{selectApplicant[0]} "
                                                                  f"{selectApplicant[1]} "
                                                                  f"{selectApplicant[2]} "
                                                                  f"на направление '{electiveName}'")

    elif query.lower() == "отклонить":
        try:
            with connect(
                    host=host,
                    user=user,
                    password=password,
                    database=db
            ) as connection:
                selectElectiveName = f"select name FROM Electives WHERE id = {selectApplicant[5]}"
                deleteApplicant = f"DELETE FROM Applicants " \
                                  f"WHERE name = '{selectApplicant[0]}' AND " \
                                  f"surname = '{selectApplicant[1]}' AND " \
                                  f"patronymic = '{selectApplicant[2]}' AND " \
                                  f"gender = {selectApplicant[3]} AND " \
                                  f"phoneNum = '{selectApplicant[4]}' AND " \
                                  f"elective_id = {selectApplicant[5]} "
                with connection.cursor() as cursor:
                    cursor.execute(deleteApplicant)
                    cursor.execute(selectElectiveName)
                    electiveName = cursor.fetchall()[0][0]
                    connection.commit()
        except Error as e:
            print(e)
        context.bot.send_message(chat_id=selectApplicant[6], text=f"Заявка отклонена для "
                                                                  f"{selectApplicant[0]} "
                                                                  f"{selectApplicant[1]} "
                                                                  f"{selectApplicant[2]} "
                                                                  f"на направление '{electiveName}'")
    return ConversationHandler.END
