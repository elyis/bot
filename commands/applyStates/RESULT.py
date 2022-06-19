from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import new_learner, admin_id, host, user, password, db


def showResultRegistration(update: Update, context):
    if update.message.text.lower() == "да":
        update.message.reply_text(new_learner.surname + " " + new_learner.name + " " + new_learner.patronymic + " " +
                                  str(new_learner.age) + " лет\nТелефон: " +
                                  new_learner.phoneNum + "\nПодает заявку на " +
                                  f"'{new_learner.elective}'")

    context.bot.send_message(chat_id=admin_id,
                             text=new_learner.surname + " " + new_learner.name + " " + new_learner.patronymic + " " +
                                  str(new_learner.age) + " лет\nТелефон: " +
                                  new_learner.phoneNum + "\nПодает заявку на " +
                                  f"'{new_learner.elective}'")
    update.message.reply_text("Заявка отправленна", reply_markup=ReplyKeyboardRemove())

    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            selectElectiveId = f"SELECT id FROM Electives WHERE name = '{new_learner.elective}'"
            electiveId = 0
            with connection.cursor() as cursor:
                cursor.execute(selectElectiveId)
                electiveId = cursor.fetchall()[0][0]

                insertLearner = f"INSERT INTO Applicants(name,surname,patronymic,gender,phoneNum,elective_id)" \
                                f"values ('{new_learner.name}','{new_learner.surname}','{new_learner.patronymic}'," \
                                f"{new_learner.gender},'{new_learner.phoneNum}',{electiveId})"

                cursor.execute(insertLearner)
                connection.commit()

    except Error as e:
        print(e)

    return ConversationHandler.END
