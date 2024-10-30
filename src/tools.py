import ast

def modify_config(config_path, var_name, new_value):
    # 1. 读取 config 文件内容
    with open(config_path, 'r') as file:
        config_content = file.read()

    # 2. 解析文件内容为 Python 代码
    config_module = ast.parse(config_content)

    # 3. 遍历 AST 并找到指定的变量
    for node in config_module.body:
        if isinstance(node, ast.Assign) and len(node.targets) == 1:
            target = node.targets[0]
            if isinstance(target, ast.Name) and target.id == var_name:
                # 修改变量的值
                node.value = ast.Constant(value=new_value)

    # 4. 将修改后的 AST 转换回代码字符串
    modified_config_content = ast.unparse(config_module)

    # 5. 将修改后的内容写回 config 文件
    with open(config_path, 'w') as file:
        file.write(modified_config_content)

def error_handler(something):
    print(something)


def print_to_file(file_name, content):
    with open(file_name, 'a') as f:
        f.write(content + '\n')