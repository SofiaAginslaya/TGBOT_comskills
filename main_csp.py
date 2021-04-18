# communication skills progress
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
import random
from settings import TG_TOKEN

MAIN_MENU = [["все упражнения"], ["оценить приложение"], ["автор проекта", "мотивация"],
             ["позвать Sofia"]]
MENU_MANY_WORDS = [["для увеличения словарного запаса"], ["для развития дикции"],
                   ["для развития коммуникабельности"], ["вернуться в главное меню"]]
PART_OF_SPEECH = [["имена\nсуществительные", "имена\nприлагательные"], ["глаголы"], ["вернуться назад"]]


def start(update, context):
    update.message.reply_text(
        "Привет! Я твой бот-помощник по развитию коммуникативных навыков.\n\nМожешь называть меня Sofia! :)",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, one_time_keyboard=False, resize_keyboard=True))


def sofia(update, context):
    update.message.reply_text("Я тут! Чем могу тебе помочь?)",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def all_ex(update, context):
    update.message.reply_text("Выберете тип упражнений:",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))


def many_words(update, context):
    update.message.reply_text("Выберете, над какой частью речи Вы хотите поиздеваться)) :",
                              reply_markup=ReplyKeyboardMarkup(PART_OF_SPEECH, resize_keyboard=True))


def be_back_to_the_main_menu(update, context):
    update.message.reply_text("Вы вернулись в главное меню:",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def be_back_to_the_menu_many_words(update, context):
    update.message.reply_text("Вы вернулись назад.",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))


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

    dp.add_handler(CommandHandler("be_back_mm", be_back_to_the_main_menu))
    dp.add_handler(MessageHandler(Filters.regex("вернуться в главное меню"), be_back_to_the_main_menu))
    dp.add_handler(CommandHandler("be_back", be_back_to_the_menu_many_words))
    dp.add_handler(MessageHandler(Filters.regex("вернуться назад"), be_back_to_the_menu_many_words))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
