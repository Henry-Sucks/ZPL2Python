from lark import Lark
from transformer import ZPLTransformer
import config as config

config_path = 'config'
base_grammar_path = config.grammar_path

def translate(input_code):
    with open(base_grammar_path, 'r', encoding='utf-8') as file:
        test_grammer = file.read()

    test_parser = Lark(test_grammer, start='start')

    tree = test_parser.parse(input_code)
    transformer = ZPLTransformer(config_path)
    transformer.transform(tree)
    ind_tree = transformer.get_ind_tree()
    ind_tree.build_code()

    final_code = ind_tree.get_code()

    return final_code