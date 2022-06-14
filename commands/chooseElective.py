from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from commands.showAgeCategoriesElectives import categoriesSuitableForStudentByAge


# def build_menu(buttons, n_cols,
#                header_buttons=None,
#                footer_buttons=None):
#     menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
#     if header_buttons:
#         menu.insert(0, [header_buttons])
#     if footer_buttons:
#         menu.append([footer_buttons])
#     return menu

def chooseElective(update, context):
    if len(categoriesSuitableForStudentByAge) > 0:
        btns = [
            [InlineKeyboardButton(text=ss, callback_data=ss,url="http://itcube56.oksei.ru/") for ss in categoriesSuitableForStudentByAge]
        ]
        reply_markup = InlineKeyboardMarkup(btns)
        context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=reply_markup, text="Выберите факультатив:")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Пропишите команду: /showAgeCategories число(возраст обучающегося) и повторите /choose'")