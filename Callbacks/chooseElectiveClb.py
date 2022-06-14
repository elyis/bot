def chooseElectiveClb(update, context):
    query = update.callback_query
    answer = query.data

    query.answer()
    query.edit_message_text(text=f"Выбранный вариант: {answer}")