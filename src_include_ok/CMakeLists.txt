# cmake_minimum_required(VERSION 3.4)
# project(example)

# # 设置 C++ 标准
# set(CMAKE_CXX_STANDARD 14)
# set(CMAKE_CXX_STANDARD_REQUIRED ON)

# # 找到 pybind11
# find_package(pybind11 REQUIRED)


# # 添加 C++ 源文件
# set(SOURCES
#     # 1-example.cpp 
#     2-example.cpp 
# )

# # 创建 Python 扩展模块
# pybind11_add_module(example ${SOURCES})

#----------------------------------------add include/ and src/ test use 2-test.py
cmake_minimum_required(VERSION 3.12)
project(example_project)

# 设置 C++ 标准
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# 添加位置无关代码选项
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# 找到 pybind11 包
find_package(pybind11 REQUIRED)

# 添加 include 目录
include_directories(include)


# 添加库目录
add_library(example_lib
    src/example.cpp
    src/calculator.cpp
)

# 创建 Python 模块
pybind11_add_module(example src/bindings.cpp)

# 链接库
target_link_libraries(example PRIVATE example_lib)