# что вижу, о том и пою
from telegram import ReplyKeyboardMarkup, ParseMode
import requests
from bs4 import BeautifulSoup
import random
import main_csp

# такое strange решение задачи по причине того, что я не нашла api русского словаря
url = 'http://dict.ruslang.ru/freq.php?act=show&dic=freq_s&title=%D7%E0%F1%F2%EE%F2%ED%FB%E9%20%F1%EF%E8%F1%EE%EA%20%' \
      'E8%EC%E5%ED%20%F1%F3%F9%E5%F1%F2%E2%E8%F2%E5%EB%FC%ED%FB%F5'
r = requests.get(url)
soup = BeautifulSoup(r.text, 'lxml')
with open('test.html', 'w') as output_file:
    output_file.write(r.text)

soup1 = soup.find_all('td')
DIGITS = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
words_list = ""
words_counter = 0

for quote in soup1:
    how_not_much_digits = 0
    quote1 = str(quote.text)
    if len(quote1) != 0:
        for i in range(0, 10):
            if DIGITS[i] not in quote1:
                how_not_much_digits += 1
        if how_not_much_digits == 10:
            words_counter += 1
            words_list += str(words_counter) + "" + quote1 + "\n"


def long_song_about(update, context):
    con, cursor = main_csp.get_cursor()
    letter = update.message.text
    print(letter[1:-1])
    goal = cursor.execute(f"""
        SELECT goal, how_to_do, frequency FROM parts_of_speech WHERE part_of_sp = "{letter[1:-1]}" """).fetchone()
    update.message.reply_text("*Цель:* \n☑ _" + goal[0] + "_☑", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Как выполнять:* \n🆙" + goal[1], parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("🅰🅱🅾🅱🅰\n🤓При регулярной практике вскоре вы сможете задвинуть часовую лекцию про ластик, "
                              "стул или дверцу шкафа:))🤠", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Частота выполнения:* \n♾♾♾♾♾♾♾♾\n" + goal[2] + "\n♾♾♾♾♾♾♾♾",
                              parse_mode=ParseMode.MARKDOWN, reply_markup=ReplyKeyboardMarkup([["🤏словечко🤏"],
                                                                                               ["🔙вернуться назад🔙"]],
                                                                                              resize_keyboard=True))
    con.close()


def song_about_word(update, context):
    random_number = random.randint(5, 1000)

    word_random = words_list[words_list.find(str(random_number)) +
                             len(str(random_number)):words_list.find(str(random_number + 1))]
    update.message.reply_text('_' + word_random + '_',
                              reply_markup=ReplyKeyboardMarkup([["🔃следующее слово🔃"], main_csp.FINISH_TALKING],
                                                               resize_keyboard=True), parse_mode=ParseMode.MARKDOWN)
