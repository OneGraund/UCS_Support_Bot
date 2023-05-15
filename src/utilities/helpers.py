import src.google_sheets.api

available_functions = {
    'Swap support schedule': {
        'func': src.google_sheets.api.swap_support,
        'args': {
            'names': ['employee1', 'date1', 'employee2', 'date2'],
            'explanation': [
                'Name of first employee that wants to change',
                'Date when employee one had to support',
                'Name of second employee that is going to change with the first one',
                'Date when employee two had to support'
            ]
        },
        'gpt': {
            'input_example': ['Bot, swap support schedule of Yaro, who should support'
                             ' at this Thursday and Vova, who should support at this'
                             ' Monday',
                              'Hey, bot! Could you please swap support schedule of Vova, who will support at '
                              'Sunday and Egor, who will support at Saturday'],
            'output_example': ['Swap support schedule; Yaro; Thursday; Vova; Monday',
                               'Swap support schedule; Vova; Sunday; Egor; Saturday']
        }
    },
    'Get who is working at': {
        'func': src.google_sheets.api.get_who_is_working,
        'args': {
            'names': ['date'],
            'explanation': ['date of when we want to look up who is working']
        },
        'gpt': {
            'input_example': 'Bot, who is working this Monday?',
            'output_example': 'Get who is working; this Monday'
        }
    }
}

def call_function(function_name, *args, **kwargs):
    function = available_functions.get(function_name)
    if function is not None:
        function(*args, **kwargs)
    else:
        print(f'[HELPERS] No function found for name {function_name}')