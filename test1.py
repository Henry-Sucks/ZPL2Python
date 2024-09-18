from lark import Lark, Transformer

# 定义 BASIC 语法
basic_grammar = """
?start: statements
statements: statement+
statement: assignment_stmt
         | print_stmt
assignment_stmt: ID EQUAL NUMBER
print_stmt: "PRINT" ID

ID: CNAME
EQUAL: "="
%import common.CNAME
%import common.NUMBER -> NUMBER
%import common.WS
%ignore WS
"""

# 创建 Lark 解析器
basic_parser = Lark(basic_grammar, start='start')

# 定义转换器
class BasicTransformer(Transformer):
    def __init__(self):
        self.vars = {}

    def ID(self, token):
        return token

    def NUMBER(self, token):
        return float(token)

    def assignment_stmt(self, items):
        var, hey, val = items
        self.vars[var] = val
        print(hey)
        return var

    def print_stmt(self, items):
        var = items[0]
        print(self.vars[var])
# BASIC 语句
basic_code = """
s = 2
PRINT s
"""

# 解析 BASIC 语句
tree = basic_parser.parse(basic_code)
# print(tree.pretty())

# 转换和执行
transformer = BasicTransformer()
transformer.transform(tree)
