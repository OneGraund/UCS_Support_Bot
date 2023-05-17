from telebot import TeleBot
from dotenv import load_dotenv
from os import getenv
from time import sleep
import threading


class UCSSupportBot:
    DEBUG = 1
    SENDER_DELAY = 60
    def __init__(self, token, ucs_group_chat_id):
        self.bot = TeleBot(token)
        self.group_id = ucs_group_chat_id
        if UCSSupportBot.DEBUG:
            self.send_message(ucs_group_chat_id, f"{str('=') * 25}\n"
                                                 f'[TELEGRAM] Bot started!')
        self.senderThread = threading.Thread(target=self.sender, args=())
        self.senderThread.start()
        self.handlers()
        if UCSSupportBot.DEBUG:
            self.bot.polling()
        else:
            self.bot.infinity_polling()

    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)

    def handlers(self):
        if UCSSupportBot.DEBUG:
            self.send_message(self.group_id, '[HANDLERS] Handlers initialised')

        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            # Handlers func goes here
            self.bot.reply_to(message, message.text)

        if UCSSupportBot.DEBUG:
            self.bot.polling()
        else:
            self.bot.infinity_polling()

    def sender(self):
        if UCSSupportBot.DEBUG:
            self.send_message(self.group_id, '[SENDER] Sender started')
        while True:
            sleep(self.SENDER_DELAY)
            # Sender func goes here
            # self.bot.send_message(self.group_id, '[SENDER] Bot is working')


if __name__ == '__main__':
    load_dotenv()
    TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
    if UCSSupportBot.DEBUG:
        GROUP_CHAT_ID = getenv('TELEGRAM_TEST_GROUP_ID')
    else:
        GROUP_CHAT_ID = getenv('TELEGRAM_UCS_GROUP_ID')
    UCSSupportBot.DEBUG = 0
    UCSSupportBot(
        token=TELEGRAM_TOKEN,
        ucs_group_chat_id=GROUP_CHAT_ID
    )
