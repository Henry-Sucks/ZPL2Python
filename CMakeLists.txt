cmake_minimum_required(VERSION 3.12)
project(zpl2python_project)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(pybind11 REQUIRED)

# 设置A.cpp和B.cpp的路径
set(a_path "/home/ZPL2Python/mylib/src/A.c++")
set(b_path "/home/ZPL2Python/mylib/src/B.c++")
# 使用变量来指定源文件
add_library(funcs ${a_path} ${b_path})

# 设置include_path
include_directories(/home/ZPL2Python/mylib/include)


pybind11_add_module(mylib bindings.cpp)
target_link_libraries(mylib PRIVATE funcs)
