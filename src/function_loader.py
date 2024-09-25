import json

config_path = 'func_config.json'
grammar_path = 'grammer.lark'
include_path = '/home/ZPL2Python/mylib/include/mylib.h'

class FunctionLoader:
    def __init__(self, config_path, grammar_path, transformer):
        self.config_path = config_path
        self.grammar_path = grammar_path
        self.transformer = transformer
        self.func_list = []

        # 第三方库头文件的存放处
        # /home/ZPL2Python/mylib/include/mylib.h
        self.include_path = include_path
        # module name: lib.h -> lib
        self.module_name = self.from_path_get_module_name(self.include_path)


        # binding.cpp存放路径

        # CMakeLists相关路径
        
    


    # 从 /home/ZPL2Python/mylib/include/mylib.h 获得 mylib
    def from_path_get_module_name(self, path):
        module_name = path.split('/')[-1].split('.')[0]
        return module_name


    # 将config中定义的函数载入到字典中
    def load_config(self):
        with open(self.config_path, 'r', encoding='utf-8') as file:
            func_list = json.load(file)

        for func in func_list:
            self.func_list.append(func)

    # 如果需要引用外部c++库的函数，利用pybind11进行引用
    def add_binding(self):
        bindings_cpp_func_list = ""
        cmakelists_func_list = ""
        for func in self.func_list:
            if not func["is built-in"]:
                # 如果是外部定义的函数
                # 假设外部库是非常规整的形式，i.e，所有源文件放在同一文件夹中并已经注册到同一头文件中
                # 假设源文件中定义的函数名称与ZPL中函数名称相同

                ## 向bindings.cpp中添加函数
                ## 格式：m.def("A", &A, "A function that multiplies two numbers");
                bindings_cpp_func_list += f'\tm.def("{func["zpl_name"]}", &{func["zpl_name"]}, "{func["description"]}");\n'


    def get_cmakelists(self, ):
        cmakelists_base_code = """
cmake_minimum_required(VERSION 3.12)
project(zpl2python_project)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

add_library(funcs A.cpp B.cpp)
pybind11_add_module(your_module_name bindings.cpp)
target_link_libraries(your_module_name PRIVATE funcs)
"""


    def get_bindings_cpp(self, function_bindings):
        base_binding_cpp_basecode = """#include <pybind11/pybind11.h>\n\
#include "{include_path}"\n\
namespace py = pybind11;\n\
PYBIND11_MODULE({module_name}, m){{\n\
""".format(include_path=self.include_path, module_name=self.module_name)
        
        ## 写入bindings.cpp
        ## 默认bindings.cpp在同一个原目录下
        bindings_cpp_code = base_binding_cpp_basecode + function_bindings + "}\n"
        with open('bindings.cpp', 'w', encoding='utf-8') as bindings_cpp:
            bindings_cpp.write(bindings_cpp_code)
        


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
    loader.load_config()
    loader.add_binding()
    # loader.add_grammar()

            






