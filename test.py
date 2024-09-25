from lark import Lark
from ZPL2Python.src.transformer import TestTransformer
from ZPL2Python.src.function_loader import FunctionLoader

config_path = 'func_config.json'
grammar_path = 'grammer.lark'

transformer = TestTransformer()
loader = FunctionLoader(config_path, grammar_path, transformer)
loader.load_config()
loader.add_grammar()
loader.add_transformer()


with open('grammer.lark', 'r', encoding='utf-8') as file:
    test_grammer = file.read()
test_parser = Lark(test_grammer, start='start')

with open('test.zpl', 'r') as file:
    text = file.read()



tree = test_parser.parse(text)
transformer.transform(tree)
ind_tree = transformer.get_ind_tree()
ind_tree.build_code()


# 打开文件并写入内容
with open('output.py', 'w') as f:  # 'w' 模式表示写入模式，如果文件不存在则创建
    print(ind_tree.get_code(), file=f)