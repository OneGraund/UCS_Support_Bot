from telebot import TeleBot
from dotenv import load_dotenv
from os import getenv
from time import sleep
import threading
import src.openai_gpt.gpt
import src.utilities.helpers


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
        def message_handling(message):
            # Handlers func goes here
            if message.text.lower().find('bot')!=-1 or message.text.lower().find('бот')!=-1:
                response = src.openai_gpt.gpt.choose_command(
                    available_functions=src.utilities.helpers.available_functions,
                    text=message.text
                )
                if response.find(';')!=-1:
                    response = response.split(';')
                    to_send=f'Calling function {response[0]}. With arguments: '
                    for i in range(1, len(response)):
                        to_send+=f'{response[i]} '
                    self.send_message(
                        chat_id=self.group_id,
                        message=to_send
                    )
                    to_print = f'[TELEGRAM] Message text: {message.text}\n\t[OPENAI CHOOSE_COMMAND]' \
                               f' chose function {response[0]} with arguments: '
                    for index, arg in enumerate(response[1:]):
                        to_print+= f'{arg}, '
                        response[index+1]=response[index+1][1:]
                    print(to_print)
                    src.utilities.helpers.available_functions[response[0]]['func'](response[1:])
                else:
                    self.send_message(
                        chat_id=self.group_id,
                        message=f'Calling function: {response}'
                    )
                    print(f'[TELEGRAM] Calling function: {response}')
                    src.utilities.helpers.available_functions[response]['func']()
            else:
                print('[TELEGRAM] A message was spotted in group chat, but not to bot')
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
    UCSSupportBot.DEBUG = 1
    UCSSupportBot(
        token=TELEGRAM_TOKEN,
        ucs_group_chat_id=GROUP_CHAT_ID
    )
