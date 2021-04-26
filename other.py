# прочее
import main_csp
from telegram import ReplyKeyboardMarkup, ParseMode


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
