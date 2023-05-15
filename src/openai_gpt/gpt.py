from dotenv import load_dotenv
import os
import openai
import src.utilities.helpers

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
DEBUG = 1


def askGPT(prompt, show_output=0):
    response = openai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        temperature=1,
        max_tokens=40,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    if show_output:
        print(f'[OPENAI RESPONSE] {response.choices[0].text}')
    return response.choices[0].text


def choose_command(available_functions, text, show_prompt=1):
    # construction prompt
    prompt = 'Imagine that you are a bot, that outputs a string with a function name and arguments ' \
             'based on a user input. As a bot you have following functions available: '
    for index, func_name in enumerate(available_functions.keys()):
        if 'args' in available_functions[func_name]:
            prompt+=f'\"{func_name}'
            for arg_id, arg in enumerate(available_functions[func_name]['args']['names']):
                if arg_id!=len(available_functions[func_name]['args']['names'])-1:
                    prompt+=f'; {arg}'
                else:
                    prompt+=f'; {arg}\"'
            prompt+=', '
            # \"Make some coffee; milk; sugar\",
            for arg_id, arg in enumerate(available_functions[func_name]['args']['names']):
                if arg_id==0:
                    prompt+=f'where {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]}'
                elif arg_id != len(available_functions[func_name]['args']['names']) - 1:
                    prompt+=f', {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]} '
                else:
                    prompt+=f'and {arg} is {available_functions[func_name]["args"]["explanation"][arg_id]}; '
            # where milk is boolean (True) and sugar is boolean (False)
        else:
            prompt+=f'\"{func_name}\"; '

        # Add examples to GPT
        if 'input_example' in available_functions[func_name]['gpt']:
            prompt+="\nHere are the examples for all user's inputs and the output I want you to output." \
                    f"\nFor \"{func_name}\" function: "
            for example_id, input_example in enumerate(available_functions[func_name]['gpt']['input_example']):
                if example_id!=len(available_functions[func_name]['gpt']['input_example'])-1:
                    prompt+=f"user's input example {example_id+1}: {input_example}, your output example based on " \
                            f"user's input example {example_id+1}: " \
                            f"{available_functions[func_name]['gpt']['output_example']};\n"
                else:
                    prompt += f"user's input example {example_id + 1}: {input_example}, your output example based on " \
                              f"user's input example {example_id + 1}: " \
                              f"{available_functions[func_name]['gpt']['output_example']}.\n"
    prompt+=f"Use all the rules and examples listed above and determine your output for this user input: \"{text}\"." \
            f" Output only string with useful data (no ':', '\"' signs or 'Output' words\n"
    if show_prompt:
        print(f'[OPENAI PROMPT] {prompt}')
    #return askGPT(prompt).replace('\n', '')

funcs = src.utilities.helpers.available_functions
inputs = [
    "Bot, I need a coffee, no sugar, I'm on a diet, but with some milk please.",
    "Bot, tell me who is scheduled to work on the 30th of May.",
    "I need you to rearrange the support schedule. Maria should work on the 15th of "
    "June instead of Alex, who is set to work on the 10th of June.",
    "Bot, make me a plain coffee, no additives."
]
outputs = [
    'Make some coffee; True; False',
    'Get who is working at; 30th of May',
    'Swap support schedule; Maria; 15th of June; Alex; 10th of June',
    'Make some coffee; False; False'
]

for id, i in enumerate(inputs):
    print(f'{str("=")*60}\nInput: {i}\nCode output: {choose_command(funcs, i)}.\nShould be: {outputs[id]}\n{str("=")*60}')
