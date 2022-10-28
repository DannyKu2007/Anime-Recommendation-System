from ..internal.composites.app_composite import prepare_application

from ..internal.adapters.db.sqlite import get_watched_document, get_undesired_document, \
    watch_anime, allow_anime, hate_anime

from ..internal.model.recommendation import get_recommendation

import telebot

token = '5781935967:AAHeQg2ORA7ceDO-PBSHX9Mbs28S726hS84'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start', 'help'])
def get_instruction(message):
    global cmd
    cmd[message.from_user.id] = 'start'

    instruction = "Hi, I'm a bot that recommends anime to people depending on their viewing history. " \
                  "I work very simply.\n" + \
                  "\n" + \
                  "Here are the main commands:\n" + \
                  "/start, /help - getting instructions\n" + \
                  "/my_watched_list - anime that you specified as viewed\n" + \
                  "/watch - write down what other anime you watched " \
                  "(you need to first write /watch, and then the name of the anime)\n" + \
                  "/recommendation - getting a recommendation\n" + \
                  "\n" + \
                  "Also, obviously you may not like some recommendations, so that a certain anime is not offered, " \
                  "you need to enter the /hate command, and then specify the name on the next line. " \
                  "To get a list of all undesired anime, type /my_hate_list. " \
                  "If you already don't mind being recommended this anime, you can write /allow, " \
                  "and then the name of the anime.\n"

    bot.send_message(message.chat.id, instruction)


@bot.message_handler(commands=['recommendation'])
def get_user_recommendation(message):
    user_id = message.from_user.id

    global cmd
    cmd[user_id] = 'recommendation'

    recommendation = get_recommendation(logger, user_id, removing_symbols)

    warning_msg = ["for a recommendation, you need at least one watched anime",
                   "sorry, i can't recommend anything to you"]

    bot.send_message(message.chat.id, recommendation.title() if recommendation not in warning_msg else recommendation)


@bot.message_handler(commands=['my_watched_list'])
def get_watched_anime(message):
    user_id = message.from_user.id

    global cmd
    cmd[user_id] = 'watched_list'

    user_watched_document = get_watched_document(logger, user_id)

    bot.send_message(
        message.chat.id,
        f'here is your list of watched anime at the moment: {", ".join(user_watched_document).title()}'
    )


@bot.message_handler(commands=['my_hate_list'])
def get_undesired_anime(message):
    user_id = message.from_user.id

    global cmd
    cmd[user_id] = 'hate_list'

    user_undesired_document = get_undesired_document(logger, user_id)

    bot.send_message(
        message.chat.id,
        f'here is your list of undesired anime at the moment: {", ".join(user_undesired_document).title()}'
    )


@bot.message_handler(commands=['watch'])
def add_watched_anime(message):
    global cmd
    cmd[message.from_user.id] = '/watch'


@bot.message_handler(commands=['allow'])
def user_allow_anime(message):
    global cmd
    cmd[message.from_user.id] = '/allow'


@bot.message_handler(commands=['hate'])
def add_undesired_anime(message):
    global cmd
    cmd[message.from_user.id] = '/hate'


@bot.message_handler(content_types=['text'])
def reply(message):
    user_id = message.from_user.id

    global cmd
    if user_id not in cmd:
        cmd[user_id] = ''

    msg = message.text
    msg = msg.lower().capitalize().translate(str.maketrans('', '', removing_symbols))

    if cmd[message.from_user.id] == '/watch':
        watch_anime(logger, user_id, msg)

    elif cmd[message.from_user.id] == '/allow':
        allow_anime(logger, user_id, msg)

    elif cmd[message.from_user.id] == '/hate':
        hate_anime(logger, user_id, msg)

    else:
        bot.send_message(message.chat.id, 'invalid format')

    cmd[message.from_user.id] = ''


if __name__ == '__main__':
    logger, removing_symbols = prepare_application()

    cmd = {}

    bot.infinity_polling()
