# отзывы
import main_csp
from telegram import ReplyKeyboardMarkup, ParseMode


def reviews(update, context):
    update.message.reply_text("Вы хотите оставить или посмотреть отзывы?🙃",
                              reply_markup=ReplyKeyboardMarkup(main_csp.REVIEWS_MENU, resize_keyboard=True))


def set_review(update, context):
    update.message.reply_text("Чтобы оставить отзыв, отправь мне сообщение с ним.\n"
                              "*Формат должен быть такой:*\n_SG, <ваше сообщение>_\n\n"
                              "*Убедительная просьба:\nПожалуйста, не делайте красную строку (абзац)*",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup([["вернуться обратно"]], resize_keyboard=True))


def add_review_to_file_and_bd(update, context):
    update.message.reply_text("Спасибо за отзыв, он очень важен для меня🥰",
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
    rev = open("all_reviews.txt", "a", encoding="UTF-8")
    rev.write("\n" + update.message.text + "\n")
    rev.close()
    con, cursor = main_csp.get_cursor()
    result = f'''INSERT INTO reviews(user_id, username, name, review) VALUES(?, ?, ?, ?)'''
    cursor.execute(result, (update.message.chat.id, update.message.chat.username,
                            update.message.chat.first_name + update.message.chat.last_name, update.message.text))
    con.commit()
    con.close()


def get_reviews(bot, update):
    update.bot.send_document(bot.message.chat.id, open(r"all_reviews.txt", 'rb'))
    bot.message.reply_text("Спасибо за интерес❣",
                           reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
