import telebot

from config import config, logger

bot = telebot.TeleBot(config.token)
logger.info('Telegram Bot started.')

bot.set_my_commands(
    [
        telebot.types.BotCommand(command='start', description='Start bot'),
        telebot.types.BotCommand(command='help', description='Help message'),
        telebot.types.BotCommand(command='about', description='About the bot'),
        telebot.types.BotCommand(command='sum', description='Summation of digits'),
        telebot.types.BotCommand(command='confirm', description='Confirm action')
    ]
)
logger.info('Bot commands loaded.')


def sum_process(text: str) -> str:
    tokens = text.strip().replace(',', ' ').split()
    numbers = []

    for token in tokens:
        if token.replace('.', '').lstrip('-').isdigit():
            numbers.append(int(token))

    if not numbers:
        result = 'В сообщении нет цифр.\nПример использования команды: /sum 2 3 10'
    else:
        result = f'Сумма: {sum(numbers)}'

    logger.debug(f'Summation of numbers: {tokens}. Result: {result}')

    return result

def create_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    keyboard.row('О боте', 'Сумма')
    keyboard.row('Помощь', 'Скрыть клавиатуру')

    return keyboard


@bot.message_handler(commands=['start'])
def send_start(message: telebot.types.Message):
    bot.reply_to(message, 'Привет! Я простой бот! Напиши /help', reply_markup=create_keyboard())
    logger.info(f'Sent start message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    bot.reply_to(message, '/start - Начать\n/help - Помощь\n/about - О боте\n/sum - Суммирование чисел\n/confirm - Подтвердить действие')
    logger.info(f'Sent help message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['about'])
def send_about(message: telebot.types.Message):
    bot.reply_to(message, 'Простой телеграм бот в рамках семинарских занятий.\nАвтор: Агаев Арсений Валерьевич 1032221668')
    logger.info(f'Sent about message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['sum'])
def send_sum(message: telebot.types.Message):
    text = sum_process(message.text.replace('/sum', ''))

    bot.reply_to(message, text)
    logger.info(f'Sent sum message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['hide'])
def hide_keyboard(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Клавиатура спрятана', reply_markup=telebot.types.ReplyKeyboardRemove())
    logger.info(f'Keyboard remove for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['confirm'])
def send_confirm(message: telebot.types.Message):
    keyboard = telebot.types.InlineKeyboardMarkup()

    keyboard.add(
        telebot.types.InlineKeyboardButton('Да', callback_data='confirm:yes'),
        telebot.types.InlineKeyboardButton('Нет', callback_data='confirm:no')
    )

    bot.send_message(message.chat.id, 'Подтвердить действие?', reply_markup=keyboard)
    logger.info(f'Sent confirm message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(func=lambda message: message.text == 'Помощь')
def send_help_button(message: telebot.types.Message):
    send_help(message)
    logger.info(f'Process keyboard button "Помощь" for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(func=lambda message: message.text == 'О боте')
def send_about_button(message: telebot.types.Message):
    send_about(message)
    logger.info(f'Process keyboard button "О боте" for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(func=lambda message: message.text == 'Сумма')
def send_sum_button(message: telebot.types.Message):
    bot.send_message(message.chat.id, 'Введите числа через пробел или запятую:')
    bot.register_next_step_handler(message, send_text_sum)
    logger.info(f'Process keyboard button "Сумма" for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(func=lambda message: message.text == 'Скрыть клавиатуру')
def hide_keyboard_button(message: telebot.types.Message):
    hide_keyboard(message)
    logger.info(f'Process keyboard button "Скрыть клавиатуру" for {message.from_user.id} ({message.from_user.first_name}).')


def send_text_sum(message: telebot.types.Message):
    text = sum_process(message.text)

    bot.reply_to(message, text)
    logger.info(f'Summarization from text for {message.from_user.id} ({message.from_user.first_name}).')


@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm:'))
def send_confirm_yes_button(call: telebot.types.CallbackQuery):
    choice = call.data.split(':', 1)[1]

    bot.answer_callback_query(call.id, 'Принято')
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

    bot.send_message(call.message.chat.id, 'Готово!' if choice == 'yes' else 'Отменено.')
    logger.info(f'Process inline keyboard button "{call.data}" for {call.message.chat.id}.')


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
