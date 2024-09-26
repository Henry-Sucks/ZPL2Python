import json
import os
import stat

class FunctionLoader:
    def __init__(self, config_path, grammar_path, transformer, include_path):
        self.config_path = config_path
        self.grammar_path = grammar_path
        self.transformer = transformer
        self.func_list = []
        self.not_built_in_func_list = []
        self.has_not_built_ins = False

        # 第三方库头文件的存放处
        # /home/ZPL2Python/mylib/include/mylib.h
        self.include_path = include_path
        # module name: lib.h -> lib
        self.module_name = self.from_path_get_module_name(self.include_path)


        # binding.cpp存放路径
        self.bindings_cpp_path = 'bindings.cpp'

        # CMakeLists存放路径
        self.cmakelists_path = 'CMakeLists.txt'

        # build.shell存放路径
        self.build_shell_path = './build.sh'

        # 便于transformer import的制作的字符串
        self.import_not_built_ins_list = ""
    


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
            if not func['is built-in']:
                self.not_built_in_func_list.append(func)
                self.has_not_built_ins = True


    # 如果需要引用外部c++库的函数，利用pybind11进行引用
    def add_bindings(self):
        bindings_cpp_func_list = ""
        cmakelists_set_func_path = ""
        cmakelists_func_path_list = ""

        for index, func in enumerate(self.not_built_in_func_list):
            # 如果是外部定义的函数
            # 假设外部库是非常规整的形式，i.e，所有源文件放在同一文件夹中并已经注册到同一头文件中
            # 假设源文件中定义的函数名称与ZPL中函数名称相同

            ## 向bindings.cpp中添加函数
            ## 格式：m.def("A", &A, "A function that multiplies two numbers");
            bindings_cpp_func_list += f'\tm.def("{func["py_name"]}", &{func["zpl_name"]}, "{func["description"]}");\n'
            ## 向CMakeList中添加函数
            ## 格式：set(a_path "/home/ZPL2Python/mylib/src/A.c++")
            cmakelists_set_func_path += f'set({func["py_name"]}_path "{func["src"]}")\n'
            ## 格式：add_library(funcs ${a_path} ${b_path})
            cmakelists_func_path_list += f'${{{func["py_name"]}_path}} '

            ## 格式 from xx import a, b
            self.import_not_built_ins_list += func["py_name"]
            if index < len(self.not_built_in_func_list) - 1:
                self.import_not_built_ins_list += ', '
            


        self.build_bindings_cpp(bindings_cpp_func_list)
        cmakelists_add_path_to_lib = f'add_library(funcs {cmakelists_func_path_list})\n'
        self.build_cmakelists(cmakelists_set_func_path, cmakelists_add_path_to_lib)

        self.build_shell()
        os.system(self.build_shell_path)

    def build_cmakelists(self, cmakelists_set_func_path, cmakelists_add_path_to_lib):
        cmakelists_code = """\
cmake_minimum_required(VERSION 3.12)\n\
project(zpl2python_project)\n\
set(CMAKE_CXX_STANDARD 11)\n\
set(CMAKE_CXX_STANDARD_REQUIRED ON)\n\
find_package(pybind11 REQUIRED)\n\
# 设置函数源文件的路径\n\
{set_func_path}\
# 使用变量来指定函数源文件\n\
{add_path_to_lib}\
# 设置include_path\n\
include_directories({include_dir})\n\
pybind11_add_module({module_name} bindings.cpp)\n\
target_link_libraries({module_name} PRIVATE funcs)\n\
""".format(set_func_path=cmakelists_set_func_path, add_path_to_lib=cmakelists_add_path_to_lib, include_dir=os.path.dirname(self.include_path), module_name=self.module_name)
        
        # 写入bindings.cpp
        with open(self.cmakelists_path, 'w', encoding='utf-8') as cmakelists:
            cmakelists.write(cmakelists_code)

    def build_bindings_cpp(self, bindings_cpp_func_list):
        base_binding_cpp_basecode = """#include <pybind11/pybind11.h>\n\
#include "{include_path}"\n\
namespace py = pybind11;\n\
PYBIND11_MODULE({module_name}, m){{\n\
""".format(include_path=self.include_path, module_name=self.module_name)
        
        # 写入bindings.cpp
        bindings_cpp_code = base_binding_cpp_basecode + bindings_cpp_func_list + "}\n"
        with open(self.bindings_cpp_path, 'w', encoding='utf-8') as bindings_cpp:
            bindings_cpp.write(bindings_cpp_code)
        
    def build_shell(self):
        build_shell_code = """\
mkdir -p build\n\
cd build\n\
export CMAKE_PREFIX_PATH=/usr/local/lib/python3.8/dist-packages:$CMAKE_PREFIX_PATH\n\
cmake ..\n\
cmake --build\n\
cd build\n\
make
"""
        # 写入build.sh
        with open(self.build_shell_path, 'w', encoding='utf-8') as build_shell:
            build_shell.write(build_shell_code)

        # 要执行，赋予权限
        os.chmod(self.build_shell_path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

    # 得到新的grammar path
    def generate_new_grammar_path(self):
        grammar_dir_path = os.path.dirname(self.grammar_path)
        grammar_filename, grammar_extension = os.path.splitext(os.path.basename(self.grammar_path))

        grammar_filename += '_1'

        self.grammar_path = grammar_dir_path + '/' + grammar_filename + grammar_extension

    def get_new_grammar_path(self):
        return self.grammar_path


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

        with open(self.grammar_path, 'r', encoding='utf-8') as file:
            gram_basecode = file.read()
        gram_txt = gram_basecode + '\n' + gram_txt
        self.generate_new_grammar_path()
        with open(self.grammar_path, 'a', encoding='utf-8') as file:
            file.write(gram_txt)


    # 向transformer注入函数处理
    # 问题：是动态地添加方法好？还是静态地添加方法好？
    def add_transformer(self):
        for func in self.func_list:
            if func in self.not_built_in_func_list:
                self.transformer.create_not_built_in_func_method(func['zpl_name'].lower(), func['py_name'])
            else:
                self.transformer.create_built_in_func_method(func['zpl_name'].lower(), func['py_name'])



    def get_module_name(self):
        return self.module_name

    def get_import_not_built_ins_list(self):
        return self.import_not_built_ins_list
        
        


            






