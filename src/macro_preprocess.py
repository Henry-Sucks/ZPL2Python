import ast
class CodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.inputs = []
        self.temp_vars = []
        self.output = None
        self.current_var = None

    def visit_Assign(self, node):
        # 处理赋值语句
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.current_var = target.id
                self.temp_vars.append(target.id)
        self.generic_visit(node)

    def visit_Call(self, node):
        # 处理函数调用
        if isinstance(node.func, ast.Attribute):
            if self.current_var:
                self.temp_vars.append(self.current_var)
            self.current_var = None
        elif isinstance(node.func, ast.Name) and node.func.id == 'api':
            for arg in node.args:
                if isinstance(arg, ast.Constant):
                    self.inputs.append(arg.value)
        self.generic_visit(node)

    def visit_Expr(self, node):
        # 处理表达式
        if isinstance(node.value, ast.Call):
            self.visit_Call(node.value)
        self.generic_visit(node)

    def visit_Return(self, node):
        # 处理返回语句
        if isinstance(node.value, ast.Name):
            self.output = node.value.id
        self.generic_visit(node)

    def visit_Module(self, node):
        # 处理模块
        self.generic_visit(node)
        self.temp_vars = list(set(self.temp_vars))  # 去重



code = """
import example
api = example.CSeeodAPI()
pro1 = api.get_field()
field_data = api.get_field_data(pro1, 0)
"""

tree = ast.parse(code)


visitor = CodeVisitor()
visitor.visit(tree)

print("Input:", visitor.inputs)
print("Temp Vars:", visitor.temp_vars)
print("Output:", visitor.output)