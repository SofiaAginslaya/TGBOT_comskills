# для развития коммуникативных навыков
from telegram import ParseMode, ReplyKeyboardMarkup
import main_csp

global value
value = 0


def many_words(update, context):
    update.message.reply_text("Выберите часть речи:",
                              reply_markup=ReplyKeyboardMarkup(main_csp.PART_OF_SPEECH, resize_keyboard=True))


def goals_many_words(update, context):
    con, cursor = main_csp.get_cursor()
    global letter
    letter = "".join(update.message.text.split())
    print(letter)
    goal = cursor.execute(f"""
    SELECT goal, how_to_do, frequency FROM parts_of_speech WHERE part_of_sp = "{letter}" """).fetchone()
    update.message.reply_text("*Цель:* \n☑ _" + goal[0] + "_", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Как выполнять:* \n🆙" + goal[1], parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("🅰🅱🅾🅱🅰\nПовторяться нельзя❗\nПосле каждого сказанного слова нажмите на кнопку"
                              " на клавиатуре.\n⭕Данное упражнение отлично _вытягивает_ "
                              "слова из пассивного запаса⭕", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Частота выполнения:* \n♾♾♾♾♾♾♾♾\n" + goal[2] + "\n♾♾♾♾♾♾♾♾",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup([["начнем!"], ["🔙вернуться назад🔙"]],
                                                               resize_keyboard=True))
    con.close()


def set_timer_for_many_words(update, context):
    chat_id = update.message.chat_id
    due = 60  # засекаем минуту
    context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
    text = "*засекла минуту\n🟣Начинай произносить словА🟣"
    global updated
    updated = update
    update.message.reply_text(text,
                              reply_markup=ReplyKeyboardMarkup([["плюс"]],
                                                               resize_keyboard=True))


def task(context):
    text = "❗Минута прошлА❗\n*Цель:*\n✅_выполнена_✅"
    updated.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                               reply_markup=ReplyKeyboardMarkup([['🔙вернуться назад🔙']], resize_keyboard=True))
    res, text = know_result_many_words()
    updated.message.reply_text("*Поздравляю!*👇\n_Ваш результат:_ " + str(res), parse_mode=ParseMode.MARKDOWN)
    updated.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    con, cursor = main_csp.get_cursor()
    query = f'''INSERT INTO counters_and_marks({letter}) VALUES(?)'''
    cursor.execute(query, (res,))
    con.commit()
    con.close()


def plus_one(update, context):
    global value
    value += 1


def know_result_many_words():
    con, cursor = main_csp.get_cursor()
    result = cursor.execute(f"SELECT {letter} FROM counters_and_marks").fetchall()
    summa, kolvo = main_csp.counter_comparison(result)
    con.close()
    if value < (summa / kolvo):
        return value,\
               "Вы сказали меньше слов, чем говорят в среднем. Но я уверена, это _неокончательный результат_!!!💜"
    else:
        return value,  "Вы сказали больше слов, чем говорят в среднем. Мои поздравления! _Дальше - больше_💜"


def be_back_to_the_menu_many_words(update, context):
    update.message.reply_text("Вы вернулись назад:",
                              reply_markup=ReplyKeyboardMarkup(main_csp.MENU_MANY_WORDS, resize_keyboard=True))
    global value
    value = 0
