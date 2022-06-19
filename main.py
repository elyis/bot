# бд
import logging

from classes import newLearners
from commands.applyStates.AGE import showAvailableElectives
from commands.applyStates.ELECTIVE import saveSelectedElective
from commands.applyStates.FULLNAME import enterFullName
from commands.applyStates.GENDER import enterGender
from commands.applyStates.NUMPHONE import enterPhoneNum
from commands.applyStates.RESULT import showResultRegistration
from commands.applyStates.apply import apply
from commands.applyStates.cancel import cancel
from commands.approveReqStates.chooseApplicant import chooseApplicant, acceptMenu
from commands.approveReqStates.showApplicants import showApplicants
from commands.removeStates.choose_rm import chooseRm
from commands.removeStates.distibutor import distibutor
from commands.removeStates.removeMenu import rmMenu
from commands.removeStates.remove_elective import removeElective
from commands.removeStates.remove_more import removeMore
from config_variable import TOKEN, AGE, ELECTIVE, FULLNAME, NUMPHONE, RESULT, GENDER, CHOOSE_RM, DISTRIBUTOR, \
    REMOVE_MORE, REMOVE_ELECTIVE, ACCEPT_MENU, APPLICANTS_MENU

# telegram bot
from telegram.ext import Updater, ConversationHandler, MessageHandler, Filters
from telegram.ext import CommandHandler

from init_database import init_database

init_database()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

apply_hand = ConversationHandler(
    entry_points=[CommandHandler("apply", apply)],
    states={
        AGE: [MessageHandler(Filters.text, showAvailableElectives)],
        ELECTIVE: [MessageHandler(Filters.text, saveSelectedElective)],
        FULLNAME: [MessageHandler(Filters.regex(r"(([А-Яа-я]){2,}([-]?([А-Яа-я]){2,})?([ ])+){2}([А-Яа-я]){2,}"),
                                  enterFullName)],
        GENDER: [MessageHandler(Filters.text, enterGender)],
        NUMPHONE: [
            MessageHandler(Filters.regex(r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"), enterPhoneNum)],
        RESULT: [MessageHandler(Filters.text, showResultRegistration)]

    },
    fallbacks=[CommandHandler("cancel", cancel)],
    allow_reentry=True
)

rm_hand = ConversationHandler(
    entry_points=[CommandHandler("rm", rmMenu)],
    states={
        CHOOSE_RM: [MessageHandler(Filters.text, chooseRm)],
        DISTRIBUTOR: [MessageHandler(Filters.text, distibutor)],
        REMOVE_MORE: [MessageHandler(Filters.text, removeMore)],
        REMOVE_ELECTIVE: [MessageHandler(Filters.text, removeElective)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

approve_request_hand = ConversationHandler(
    entry_points=[CommandHandler("approve_req", showApplicants)],
    states={
        APPLICANTS_MENU: [MessageHandler(Filters.text, chooseApplicant)],
        ACCEPT_MENU: [MessageHandler(Filters.text, acceptMenu)]
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)

dispatcher.add_handler(apply_hand)
dispatcher.add_handler(rm_hand)
dispatcher.add_handler(approve_request_hand)

if __name__ == "__main__":
    updater.start_polling()
