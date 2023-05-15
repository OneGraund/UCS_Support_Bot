from dotenv import load_dotenv
import os
import openai
import src.utilities.helpers

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEBUG = 1


def askGPT(prompt):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=1,
        max_tokens=2000,
    )
    return response.choices[0].text


def choose_command(available_functions, text):
    prompt = f'Given is this user input: "{text}". '
    # Given is this user input: "Bot, who is working this Monday?"
    prompt += 'Your task it to choose between this available bot functions the one that ' \
              'suits user input the best and output only the string that is like in given examples' \
              '. Here are the available bot functions:\n'
    for func_name in available_functions:
        prompt += f'{func_name}'
        if 'args' in available_functions[func_name]:
            prompt += f', that takes this arguments:'
            for index, arg in enumerate(available_functions[func_name]['args']):
                if index == len(available_functions[func_name]['args']) - 1:
                    prompt += f' {arg}.'
                else:
                    prompt += f' {arg},'
        if 'gpt' in available_functions[func_name]:
            if type(available_functions[func_name]['gpt']['input_example']) is not list:
                prompt += f' Here is an example for user input: ' \
                          f'{available_functions[func_name]["gpt"]["input_example"]}.'
                prompt += f' In this case your output should be like that: ' \
                          f'{available_functions[func_name]["gpt"]["output_example"]}'
            elif type(available_functions[func_name]['gpt']['input_example']) is list:
                prompt += f' Here are examples for user inputs and your outputs:\n'
                for index, user_input in enumerate(available_functions[func_name]['gpt']['input_example']):
                    prompt += f"User's input:\n{user_input},\n"
                    prompt += f"In this case your output should be like that:\n{available_functions[func_name]['gpt']['output_example'][index]}\n"
    if DEBUG:
        print(f'[OPENAI PROMPT]\n{prompt}')

    answer = askGPT(prompt)
    if DEBUG:
        print(f'[OPENAI RESPONSE]\n{answer[1:]}')
    return answer.replace('\n', '')


choose_command(available_functions=src.utilities.helpers.available_functions, text='Бот, скажи пожалуйста кто работает в эту пятницу')