# бд
import logging
from mysql.connector import connect, Error
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from Callbacks import chooseElectiveClb
from commands.chooseElective import chooseElective
from commands.showAgeCategoriesElectives import showAgeCategoriesElectives, categoriesSuitableForStudentByAge
from database.ElectivesDb import create_table_electives
from database.LearnersDb import create_table_learner
from static_data.Electives import inserts_electives

# telegram bot
from telegram.ext import Updater, CallbackQueryHandler
from telegram.ext import CommandHandler

TOKEN = '5378657511:AAGBXSLkAZA-AJFD6tp78PLiMfIx1Hfc5MY'
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

showAgeCategoriesElectives_handler = CommandHandler('showAgeCategories', showAgeCategoriesElectives)
dispatcher.add_handler(showAgeCategoriesElectives_handler)

start_handler = CommandHandler('choose', chooseElective)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(CallbackQueryHandler(chooseElectiveClb))

# def chooseAnElective(update, context):
#     print(categoriesSuitableForStudentByAge)
#     btn = KeyboardButton("hi")
#     markup = ReplyKeyboardMarkup([btn])
#     print("work")
#     print("work2")
#     # btns = list()
#     #
#     # for i in range(len(categoriesSuitableForStudentByAge)):
#     #     btns.append(KeyboardButton(categoriesSuitableForStudentByAge[i]))
#     #
#     # markup.add(btns)
#     print("work3")
#     context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=markup)
#
#
# chooseAnElective_handler = CommandHandler('choose', chooseAnElective)
# dispatcher.add_handler(chooseAnElective_handler)

# try:
#     with connect(
#         host="localhost",
#         user=input("Имя пользователя: "),
#         password=getpass("Пароль: "),
#         database="it_cub"
#     ) as connection:
#
#         with connection.cursor() as cursor:
#             cursor.execute(create_table_electives)
#             cursor.execute(create_table_learner)
#             cursor.execute(inserts_electives)
#             connection.commit()
#             connection.close()
# except Error as e:
#     print(e)

if __name__ == "__main__":
    updater.start_polling()
