# прочее
import sqlite3
import main_csp
from telegram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode


def mark(update, context):
    update.message.reply_text("Вы хотите поставить оценку боту или узнать рейтинг?🙃",
                              reply_markup=ReplyKeyboardMarkup([["поставить оценку", "узнать рейтинг"],
                                                                ["вернуться обратно"]], resize_keyboard=True))


def set_mark(update, context):
    update.message.reply_text("Опишите работоспособность бота, нажав на одну из кнопок:",
                              reply_markup=ReplyKeyboardMarkup([["1", "2", "3", "4", "5"], ["вернуться обратно"]],
                                                               resize_keyboard=True))


def add_mark_to_bd(update, context):
    update.message.reply_text("Спасибо за оценку! Этим ты помогаешь мне понять, достаточно ли я хороша💞",
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    query = f'''INSERT INTO counters_and_marks(mark) VALUES(?)'''
    cursor.execute(query, (update.message.text,))
    con.commit()
    con.close()


def know_mark(update, context):
    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    result = cursor.execute(f"SELECT mark FROM counters_and_marks").fetchall()
    summa, kolvo = main_csp.counter_comparison(result)
    update.message.reply_text("*🙊Рейтинг бота:*\n_👉" + str(summa / kolvo) + " / 5👈_\n\nКажется, я не так плоха💌",
                              parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
    con.close()


def be_back_other(update, context):
    update.message.reply_text("Вы вернулись обратно. Сделайте свой выбор:",
                              reply_markup=ReplyKeyboardMarkup(main_csp.SECTION_OTHER, resize_keyboard=True))
