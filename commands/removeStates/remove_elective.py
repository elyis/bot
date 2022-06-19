from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove

from commands.removeStates.removeMenu import select_el, rmMenu
from config_variable import host, user, password, db


def removeElective(update: Update, context):
    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            electiveId = 0
            selectElectiveId = f"SELECT id FROM Electives WHERE name = '{select_el}'"
            with connection.cursor() as cursor:
                cursor.execute(selectElectiveId)

                electiveId = cursor.fetchall()[0][0]
                deleteLearners = f"DELETE FROM Learners WHERE elective_id = {electiveId}"
                deleteApplicant = f"DELETE FROM Applicants WHERE elective_id = {electiveId}"
                deleteElective = f"DELETE FROM Electives WHERE id = {electiveId}"

                cursor.execute(deleteLearners)
                cursor.execute(deleteApplicant)
                cursor.execute(deleteElective)
                connection.commit()

    except Error as e:
        print(e)

    update.message.reply_text(text="Электив удален", reply_markup=ReplyKeyboardRemove())

    rmMenu(update, context)