# communication skills progress
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup
from settings import TG_TOKEN
import vocabulary
import long_song_about
import english_quotes
import other
import marks
import reviews
import sqlite3


MAIN_MENU = [["🦋все упражнения🦋"], ["↪прочее↩"]]
MENU_MANY_WORDS = [["🐣для увеличения словарного запаса🐥"], ["🎤что вижу, о том и пою🎤"],
                   ["🔡развитие английской речи🔠	"], ["🔙вернуться в главное меню🔙"]]
SECTION_OTHER = [["💯оценка💯", "🐝отзывы🐝"], ["🐾автор проекта🐾"], ["👣мотивация создания бота👣"],
                 ["🔙вернуться в главное меню🔙"]]
PART_OF_SPEECH = [["имена\nсуществительные", "имена\nприлагательные"], ["глаголы", "наречия"],
                  ["🔙вернуться назад🔙", "🐒позвать Sofia🐒"]]
MARK_MENU = [["🆕поставить оценку🆕", "💌узнать рейтинг💌", "🔢изменить оценку🔢"],
             ["🔙вернуться обратно🔙", "🐒позвать Sofia🐒"]]
REVIEWS_MENU = [["оставить отзыв", "посмотреть отзывы"], ["вернуться обратно"]]


def start(update, context):
    update.message.reply_text(f"Привет, {update.message.chat.first_name}!👋 Я Ваш бот-помощник по развитию "
                              f"коммуникативных навыков.\n\nМожете называть меня Sofia! :)",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU,
                                                               one_time_keyboard=False, resize_keyboard=True))


def sofia(update, context):
    update.message.reply_text("Я тут! Чем могу Вам помочь?)🐒",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def what_is_it(update, context):
    update.message.reply_text("Извините, не знаю такой команды: " + update.message.text,
                              reply_markup=ReplyKeyboardMarkup([["🐒позвать Sofia🐒"]], resize_keyboard=True))


def be_back_to_the_main_menu(update, context):
    update.message.reply_text("Вы вернулись в главное меню:",
                              reply_markup=ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True))


def all_ex(update, context):
    update.message.reply_text("Выберите тип упражнений:",
                              reply_markup=ReplyKeyboardMarkup(MENU_MANY_WORDS, resize_keyboard=True))


def otherr(update, context):
    update.message.reply_text("Вам правда интересен этот раздел?..🥺",
                              reply_markup=ReplyKeyboardMarkup(SECTION_OTHER, resize_keyboard=True))


# вспомогательные функции (методы)

def counter_comparison(result):
    summa, kolvo = 0, 0
    for i in result:
        if i[0] is not None:
            summa += int(i[0])
            kolvo += 1
    return summa, kolvo


def get_cursor():
    con = sqlite3.connect("bd_tgbot_comskills.db")
    cursor = con.cursor()
    return con, cursor


def main():
    updater = Updater(TG_TOKEN, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.regex("начать"), start))
    dp.add_handler(CommandHandler("Sofia", sofia))
    dp.add_handler(MessageHandler(Filters.regex("Sofia"), sofia))

    dp.add_handler(MessageHandler(Filters.regex("прочее"), otherr))
    dp.add_handler(CommandHandler("other", otherr))
    dp.add_handler(CommandHandler("rating", other.get_rating))
    dp.add_handler(MessageHandler(Filters.regex("рейтинг"), other.get_rating))
    dp.add_handler(MessageHandler(Filters.regex("автор"), other.author))
    dp.add_handler(CommandHandler("author", other.author))
    dp.add_handler(MessageHandler(Filters.regex("мотивация"), other.motivation))
    dp.add_handler(CommandHandler("motivation", other.motivation))

    dp.add_handler(MessageHandler(Filters.regex("поставить оценку"), marks.set_mark))
    dp.add_handler(MessageHandler(Filters.regex("изменить оценку"), marks.change_mark))
    dp.add_handler(MessageHandler(Filters.regex("оценка"), marks.mark))
    dp.add_handler(CallbackQueryHandler(marks.add_mark_to_bd))

    dp.add_handler(MessageHandler(Filters.regex("оставить отзыв"), reviews.set_review))
    dp.add_handler(MessageHandler(Filters.regex("посмотреть отзывы"), reviews.get_reviews))
    dp.add_handler(MessageHandler(Filters.regex("SG"), reviews.add_review_to_file_and_bd))
    dp.add_handler(MessageHandler(Filters.regex("отзывы"), reviews.reviews))
    dp.add_handler(CommandHandler("reviews", reviews.get_reviews))

    dp.add_handler(CommandHandler("all_ex", all_ex))
    dp.add_handler(MessageHandler(Filters.regex("все упражнения"), all_ex))
    dp.add_handler(CommandHandler("many_words", vocabulary.many_words))
    dp.add_handler(MessageHandler(Filters.regex("словарного запаса"), vocabulary.many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nсуществительные"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("имена\nприлагательные"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("глаголы"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("наречия"), vocabulary.goals_many_words))
    dp.add_handler(MessageHandler(Filters.regex("начнем!"), vocabulary.set_timer_for_many_words))
    dp.add_handler(MessageHandler(Filters.regex("плюс"), vocabulary.plus_one))

    dp.add_handler(MessageHandler(Filters.regex("что вижу, о том и пою"), long_song_about.long_song_about))
    dp.add_handler(CommandHandler("song_about", long_song_about.long_song_about))
    dp.add_handler(MessageHandler(Filters.regex("словечко"), long_song_about.song_about_word))
    dp.add_handler(MessageHandler(Filters.regex("следующее слово"), long_song_about.song_about_word))
    dp.add_handler(MessageHandler(Filters.regex("я закончил"), all_ex))

    dp.add_handler(MessageHandler(Filters.regex("развитие английской речи"), english_quotes.english_speech))
    dp.add_handler(CommandHandler("eng_quotes", english_quotes.english_speech))
    dp.add_handler(MessageHandler(Filters.regex("цитата"), english_quotes.get_quote))

    dp.add_handler(CommandHandler("be_back_mm", be_back_to_the_main_menu))
    dp.add_handler(MessageHandler(Filters.regex("вернуться в главное меню"), be_back_to_the_main_menu))
    dp.add_handler(CommandHandler("be_back", vocabulary.be_back_to_the_menu_many_words))
    dp.add_handler(MessageHandler(Filters.regex("вернуться назад"), vocabulary.be_back_to_the_menu_many_words))
    dp.add_handler(CommandHandler("be_back_ot", other.be_back_other))
    dp.add_handler(MessageHandler(Filters.regex("вернуться обратно"), other.be_back_other))

    dp.add_handler(MessageHandler(Filters.text, what_is_it))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
