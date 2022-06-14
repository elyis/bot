# бд
import logging
from mysql.connector import connect, Error
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from bot.Callbacks.chooseElectiveClb import chooseElectiveClb
from commands.chooseElective import chooseElective
from commands.showAgeCategoriesElectives import showAgeCategoriesElectives, categoriesSuitableForStudentByAge
from database.ElectivesDb import create_table_electives
from database.LearnersDb import create_table_learner
from static_data.Electives import inserts_electives

from init_database import init_database

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

if __name__ == "__main__":
    #init_database()
    updater.start_polling()
