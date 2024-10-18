from lark import Lark
from src.transformer import ZPLTransformer
from src.macro_loader import MacroLoader

config_path = '/home/ZPL2Python/config'
base_grammar_path = '/home/ZPL2Python/src/base_grammer.lark'

loader = MacroLoader(config_path, base_grammar_path)
loader.load_config()
loader.add_grammar()
new_grammar_path = loader.get_new_grammar_path()


with open(new_grammar_path, 'r', encoding='utf-8') as file:
    test_grammer = file.read()
test_parser = Lark(test_grammer, start='start')

with open('test2.zpl', 'r') as file:
    text = file.read()


tree = test_parser.parse(text)
transformer = ZPLTransformer(config_path)
# transformer.build_transformer()
transformer.transform(tree)
# ind_tree = transformer.get_ind_tree()
# ind_tree.build_code()

# # 如果调用了外部函数，在开头import
# final_code = transformer.get_import_code() + '\n' + ind_tree.get_code()

# # 打开文件并写入内容
# with open('output.py', 'w') as f:  # 'w' 模式表示写入模式，如果文件不存在则创建
#     print(final_code, file=f)

