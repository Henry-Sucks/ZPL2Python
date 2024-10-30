import json
import re
import time

# 读取JSON配置文件
with open('functions.json', 'r') as file:
    functions_config = json.load(file)

# 定义一个函数来生成唯一的变量名
def generate_unique_var(base_name):
    timestamp = int(time.time() * 1000)  # 获取当前时间戳
    return f"{base_name}_{timestamp}"

# 定义一个函数来解析BASIC代码并生成Python代码
def translate_basic_to_python(basic_code):
    python_code = []
    for line in basic_code.splitlines():
        if line.startswith("PRINT("):
            # 提取函数名和参数
            function_call = line.split('(')[1].split(')')[0]
            function_name, *args = function_call.split('(')
            args = [arg.strip() for arg in args[0].split(',')] if args else []

            # 查找函数定义
            if function_name in functions_config["functions"]:
                function_def = functions_config["functions"][function_name]
                input_vars = function_def["input"]
                temp_vars = function_def.get("temp_vars", [])
                output_var = generate_unique_var("result")
                code_template = function_def["code"]

                # 动态生成临时变量名
                unique_temp_vars = {temp_var: generate_unique_var(temp_var) for temp_var in temp_vars}

                # 替换代码模板中的占位符
                code = code_template
                for input_var, arg in zip(input_vars, args):
                    code = code.replace(f"{{{{input[{input_vars.index(input_var)}]}}}}", arg)
                for temp_var, unique_temp_var in unique_temp_vars.items():
                    code = code.replace(f"{{{{temp_vars[{temp_vars.index(temp_var)}]}}}}", unique_temp_var)

                # 替换返回值
                code = code.replace("return result", f"{output_var} = result")

                # 生成Python代码
                python_code.append(code)
                python_code.append(f"print({output_var})")

    # 将生成的Python代码拼接成一个字符串
    python_code_str = "\n".join(python_code)

    # 使用exec执行生成的Python代码
    print(python_code_str)

# 示例BASIC代码
basic_code = """
PRINT(FIELD(0))
PRINT(FIELD(1))
"""

# 调用函数进行翻译和执行
translate_basic_to_python(basic_code)