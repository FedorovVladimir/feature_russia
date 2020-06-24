import json
import telebot

from site_parser import parse

config_file_name = 'telegram_token.json'
try:
    with open(config_file_name, 'r') as file:
        data = file.read()
except FileNotFoundError as e:
    print(f"File {config_file_name} not found.")
    exit()
config = json.loads(data)

bot = telebot.TeleBot(config["token"])


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, 'Привет я bot для статистики конкурса "Будущее России"" от 3CRABS soft!\n'
                                      'Чтобы узнать подробности введи /help')


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "Команды:\n"
                                      "/start - привет бот\n"
                                      "/help - помощь\n"
                                      "Бот {количество записей не больше 10)} - показ части списка\n")


def create_answer(text: str, chat_id):
    if text.startswith('бот'):
        try:
            count = int(text.replace('бот', '').strip())
            if count > 10:
                return 'Нельзя запрашивать больше десяти участников.'
        except ValueError:
            return 'Ожидалось число участников или ничего'

        bot.send_message(chat_id, f'Ищу {count} участников. Подождите...')
        return parse(count)


@bot.message_handler(content_types=["text"])
def content_text(message):
    chat_id = message.chat.id
    answer = create_answer(message.text.lower(), chat_id)
    if answer is not None:
        bot.send_message(chat_id, answer)


if __name__ == '__main__':
    bot.polling()
