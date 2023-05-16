from telebot import TeleBot
from dotenv import load_dotenv
from os import getenv
from time import sleep
import threading

DEBUG=1
SENDER_DELAY=60

load_dotenv()
TELEGRAM_TOKEN = getenv('TELEGRAM_TOKEN')
if DEBUG:
    UCS_GROUP_CHAT_ID = getenv('TELEGRAM_TEST_GROUP_ID')
else:
    UCS_GROUP_CHAT_ID = getenv('TELEGRAM_UCS_GROUP_ID')

class UCSSupportBot:
    def __init__(self, token, ucs_group_chat_id):
        self.bot = TeleBot(token)
        self.group_id = ucs_group_chat_id
        if DEBUG:
            self.send_message(ucs_group_chat_id, f"{str('=')*25}\n"
                                                 f'[TELEGRAM] Bot started!')
        self.senderThread = threading.Thread(target=self.sender, args=())
        self.senderThread.start()
        self.handlers()
        if DEBUG:
            self.bot.polling()
        else:
            self.bot.infinity_polling()



    def send_message(self, chat_id, message):
        self.bot.send_message(chat_id, message)

    def handlers(self):
        if DEBUG:
            self.send_message(self.group_id, '[HANDLERS] Handlers initialised')
        @self.bot.message_handler(func=lambda message: True)
        def echo_all(message):
            # Handlers func goes here
            self.bot.reply_to(message, message.text)

        if DEBUG:
            self.bot.polling()
        else:
            self.bot.infinity_polling()

    def sender(self):
        if DEBUG:
            self.send_message(self.group_id, '[SENDER] Sender started')
        while True:
            sleep(SENDER_DELAY)
            # Sender func goes here
            self.bot.send_message(self.group_id, '[SENDER] Bot is working')


if __name__=='__main__':
    UCSSupportBot(token=TELEGRAM_TOKEN, ucs_group_chat_id=UCS_GROUP_CHAT_ID)