from mysql.connector import connect, Error
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from config_variable import new_learner, admin_id, host, user, password, db


# Отображение введеных данных и занесение в базу поступающих
def showResultRegistration(update: Update, context):
    chat_id = update.effective_chat.id
    if update.message.text.lower() == "да":
        update.message.reply_text(new_learner[chat_id].surname + " " +
                                  new_learner[chat_id].name + " " +
                                  new_learner[chat_id].patronymic + " " +
                                  str(new_learner[chat_id].age) + " лет\nТелефон: " +
                                  new_learner[chat_id].phoneNum + "\nПодает заявку на " +
                                  f"'{new_learner[chat_id].elective}'")

    context.bot.send_message(chat_id=admin_id,
                             text=new_learner[chat_id].surname + " " + new_learner[chat_id].name + " " + new_learner[chat_id].patronymic + " " +
                                  str(new_learner[chat_id].age) + " лет\nТелефон: " +
                                  new_learner[chat_id].phoneNum + "\nПодает заявку на " +
                                  f"'{new_learner[chat_id].elective}'")
    update.message.reply_text("Заявка отправленна, вам придет уведомление в чат", reply_markup=ReplyKeyboardRemove())

    try:
        with connect(
                host=host,
                user=user,
                password=password,
                database=db
        ) as connection:
            selectElectiveId = f"SELECT id FROM Electives WHERE name = '{new_learner[chat_id].elective}'"
            electiveId = 0
            with connection.cursor() as cursor:
                cursor.execute(selectElectiveId)
                electiveId = cursor.fetchall()[0][0]

                insertLearner = f"INSERT INTO " \
                                f"Applicants(name,surname,patronymic,gender,chatId,phoneNum,age,elective_id)" \
                                f"values " \
                                f"('{new_learner[chat_id].name}'," \
                                f"'{new_learner[chat_id].surname}'," \
                                f"'{new_learner[chat_id].patronymic}'," \
                                f"{new_learner[chat_id].gender}," \
                                f"{chat_id}," \
                                f"'{new_learner[chat_id].phoneNum}'" \
                                f",{new_learner[chat_id].age}," \
                                f"{electiveId})"

                cursor.execute(insertLearner)
                connection.commit()


    except Error as e:
        print(e)
    new_learner.pop(chat_id)
    return ConversationHandler.END
