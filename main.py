import telebot

from config import config, logger

bot = telebot.TeleBot(config.token)
logger.info('Telegram Bot started.')

bot.set_my_commands(
    [
        telebot.types.BotCommand(command='start', description='Start bot'),
        telebot.types.BotCommand(command='help', description='Help message'),
        telebot.types.BotCommand(command='about', description='About the bot')
    ]
)
logger.info('Bot commands loaded.')


@bot.message_handler(commands=['start'])
def send_start(message: telebot.types.Message):
    bot.reply_to(message, 'Привет! Я простой бот! Напиши /help')
    logger.info(f'Sent start message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['help'])
def send_help(message: telebot.types.Message):
    bot.reply_to(message, '/start - Начать\n/help - Помощь\n/about - О боте')
    logger.info(f'Sent help message for {message.from_user.id} ({message.from_user.first_name}).')


@bot.message_handler(commands=['about'])
def send_about(message: telebot.types.Message):
    bot.reply_to(message, 'Простой телеграм бот в рамках семинарских занятий.\nАвтор: Агаев Арсений Валерьевич 1032221668')
    logger.info(f'Sent about message for {message.from_user.id} ({message.from_user.first_name}).')


if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
