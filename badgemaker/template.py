import pandas as pd
import json

def load_configuration():
    with open('config.json', 'r') as f:
        return json.load(f)

def choose_template(row, config):
    for rule in config['rules']:
        if eval(rule['condition'], {'row': row}):
            return rule['template']
    return None

#for index, row in data.iterrows():
    #template = choose_template(row, config)
    #if template:
    #    print(f"Selected template for row {index}: {template}")
    #else:
    #    print(f"No matching template found for row {index}.")
