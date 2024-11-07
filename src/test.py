from lark import Lark
from transformer import ZPLTransformer
import config as config


config_path = 'config'
base_grammar_path = config.grammar_path

# loader = MacroLoader(config_path, base_grammar_path)
# loader.load_config()
# loader.add_grammar()
# new_grammar_path = loader.get_new_grammar_path()

with open(base_grammar_path, 'r', encoding='utf-8') as file:
    test_grammer = file.read()


test_parser = Lark(test_grammer, start='start')

with open('test2.zpl', 'r') as file:
    text = file.read()


tree = test_parser.parse(text)
transformer = ZPLTransformer(config_path)
transformer.transform(tree)
ind_tree = transformer.get_ind_tree()
ind_tree.build_code()

final_code = ind_tree.get_code()

# 打开文件并写入内容
with open('output.py', 'w') as f:  # 'w' 模式表示写入模式，如果文件不存在则创建
    print(final_code, file=f)