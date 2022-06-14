from telegram import InlineKeyboardButton, InlineKeyboardMarkup

selected_elective = ""

def chooseElectiveClb(update, context):
    query = update.callback_query
    answer = query.data
    query.answer()

    selected_elective = answer
    query.edit_message_text(text=f"Выбран факультатив: {answer}")


