from telegram import Update, ReplyKeyboardRemove

from config_variable import categoriesSuitableForStudentByAge, FULLNAME, new_learner


def saveSelectedElective(update: Update, context):
    query = update.message.text
    if query.isdigit():
        if int(query) in range(1, len(categoriesSuitableForStudentByAge) + 1):
            select_elective = categoriesSuitableForStudentByAge[int(query) - 1]
            new_learner.elective = categoriesSuitableForStudentByAge[int(query) - 1]
            update.message.reply_text("Введите ФИО ребенка полностью:", reply_markup=ReplyKeyboardRemove())
            return FULLNAME
        else:
            update.message.reply_text("Введено значение вне доступных категорий")
    else:
        update.message.reply_text("Введен текст, пожалуйста, введите число:")