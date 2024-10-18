import json
import os
import stat

class MacroLoader:
    def __init__(self, config_dir, base_grammar_path):
        self.config_dir = config_dir
        self.base_grammar_path = base_grammar_path
        self.new_grammar_path = ''
        self.macro_list = []

    # 将config中定义的函数载入到字典中
    def load_config(self):
        for filename in os.listdir(self.config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.config_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    config_data = json.load(file)
                    for macro in config_data.get('macros', []):
                        self.macro_list.append(macro)
        


                
    # 得到新的grammar path
    def generate_new_grammar_path(self, version=1):
        grammar_dir_path = os.path.dirname(self.base_grammar_path)
        grammar_filename, grammar_extension = os.path.splitext(os.path.basename(self.base_grammar_path))
        # 生成新文件名，加上递增的版本号
        grammar_filename += f'_{version}'
        new_grammar_path = os.path.join(grammar_dir_path, grammar_filename + grammar_extension)
        
        # 如果文件已存在，递归增加版本号
        if os.path.exists(new_grammar_path):
            return self.generate_new_grammar_path(version + 1)
        else:
            return new_grammar_path

    def get_new_grammar_path(self):
        return self.new_grammar_path

    # 向语法注入宏处理
    def add_grammar(self):
        if not self.macro_list:
            raise RuntimeError("宏函数列表为空，请先调用 load_config 进行加载！")
    

        # 生成语法注入部分
        gram_header = "\n//// 宏返回值\n"
        gram_macro_ret = "macro_ret: "
        tab_count = "\t"
        gram_macro_list = ""

        for i, macro in enumerate(self.macro_list):
            macro_name = macro['zpl_macro']  # 使用 'zpl_macro' 表示 ZPL 宏名称
            macro_header = f"{macro_name.lower()}_macro"
            
            gram_macro_ret += f"{macro_header}\n"
            if len(self.macro_list) > 1 and i < len(self.macro_list) - 1:
                gram_macro_ret += f"{tab_count}| "

            gram_macro_list += f'{macro_header}: "{macro_name}" "(" expression_list ")"\n'

        gram_body = f"{gram_macro_ret}\n{gram_macro_list}"
        gram_txt = gram_header + gram_body

        # 读取基础语法文件
        with open(self.base_grammar_path, 'r', encoding='utf-8') as file:
            gram_basecode = file.read()

        # 合并基础语法和宏定义
        gram_txt = gram_basecode + '\n' + gram_txt

        # 生成新的语法文件路径，防止覆盖
        new_grammar_path = self.generate_new_grammar_path()
        self.new_grammar_path = new_grammar_path

        # 将新的语法写入到新文件中
        with open(new_grammar_path, 'w', encoding='utf-8') as file:
            file.write(gram_txt)
        
        


if __name__ == '__main__':
    config_dir = '/home/ZPL2Python/config/'
    base_grammar_path = '/home/ZPL2Python/src/base_grammer.lark'

    loader = MacroLoader(config_dir, base_grammar_path)
    loader.load_config()
    loader.add_grammar()






