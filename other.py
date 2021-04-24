# прочее
import main_csp
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode


def author(update, context):
    update.message.reply_text("Спасибо, что поинтересовался❣\nМне очень приятно💓\n\nВот мои контакты:\n@sofa_gans")
    con, cursor = main_csp.get_cursor()
    cursor.execute(f"INSERT INTO counters_and_marks(username) VALUES(?)", (update.message.chat.username,))
    con.commit()
    con.close()


def motivation(update, context):
    update.message.reply_text("В какой-то момент я захотела потренировать свои коммуникативные навыки, но, увы, нашла"
                              " такое приложение только на ОП Android, что меня очень расстроило, так как я обладаю"
                              " IOS.\nК тому же, я не нашла никаких ботов для развития тех же навыков, именно поэтому"
                              ", как говорил великий Линус Торвальдс, 'Пришлось пойти дальше и дизассемблировать "
                              "операционную систему'; в моем же случае: создать своего бота, которому я смогу "
                              "довериться и которого я смогу дополнять по своему вкусу🧜‍♀‍‍")
    print(update.message.chat.username, update.message.chat.first_name, update.message.chat.last_name)


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
    if int(query.data) == 1 or int(query.data) == 2:
        update.message.reply_text("обидно🤧")
    user = query.message.chat.id
    con, cursor = main_csp.get_cursor()
    check = cursor.execute(f"SELECT user_id FROM marks").fetchall()
    mark = cursor.execute(f"SELECT mark FROM marks WHERE user_id = '{user}' ").fetchone()
    users = [us[0] for us in check]
    if user in users:
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
        result = f'''INSERT INTO marks(user_id, username, name, mark) VALUES(?, ?, ?, ?)'''
        cursor.execute(result, (query.message.chat.id, query.message.chat.username,
                                query.message.chat.first_name + query.message.chat.last_name, int(query.data)))
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
