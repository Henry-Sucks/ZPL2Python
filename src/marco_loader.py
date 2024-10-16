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


    # def get_module_name(self):
    #     return self.module_name

    # def get_import_not_built_ins_list(self):
    #     return self.import_not_built_ins_list


#     # 如果需要引用外部c++库的函数，利用pybind11进行引用
#     def add_bindings(self):
#         bindings_cpp_func_list = ""
#         cmakelists_set_func_path = ""
#         cmakelists_func_path_list = ""

#         for index, func in enumerate(self.not_built_in_func_list):
#             # 如果是外部定义的函数
#             # 假设外部库是非常规整的形式，i.e，所有源文件放在同一文件夹中并已经注册到同一头文件中
#             # 假设源文件中定义的函数名称与ZPL中函数名称相同

#             ## 向bindings.cpp中添加函数
#             ## 格式：m.def("A", &A, "A function that multiplies two numbers");
#             bindings_cpp_func_list += f'\tm.def("{func["py_name"]}", &{func["zpl_name"]}, "{func["description"]}");\n'
#             ## 向CMakeList中添加函数
#             ## 格式：set(a_path "/home/ZPL2Python/mylib/src/A.c++")
#             cmakelists_set_func_path += f'set({func["py_name"]}_path "{func["src"]}")\n'
#             ## 格式：add_library(funcs ${a_path} ${b_path})
#             cmakelists_func_path_list += f'${{{func["py_name"]}_path}} '

#         self.build_bindings_cpp(bindings_cpp_func_list)
#         cmakelists_add_path_to_lib = f'add_library(funcs {cmakelists_func_path_list})\n'
#         self.build_cmakelists(cmakelists_set_func_path, cmakelists_add_path_to_lib)

#         self.build_shell()
#         os.system(self.build_shell_path)

#     def build_cmakelists(self, cmakelists_set_func_path, cmakelists_add_path_to_lib):
#         cmakelists_code = """\
# cmake_minimum_required(VERSION 3.12)\n\
# project(zpl2python_project)\n\
# set(CMAKE_CXX_STANDARD 11)\n\
# set(CMAKE_CXX_STANDARD_REQUIRED ON)\n\
# find_package(pybind11 REQUIRED)\n\
# # 设置函数源文件的路径\n\
# {set_func_path}\
# # 使用变量来指定函数源文件\n\
# {add_path_to_lib}\
# # 设置include_path\n\
# include_directories({include_dir})\n\
# pybind11_add_module({module_name} bindings.cpp)\n\
# target_link_libraries({module_name} PRIVATE funcs)\n\
# """.format(set_func_path=cmakelists_set_func_path, add_path_to_lib=cmakelists_add_path_to_lib, include_dir=os.path.dirname(self.include_path), module_name=self.module_name)
        
#         # 写入bindings.cpp
#         with open(self.cmakelists_path, 'w', encoding='utf-8') as cmakelists:
#             cmakelists.write(cmakelists_code)

#     def build_bindings_cpp(self, bindings_cpp_func_list):
#         base_binding_cpp_basecode = """#include <pybind11/pybind11.h>\n\
# #include "{include_path}"\n\
# namespace py = pybind11;\n\
# PYBIND11_MODULE({module_name}, m){{\n\
# """.format(include_path=self.include_path, module_name=self.module_name)
        
#         # 写入bindings.cpp
#         bindings_cpp_code = base_binding_cpp_basecode + bindings_cpp_func_list + "}\n"
#         with open(self.bindings_cpp_path, 'w', encoding='utf-8') as bindings_cpp:
#             bindings_cpp.write(bindings_cpp_code)
        
#     def build_shell(self):
#         build_shell_code = """\
# mkdir -p build\n\
# cd build\n\
# export CMAKE_PREFIX_PATH=/usr/local/lib/python3.8/dist-packages:$CMAKE_PREFIX_PATH\n\
# cmake ..\n\
# cmake --build\n\
# cd build\n\
# make
# """
#         # 写入build.sh
#         with open(self.build_shell_path, 'w', encoding='utf-8') as build_shell:
#             build_shell.write(build_shell_code)

#         # 要执行，赋予权限
#         os.chmod(self.build_shell_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
        
        


if __name__ == '__main__':
    config_dir = '/home/ZPL2Python/config/'
    base_grammar_path = '/home/ZPL2Python/src/base_grammer.lark'

    loader = MacroLoader(config_dir, base_grammar_path)
    loader.load_config()
    print(loader.macro_list)
    # loader.add_grammar()






