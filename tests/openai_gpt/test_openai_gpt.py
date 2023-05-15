import unittest
import sys
sys.path.append('C:/Users/OneGraund/PycharmProjects/UCS_Support_Bot')
from src.openai_gpt.gpt import *


functions = {
    'Make some coffee': {
        'func': None,
        'args': ['milk', 'sugar'],
        'gpt': {
            'input_example': ['Bot, can you make me some rereshing coffee that contains '
                             'milk, but because I am alergic to sugar, add no sugar',
                              'Bot, make me coffee with sugar and milk',
                              'Hey, the greatest bot. If you can, please make me a coffee without anything. Thanks'],
            'output_example': ['Make some coffee; True; False',
                               'Make some coffee; True; True',
                               'Make some coffee; False; False']
        }
    },
    'Get who is working at': {
        'func': None,
        'args': ['date'],
        'gpt': {
            'input_example': ['Bot, who is working this Monday?',
                              'Bot, who should work the next Friday?'],
            'output_example': ['Get who is working at; this Monday',
                               'Get who is working at; next Friday']
        }
    }
}


class TestChooseCommand(unittest.TestCase):

    def test_choose_command_coffee(self):
        # Test case 1 for coffee
        response1 = choose_command(
            available_functions=functions,
            text="Hey, bot. I would really like you to make an espresso, but don't "
                 "make it sweet or anything. Milk would be great. Thank you!"
        )
        self.assertEqual(response1, 'Make some coffee; True; False')

        # Test case 2 for coffee
        response2 = choose_command(
            available_functions=functions,
            text='Good day to you, the greatest bot. Make me pure coffee please. Thanks'
        )
        self.assertEqual(response2, 'Make some coffee; False; False')

        # Test case 3 for coffee
        response3 = choose_command(
            available_functions=functions,
            text='You know what, bot? I am a huge coffee lover. What I like even more is the additional stuff'
                 ' you can put in it. So if you may, add to my coffee everything you can :)'
        )
        self.assertEqual(response3, 'Make some coffee; True; True')



    def test_choose_command_who_is_working_at(self):
        # Test case 2 for who is working
        response2 = choose_command(
            available_functions=functions,
            text='How is it going, bot? I am confused... Who can be working on the next Monday?'
        )
        self.assertEqual(
            response2,
            'Get who is working at; next Monday'
        )