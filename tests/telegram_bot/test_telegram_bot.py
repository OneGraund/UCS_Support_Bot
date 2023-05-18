import unittest
import sys
import dotenv
import os
import telebot
import threading
import time

sys.path.append('C:/Users/OneGraund/PycharmProjects/UCS_Support_Bot')
from src.telegram_bot.bot import UCSSupportBot

dotenv.load_dotenv()
tg_secrets = {
    'tokens': {
        'UCSSupportBot': os.getenv('TELEGRAM_TOKEN'),
        'TestBot': os.getenv('TELEGRAM_TEST_TOKEN')
    },
    'groups': {
        'test': os.getenv('TELEGRAM_TEST_GROUP_ID'),
        'ucs': os.getenv('TELEGRAM_UCS_GROUP_ID')
    }
}

def start_ucs_bot():
    global ucs_bot
    UCSSupportBot.DEBUG = 0
    ucs_bot = UCSSupportBot(
        token=tg_secrets['tokens']['UCSSupportBot'],
        ucs_group_chat_id=tg_secrets['groups']['test']
    )


def await_message(bot, chat_id):
    print(f'[TELEGRAM] {bot} awaiting message...')
    @bot.message_handler(func=lambda message: True)
    def retrieve_and_end(message):
        # Optional: check user_id to see whether ucs_bot sent this
        return message.text

def wait_and_send(DELAY, bot):
    print(f'[TELEGRAM] Waiting {DELAY} seconds...')
    time.sleep(DELAY)
    bot.send_message(tg_secrets['groups']['test'], '[TEST MESSAGE] TestBotCoreFunctionality')
    print(f'[TELEGRAM] Test message sent!')


class TestBotCoreFunctionality(unittest.TestCase):
    def test_send_message(self):
        # Test send_message
        print(f'[TELEGRAM] Starting test bot...')
        test_bot = telebot.TeleBot(tg_secrets['tokens']['TestBot'])
        print(f'[TELEGRAM] Test Bot started!')

        print(f'[TELEGRAM] Starting ucs bot on separate thread...')
        ucs_bot = None
        ucs_bot_thread = threading.Thread(target=start_ucs_bot)
        ucs_bot_thread.start()
        print(f'[TELEGRAM] Ucs bot started')

        time.sleep(1)

        print(f'[TELEGRAM] sending message via ucs bot on separate thread...')
        test_bot_thread = threading.Thread(target=wait_and_send, args=(2, ucs_bot))
        test_bot_thread.start()
        response = await_message(test_bot, tg_secrets['groups']['test'])

        # Join threads and stop them
        ucs_bot_thread.join()
        test_bot_thread.join()

        self.assertEqual(
            response,
            '[TEST MESSAGE] TestBotCoreFunctionality'
        )