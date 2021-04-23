# прочее
import main_csp
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode


def mark(update, context):
    update.message.reply_text("Вы хотите поставить/изменить оценку боту или узнать рейтинг?🙃",
                              reply_markup=ReplyKeyboardMarkup(main_csp.MARK_MENU,
                                                               resize_keyboard=True))


def set_mark(bot, update):
    mark_keyboard = [[InlineKeyboardButton("отлично", callback_data='5'),
                      InlineKeyboardButton("хорошо", callback_data='4')],
                     [InlineKeyboardButton("удовлетворительно", callback_data='3')],
                     [InlineKeyboardButton("плохо", callback_data='2'),
                      InlineKeyboardButton("ужасно", callback_data='1')]]
    con, cursor = main_csp.get_cursor()
    result = cursor.execute("SELECT file_id FROM names_of_pic WHERE name = 'kitten_gif' ").fetchone()
    # в бд находится уже готовый id гифки, чтобы 1)не загружать в телеграм заново одно и то же;
    # 2) программа не тормозила
    con.close()
    update.bot.send_animation(
        chat_id=bot.message.chat.id,
        animation=result[0],
        reply_markup=InlineKeyboardMarkup(mark_keyboard))


def change_mark(bot, update):
    con, cursor = main_csp.get_cursor()
    user = bot.message.chat.id
    query = f"DELETE FROM marks WHERE user_id = '{user}' "
    cursor.execute(query)
    con.commit()
    con.close()
    bot.message.reply_text("Оценка удалена! Поставьте оценку заново:")
    set_mark(bot, update)


def add_mark_to_bd(bot, update):
    query = bot.callback_query
    user = query.message.chat.id
    con, cursor = main_csp.get_cursor()
    check = cursor.execute(f"SELECT user_id FROM marks").fetchall()
    mark = cursor.execute(f"SELECT mark FROM marks WHERE user_id = '{user}' ").fetchone()
    if user in check[0]:
        update.bot.edit_message_caption(
            caption=f"Вы уже ставили оценку! Ваша оценка: {mark[0]}",
            chat_id=user,
            message_id=query.message.message_id
        )
    else:
        update.bot.edit_message_caption(
            caption="Спасибо за оценку! Этим вы помогаете мне понять, достаточно ли я хороша💞",
            chat_id=user,
            message_id=query.message.message_id
        )
        result = f'''INSERT INTO marks(user_id, mark) VALUES(?, ?)'''
        cursor.execute(result, (query.message.chat.id, int(query.data)))
        con.commit()
        con.close()


def get_rating(update, context):
    con, cursor = main_csp.get_cursor()
    result = cursor.execute(f"SELECT mark FROM marks").fetchall()
    summa, kolvo = main_csp.counter_comparison(result)
    update.message.reply_text("*🙊Рейтинг бота:*\n_👉" + str(summa / kolvo) + " / 5👈_\n\nКажется, я не так плоха💌",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
    con.close()


def be_back_other(update, context):
    update.message.reply_text("Вы вернулись обратно. Сделайте свой выбор:",
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
