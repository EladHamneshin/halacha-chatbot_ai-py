from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ParseMode
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.callbackquery import CallbackQuery
from telegram.ext.filters import Filters
from telegram.ext.updater import Updater
from telegram.update import Update
import halacha_chatbotBL
import sys

with open("token.txt", "r") as fIn:
    TOKEN = fIn.read()
shabbat_category_str = "שבת" + " \N{candle} \N{candle}"
brachot_category_str = "ברכות" + " \N{avocado}"


def qa_str_format(question, answer):
    """
    format the quetion and the answer to be sent to the user
    :param quetion: the quetion
    :param answer: the answer
    :return: the formatted string
    """
    return "<b>שאלה:</b> {} \n\n<b>תשובה:</b> {}\n".format(question, answer)


############################ Bot #########################################
def error_logger(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    sys.stderr.write("ERROR: '{}' caused by '{}'".format(
        context.error, update))
    pass


def start_cmd_handler(update, context):
    """
    callback method handling /start command
    """
    update.message.reply_text(
        "<b>ברוך הבא! \n יש לך שאלה הלכתית? הגעת למקום הנכון! \n כתוב את השאלה שלך ואני אנסה לענות עליה.\n</b>",
        reply_markup=start_menu_keyboard(),
        parse_mode=ParseMode.HTML)


def good_result_btn_handler(update, context):
    """
    callback method handling good result button press
    """
    query: CallbackQuery = update.callback_query

    query.answer()

    quetion, answer = halacha_chatbotBL.get_answer_by_index(0)

    # editing message sent by the bot
    query.edit_message_text(qa_str_format(quetion, answer),
                            parse_mode=ParseMode.HTML)


def bad_result_btn_handler(update, context):
    """
    callback method handling bad result button press
    """
    query: CallbackQuery = update.callback_query

    query.answer()

    ans = '<b>האם התכוונת לאחת מהשאלות הבאות?\n\n</b>'
    for i in range(1, 3):
        quetion, answer = halacha_chatbotBL.get_answer_by_index(i)
        ans += qa_str_format(quetion, answer) + '\n\n'

    # editing message sent by the bot
    query.edit_message_text(ans,
                            reply_markup=next_questions_keyboard(),
                            parse_mode=ParseMode.HTML)


def next_questions_btn_handler(update, context):
    """
    callback method handling next questions button press
    """
    query: CallbackQuery = update.callback_query

    query.answer()

    question, answer = halacha_chatbotBL.get_answer_by_index(0)

    if query.data == "q1":
        question, answer = halacha_chatbotBL.get_answer_by_index(1)
        # halacha_chatbotBL.append_question(
        #    question, answer, halacha_chatbotBL.current_question_embedding)
    elif query.data == "q2":
        question, answer = halacha_chatbotBL.get_answer_by_index(2)
        # halacha_chatbotBL.append_question(
        #    question, answer, halacha_chatbotBL.current_question_embedding)

    # editing message sent by the bot
    query.edit_message_text(qa_str_format(question, answer),
                            parse_mode=ParseMode.HTML)


def reply_txt_handler(update: Update, context: CallbackContext):
    """
    callback method handling user text reply
    """
    if update.message.text == shabbat_category_str:
        halacha_chatbotBL.update_shabbat()
        update.message.reply_text("\U0001F44D")
    elif update.message.text == brachot_category_str:
        halacha_chatbotBL.update_brachot()
        update.message.reply_text("\U0001F44D")
    else:
        user_question = update.message.text
        question, answer = halacha_chatbotBL.find_closest_answer(user_question)
        update.message.reply_text(qa_str_format(question, answer),
                                  reply_markup=yes_no_keyboard(),
                                  parse_mode=ParseMode.HTML)


############################ Keyboards #########################################
def next_questions_keyboard():
    keyboard = [
        [InlineKeyboardButton('שאלה 1', callback_data='q1')],
        [InlineKeyboardButton('שאלה 2', callback_data='q2')],
        [
            InlineKeyboardButton('זה אמור להיות טוב יותר? ' +
                                 "\N{rolling on the floor laughing}",
                                 callback_data='next')
        ],
    ]
    return InlineKeyboardMarkup(keyboard)


def yes_no_keyboard():
    keyboard = [[
        InlineKeyboardButton("מעולה תודה!!!" +
                             " \N{grinning face with smiling eyes}",
                             callback_data='good')
    ],
                [
                    InlineKeyboardButton("זה לא מה ששאלתי" +
                                         " \N{confused face}",
                                         callback_data='bad')
                ]]
    return InlineKeyboardMarkup(keyboard)


def start_menu_keyboard():
    keyboard = [[KeyboardButton(shabbat_category_str)],
                [KeyboardButton(brachot_category_str)]]
    return ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)


############################# Handlers #########################################
def main():
    # creating updater
    updater: Updater = Updater(TOKEN, use_context=True)

    # adding listeners
    updater.dispatcher.add_handler(CommandHandler('start', start_cmd_handler))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.text, reply_txt_handler))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(good_result_btn_handler, pattern="good"))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(bad_result_btn_handler, pattern="bad"))
    updater.dispatcher.add_handler(
        CallbackQueryHandler(next_questions_btn_handler))
    updater.dispatcher.add_error_handler(error_logger)

    # started polling
    updater.start_polling()


if "__main__" == __name__:
    main()