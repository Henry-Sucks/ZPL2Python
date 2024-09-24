import json

config_path = 'func_config.json'
grammar_path = 'grammer.lark'

class FunctionLoader:
    def __init__(self, config_path, grammar_path, transformer):
        self.config_path = config_path
        self.grammar_path = grammar_path
        self.transformer = transformer
        self.func_list = []

    # 将config中定义的函数载入到字典中
    def load(self):
        with open(self.config_path, 'r', encoding='utf-8') as file:
            func_list = json.load(file)

        for func in func_list:
            self.func_list.append(func)

    # 向语法注入函数处理
    def add_grammar(self):
        gram_header = "\n//// 函数返回值\n"
        gram_func_ret = "func_ret: "
        tab_count = "\t"
        gram_func_list = ""

        for i, func in enumerate(self.func_list):
            func_name = func['zpl_name']
            func_header = f"{func_name.lower()}_func"
            
            gram_func_ret += f"{func_header}\n"
            if len(self.func_list) > 1 and i < len(self.func_list) - 1:
                gram_func_ret += f"{tab_count}| "

            gram_func_list += f"{func_header}: \"{func_name}\" \"(\" expression_list \")\"\n"

        gram_body = f"{gram_func_ret}\n{gram_func_list}"
        gram_txt = gram_header + gram_body

        with open(self.grammar_path, 'a', encoding='utf-8') as file:
            file.write(gram_txt)


    # 向transformer注入函数处理
    # 问题：是动态地添加方法好？还是静态地添加方法好？
    def add_transformer(self):
        for func in self.func_list:
            self.transformer.create_func_method(func['zpl_name'].lower(), func['py_name'])

        
        





            

            

            

            



if __name__ == "__main__":
    loader = FunctionLoader(config_path, grammar_path, "")
    loader.load()
    loader.add_grammar()

            






