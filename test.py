from lark import Lark
from src.transformer import TestTransformer
from src.function_loader import FunctionLoader

config_path = '/home/ZPL2Python/config/func_config.json'
base_grammar_path = '/home/ZPL2Python/src/grammer.lark'
include_path = '/home/ZPL2Python/mylib/include/mylib.h'

transformer = TestTransformer()
loader = FunctionLoader(config_path, base_grammar_path, transformer, include_path)
loader.load_config()
loader.add_bindings()
loader.add_grammar()
new_grammar_path = loader.get_new_grammar_path()
loader.add_transformer()


with open(new_grammar_path, 'r', encoding='utf-8') as file:
    test_grammer = file.read()
test_parser = Lark(test_grammer, start='start')

with open('test2.zpl', 'r') as file:
    text = file.read()



tree = test_parser.parse(text)
transformer.transform(tree)
ind_tree = transformer.get_ind_tree()
ind_tree.build_code()

# 如果调用了外部函数，在开头import
if transformer.called_has_not_built_in:
    import_code = f'from {loader.get_module_name()} import {transformer.get_called_not_built_in_list()}\n'
    final_code = import_code + ind_tree.get_code()
else:
    final_code = ind_tree.get_code()
# 打开文件并写入内容
with open('output.py', 'w') as f:  # 'w' 模式表示写入模式，如果文件不存在则创建
    print(final_code, file=f)
