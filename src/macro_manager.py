import os
import json


def load_macros_from_folder(folder_path):
    macros = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            with open(os.path.join(folder_path, filename), "r") as file:
                macro_list = json.load(file)
                for macro in macro_list:
                    macros.append(macro)
    return macros

def build_macro_dict(macros_data):
    macro_dict = {}
    for macro in macros_data:
        macro_dict[macro['zpl_name']] = macro
    return macro_dict

def save_macro_dict(macro_dict, file_path):
    with open(file_path, 'w') as f:
        json.dump(macro_dict, f, indent=4)


folder_path = "../macros"
macros_data = load_macros_from_folder(folder_path)
macro_dict = build_macro_dict(macros_data)
save_macro_dict(macro_dict, f"{folder_path}/macro_dict.json")
