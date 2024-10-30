import ast
class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        """
        初始化 CodeVisitor 类。

        属性:
        - inputs: 存储输入参数的列表。
        - temp_vars: 存储临时变量的列表。
        - output: 存储输出变量的列表。
        - current_var: 当前处理的变量名。
        - defined_vars: 存储已定义变量的集合。
        - imported_modules: 存储导入模块的集合。
        """
        self.inputs = []
        self.temp_vars = []
        self.output = []
        self.current_var = None
        self.defined_vars = set()
        self.imported_modules = set()

    def visit_Import(self, node):
        """
        处理导入语句。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 遍历导入的模块名称，并将其添加到导入模块集合中。
        2. 递归访问子节点。
        """
        for alias in node.names:
            self.imported_modules.add(alias.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        """
        处理赋值语句。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 遍历赋值语句的目标变量。
        2. 如果目标变量是 ast.Name 类型，将其添加到已定义变量集合中。
        3. 递归访问子节点。
        """
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.defined_vars.add(target.id)
                self.current_var = target.id
                self.temp_vars.append(target.id)
        self.generic_visit(node)

    def visit_Name(self, node):
        """
        处理名称节点。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 如果名称节点未在已定义变量集合中且不是导入的模块名称，将其添加到输入参数列表中。
        2. 递归访问子节点。
        """
        if node.id not in self.defined_vars and node.id not in self.imported_modules:
            self.inputs.append(node.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        """
        处理函数调用。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 如果函数调用的目标是属性（如 obj.method()），将当前变量添加到临时变量列表中。
        2. 遍历参数列表，将常量参数添加到输入参数列表中。
        3. 递归访问子节点。
        """
        if isinstance(node.func, ast.Attribute):
            if self.current_var:
                self.temp_vars.append(self.current_var)
            self.current_var = None
        for arg in node.args:
            if isinstance(arg, ast.Constant):
                self.inputs.append(arg.value)
        self.generic_visit(node)

    def visit_Expr(self, node):
        """
        处理表达式。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 如果表达式是函数调用，递归处理函数调用。
        2. 递归访问子节点。
        """
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
        self.generic_visit(node)

    def visit_Return(self, node):
        """
        处理返回语句。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 如果返回值是名称（如 field_data），将其添加到输出变量列表中。
        2. 递归访问子节点。
        """
        if isinstance(node.value, ast.Name):
            self.output.append(node.value.id)
        self.generic_visit(node)

    def visit_Module(self, node):
        """
        处理模块。

        参数:
        - node: 当前处理的 AST 节点。

        实现细节:
        1. 递归访问子节点。
        2. 对临时变量列表和输入参数列表进行去重。
        """
        self.generic_visit(node)
        self.temp_vars = list(set(self.temp_vars))  # 去重
        self.inputs = list(set(self.inputs))  # 去重

def add_braces_to_vars(code, vars_list):
    """
    在代码中对应的变量名外加两对大括号（{{}}）。

    参数:
    - code: 源代码字符串。
    - vars_list: 包含变量名的列表。

    返回:
    - 替换后的代码字符串。
    """
    import re
    for var in vars_list:
        # 使用正则表达式匹配变量名，并确保不会出现错误的匹配情形
        pattern = r'\b' + re.escape(var) + r'\b'
        code = re.sub(pattern, f'{{{{{var}}}}}', code)
    return code

def record_code_with_escapes(code):
    """
    记录代码的换行与缩进，并转换成一串包含转义符的字符串。

    参数:
    - code: 源代码字符串。

    返回:
    - 包含转义符的字符串。
    """
    lines = code.split('\n')
    escaped_code = []

    for line in lines:
        # 记录换行符
        escaped_code.append('\\n')
        # 记录缩进
        indent = len(line) - len(line.lstrip())
        escaped_code.append('\\t' * indent)
        # 记录行内容
        escaped_code.append(line.strip())

    return ''.join(escaped_code)





code = """
import example
if input1 > 1:
    temp = input1 * input2
else:
    temp = input1 + input2
api = example.CSeeodAPI()
pro1 = api.get_field()
field_data = api.get_field_data(temp, input3, api)
return field_data
"""

tree = ast.parse(code)


visitor = CodeVisitor()
visitor.visit(tree)

print("Input:", visitor.inputs)
print("Temp Vars:", visitor.temp_vars)
print("Output:", visitor.output)

# 替换输入变量名
code_with_braces = add_braces_to_vars(code, visitor.inputs)

# 替换临时变量名
code_with_braces = add_braces_to_vars(code_with_braces, visitor.temp_vars)

# 替换输出变量名
code_with_braces = add_braces_to_vars(code_with_braces, visitor.output)

print(code_with_braces)

# 记录代码的换行与缩进，并转换成一串字符串
escaped_code = record_code_with_escapes(code_with_braces)

print(escaped_code)