# communication skills progress
from telegram import ParseMode
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN
import sqlite3


MAIN_MENU = [["все упражнения"], ["оценить приложение"], ["автор проекта", "мотивация"]]
MENU_MANY_WORDS = [["для увеличения словарного запаса"], ["для развития дикции"],
                   ["для развития коммуникабельности"], ["вернуться в главное меню"]]
PART_OF_SPEECH = [["имена\nсуществительные", "имена\nприлагательные"], ["глаголы"],
                  ["вернуться назад", "позвать Sofia"]]


def start(update, context):
    update.message.reply_text(
        "Привет!👋 Я твой бот-помощник по развитию коммуникативных навыков.\n\nМожешь называть меня Sofia! :)",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, one_time_keyboard=False, resize_keyboard=True))


def sofia(update, context):
    update.message.reply_text("Я тут! Чем могу тебе помочь?)",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def all_ex(update, context):
    update.message.reply_text("Выберете тип упражнений:",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))
    global value
    value = 0


def many_words(update, context):
    update.message.reply_text("Выберете, над какой частью речи Вы хотите поиздеваться)) :",
                              reply_markup=ReplyKeyboardMarkup(PART_OF_SPEECH, resize_keyboard=True))


def goals_many_words(update, context):
    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    global letter
    letter = "".join(update.message.text.split())
    print(letter)
    goal = cursor.execute(f"""
    SELECT goal, how_to_do, frequency FROM parts_of_speech WHERE part_of_sp = "{letter}" """).fetchone()
    update.message.reply_text("*Цель:* \n☑ _" + goal[0] + "_", parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup([["начать", "вернуться назад"]],
                                                               resize_keyboard=True))
    update.message.reply_text("*Как выполнять:* \n🆙" + goal[1], parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("🅰🅱🅾🅱🅰\nПовторяться нельзя❗\nПосле каждого сказанного слова нажмите на кнопку"
                              " на клавиатуре.\n⭕Данное упражнение отлично _вытягивает_ "
                              "слова из пассивного запаса⭕", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Частота выполнения:* \n♾♾♾♾♾\n" + goal[2] + "\n♾♾♾♾♾", parse_mode=ParseMode.MARKDOWN)
    con.close()


def set_timer_for_many_words(update, context):
    chat_id = update.message.chat_id
    due = 60  # засекаем минуту
    context.job_queue.run_once(task, due, context=chat_id, name=str(chat_id))
    text = "*засекла минуту\n🟣Начинай произносить словА🟣"
    global updated
    updated = update
    update.message.reply_text(text,
                              reply_markup=ReplyKeyboardMarkup([['слово+']],
                                                               resize_keyboard=True))


def task(context):
    text = "❗Минута прошлА❗\n*Цель:*\n✅_выполнена_✅"
    updated.message.reply_text(text, parse_mode=ParseMode.MARKDOWN,
                               reply_markup=ReplyKeyboardMarkup([['вернуться назад']], resize_keyboard=True))
    res, text = know_result_many_words()
    updated.message.reply_text("*Поздравляю!*👇\n_Твой результат:_ " + str(res), parse_mode=ParseMode.MARKDOWN)
    updated.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    query = f'''INSERT INTO counters_and_marks({letter}) VALUES(?)'''
    cursor.execute(query, (res,))
    con.commit()
    con.close()


def plus_one(update, context):
    global value
    value += 1


def know_result_many_words():
    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    result = cursor.execute(f"SELECT {letter} FROM counters_and_marks").fetchall()
    summa, kolvo = 0, 0
    for i in result:
        if i[0] != None:
            summa += int(i[0])
            kolvo += 1
    if value < (summa / kolvo):
        return value,\
               "Ты сказал меньше слов, чем говорят в среднем. Но я уверена, это _*не* окончательный результат_!!!💜"
    else:
        return value,  "Ты сказал больше слов, чем говорят в среднем. Мои поздравления! _Дальше - больше_💜"
    con.close()


def be_back_to_the_main_menu(update, context):
    update.message.reply_text("Вы вернулись в главное меню:",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def be_back_to_the_menu_many_words(update, context):
    update.message.reply_text("Вы вернулись назад.",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))
    global value
    value = 0


def main():
    updater = Updater(TG_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("начнем!"), start))
    dp.add_handler(CommandHandler("Sofia", sofia))
    dp.add_handler(MessageHandler(Filters.regex("Sofia"), sofia))

    dp.add_handler(CommandHandler("all_ex", all_ex))
    dp.add_handler(MessageHandler(Filters.regex("все упражнения"), all_ex))
    dp.add_handler(CommandHandler("many_words", many_words))
    dp.add_handler(MessageHandler(Filters.regex("словарного запаса"), many_words))
    dp.add_handler(CommandHandler("noun", goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nсуществительные"), goals_many_words))
    dp.add_handler(CommandHandler("adjs", goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nприлагательные"), goals_many_words))
    dp.add_handler(CommandHandler("verbs", goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("глаголы"), goals_many_words))
    dp.add_handler(CommandHandler("timer_for_many_words", set_timer_for_many_words))
    dp.add_handler(MessageHandler(Filters.regex("начать"), set_timer_for_many_words))
    dp.add_handler(MessageHandler(Filters.regex("слово+"), plus_one))

    dp.add_handler(CommandHandler("be_back_mm", be_back_to_the_main_menu))
    dp.add_handler(MessageHandler(Filters.regex("вернуться в главное меню"), be_back_to_the_main_menu))
    dp.add_handler(CommandHandler("be_back", be_back_to_the_menu_many_words))
    dp.add_handler(MessageHandler(Filters.regex("вернуться назад"), be_back_to_the_menu_many_words))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
