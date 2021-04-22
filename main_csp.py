# communication skills progress
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN
import vocabulary
import long_song_about


MAIN_MENU = [["все упражнения"], ["оценить приложение"], ["автор проекта", "мотивация"]]
MENU_MANY_WORDS = [["для увеличения словарного запаса"],
                   ["что вижу, о том и пою"], ["вернуться в главное меню"]]
PART_OF_SPEECH = [["имена\nсуществительные", "имена\nприлагательные"], ["глаголы", "наречия"],
                  ["🔙вернуться назад🔙", "позвать Sofia"]]


def start(update, context):
    update.message.reply_text(
        "Привет!👋 Я твой бот-помощник по развитию коммуникативных навыков.\n\nМожешь называть меня Sofia! :)",
        reply_markup=ReplyKeyboardMarkup(MAIN_MENU, one_time_keyboard=False, resize_keyboard=True))


def sofia(update, context):
    update.message.reply_text("Я тут! Чем могу тебе помочь?)",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def be_back_to_the_main_menu(update, context):
    update.message.reply_text("Вы вернулись в главное меню:",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def all_ex(update, context):
    update.message.reply_text("Выберите тип упражнений:",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))


def main():
    updater = Updater(TG_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("начать"), start))
    dp.add_handler(CommandHandler("Sofia", sofia))
    dp.add_handler(MessageHandler(Filters.regex("Sofia"), sofia))

    dp.add_handler(CommandHandler("all_ex", all_ex))
    dp.add_handler(MessageHandler(Filters.regex("все упражнения"), all_ex))
    dp.add_handler(CommandHandler("many_words", vocabulary.many_words))
    dp.add_handler(MessageHandler(Filters.regex("словарного запаса"), vocabulary.many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nсуществительные"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nприлагательные"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("глаголы"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("наречия"), vocabulary.goals_many_words))
    dp.add_handler(CommandHandler("timer_for_many_words", vocabulary.set_timer_for_many_words))
    dp.add_handler(MessageHandler(Filters.regex("начнем!"), vocabulary.set_timer_for_many_words))
    dp.add_handler(MessageHandler(Filters.regex("плюс"), vocabulary.plus_one))

    dp.add_handler(MessageHandler(Filters.regex("что вижу, о том и пою"), long_song_about.long_song_about))
    dp.add_handler(MessageHandler(Filters.regex("словечко"), long_song_about.song_about_word))
    dp.add_handler(MessageHandler(Filters.regex("🔃заменить слово🔃"), long_song_about.song_about_word))
    dp.add_handler(MessageHandler(Filters.regex("я закончил"), all_ex))

    dp.add_handler(CommandHandler("be_back_mm", be_back_to_the_main_menu))
    dp.add_handler(MessageHandler(Filters.regex("вернуться в главное меню"), be_back_to_the_main_menu))
    dp.add_handler(CommandHandler("be_back", vocabulary.be_back_to_the_menu_many_words))
    dp.add_handler(MessageHandler(Filters.regex("вернуться назад"), vocabulary.be_back_to_the_menu_many_words))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
