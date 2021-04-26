# развитие английской речи
import requests
import main_csp
from telegram import ReplyKeyboardMarkup, ParseMode


def english_speech(update, context):
    con, cursor = main_csp.get_cursor()
    letter = update.message.text
    goal = cursor.execute(f"SELECT goal, how_to_do FROM parts_of_speech WHERE part_of_sp ='{letter[1:-1]}' ").fetchone()
    update.message.reply_text("*Цель:* \n☑ _" + goal[0] + "_☑", parse_mode=ParseMode.MARKDOWN)
    update.message.reply_text("*Как выполнять:* \n🆙" + goal[1], parse_mode=ParseMode.MARKDOWN,
                              reply_markup=ReplyKeyboardMarkup([["🤏цитата🤏"], ["🔙вернуться назад🔙"]],
                                                               resize_keyboard=True))
    con.close()


def get_quote(update, context):
    response = requests.get("https://api.kanye.rest/")
    json_response = response.json()
    print(json_response['quote'])
    update.message.reply_text(json_response['quote'],
                              reply_markup=ReplyKeyboardMarkup([["🔃следующая цитата🔃"], main_csp.FINISH_TALKING],
                                                               resize_keyboard=True))
