from macro_loader import MacroLoader
from tools import modify_config

macros_path = '../macros'
config_path = "config.py"
base_grammar_path = 'base_grammer.lark'

loader = MacroLoader(macros_path, base_grammar_path)
loader.load_config()
loader.add_grammar()
new_grammar_path = loader.get_new_grammar_path()
modify_config(config_path, 'grammar_path', new_grammar_path)