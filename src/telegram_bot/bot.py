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
        #self.handlersThread = threading.Thread(target=self.handlers, args=())
        #self.handlersThread.start()
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
                print(f'[TELEGRAM] A message was spotted to the bot from user_id {message.from_user()}. Sending to OpenAI...')
                def employee_by_user_id(dictionary, value):
                    for key, val in dictionary.items():
                        if val == value:
                            return key
                    return None  # Value not found in the dictionary

                employees = {
                    'Alex': getenv('TELEGRAM_ALEX_USER_ID'),
                    'Vova': getenv('TELEGRAM_VOVA_USER_ID'),
                    'Egor': getenv('TELEGRAM_EGOR_USER_ID'),
                    'Yaro': getenv('TELEGRAM_YARO_USER_ID')
                }

                user_id = message.from_user()
                employee_name = employee_by_user_id(employees, user_id)
                response = src.openai_gpt.gpt.choose_command(
                    available_functions=src.utilities.helpers.available_functions,
                    text=f'From: {employee_name} {message.text}'
                )
                del employee_name
                print(f'\t[OPENAI] Response: {response}')
                if response.find(';')!=-1:
                    response = response.split(';')
                    to_send=f'Calling function "{response[0]}". With arguments: '
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
                    src.utilities.helpers.available_functions[response[0]]['func'](*response[1:])
                elif response=='None':
                    self.send_message(
                        chat_id=self.group_id,
                        message=f'This is not one of my functions'
                    )
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
            if UCSSupportBot.DEBUG:
                self.bot.send_message(self.group_id, '[SENDER] Bot is working')


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
