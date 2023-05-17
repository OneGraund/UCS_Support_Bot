from dotenv import load_dotenv
import os
import openai
import src.utilities.helpers

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEBUG = 1


def ask_gpt(prompt, show_output=0):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=40,
        top_p=1,
        best_of=10,
        frequency_penalty=0,
        presence_penalty=0
    )
    if show_output:
        print(f'[OPENAI RESPONSE] {response.choices[0].text}')
    return response.choices[0].text


def choose_command(available_functions, text, show_prompt=0):
    # construction prompt
    prompt = 'Imagine that you are a bot, that outputs a string with a function name and arguments ' \
             'based on a user input. As a bot you have following functions available: '
    for index, func_name in enumerate(available_functions.keys()):
        if 'args' in available_functions[func_name]:
            prompt += f'\"{func_name}'
            for arg_id, arg in enumerate(available_functions[func_name]['args']['names']):
                if arg_id != len(available_functions[func_name]['args']['names']) - 1:
                    prompt += f'; {arg}'
                else:
                    prompt += f'; {arg}\"'
            prompt += ', '
            # \"Make some coffee; milk; sugar\",
            for arg_id, arg in enumerate(available_functions[func_name]['args']['names']):
                if arg_id == 0:
                    prompt += f'where {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]}'
                elif arg_id != len(available_functions[func_name]['args']['names']) - 1:
                    prompt += f', {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]} '
                else:
                    prompt += f'and {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]}; '
            # where milk is boolean (True) and sugar is boolean (False)
        else:
            prompt += f'\"{func_name}\"; '

        # Add examples to GPT
        if 'input_example' in available_functions[func_name]['gpt']:
            prompt += "\nHere are the examples for all user's inputs and the output I want you to output." \
                      f"\nFor \"{func_name}\" function: "
            for example_id, input_example in enumerate(available_functions[func_name]['gpt']['input_example']):
                if example_id != len(available_functions[func_name]['gpt']['input_example']) - 1:
                    prompt += f"user's input example {example_id + 1}: \"{input_example}\", " \
                              f"your output example based on " \
                              f"user's input example {example_id + 1}: " \
                              f"\"{available_functions[func_name]['gpt']['output_example'][example_id]}\";\n"
                else:
                    prompt += f"user's input example {example_id + 1}: \"{input_example}\", " \
                              f"your output example based on " \
                              f"user's input example {example_id + 1}: " \
                              f"\"{available_functions[func_name]['gpt']['output_example'][example_id]}\".\n"
    prompt += f"Use all the rules and examples listed above and determine your output for this user input: \"{text}\"." \
              f" Output only string with useful data (no ':', '\"' signs or 'Output' words)," \
              f"If you have a day and month in your output, style it in this way: Day Month " \
              f"(For example: 20 May; 15 July; 13 August). If you think that user's" \
              f"input doesn't suit any of the listed above functions, than output \"None\"\n\n"
    if show_prompt:
        print(f'[OPENAI PROMPT] {prompt}')
    return ask_gpt(prompt).replace('\n', '').replace('.', '').replace('"', '')


if __name__ == '__main__':
    funcs = src.utilities.helpers.available_functions
    inputs = [
        "Bot, tell me who is scheduled to work on the 30th of May.",
        "I need you to rearrange the support schedule. Maria should work on the 15th of "
        "June instead of Alex, who is set to work on the 10th of June.",
        "I need a coffee bot, but I'm lactose intolerant, so no milk please. And no sugar, I'm trying to cut down.",
        'Bot, can you switch the support schedule for Anna, who is supposed to work on the 21st of May, and James, '
        'who is supposed to work on the 22nd of May?'
    ]
    outputs = [
        'Get who is working at; 30 May',
        'Swap support schedule; Maria; 15 June; Alex; 10 June',
        "None",
        'Swap support schedule; Anna; 21 May; James; 22 May'
    ]

    for input_id, input_example in enumerate(inputs):
        print(f'{str("=") * 60}\nInput: {input_example}\nCode output: {choose_command(funcs, input_example)}.\n'
              f'Should be: {outputs[input_id]}\n{str("=") * 60}')
