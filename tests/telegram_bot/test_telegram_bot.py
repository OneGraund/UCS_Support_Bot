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
    UCSSupportBot.DEBUG = 1
    ucs_bot = UCSSupportBot(
        token=tg_secrets['tokens']['UCSSupportBot'],
        ucs_group_chat_id=tg_secrets['groups']['test']
    )


class TestBotCoreFunctionality(unittest.TestCase):
    def test_choose_command(self):
        pass