from lark import Transformer
import json
import os
from ind_tree_node import IndTreeNode
from tools import error_handler
import config

class Symbol:
    def __init__(self, symbol_type, element_type=None, value=None, dimensions=None, code=None):
        self.symbol_type = symbol_type  # CONST / VAR / ARRAY / ARRAY_ELEMENT / EXP / NONE / MACRO(不会暴露出来，在EXP中处理)
        self.element_type = element_type  # INT / DOUBLE / STRING / NONE
        self.value = value # 定义：插入源代码的部分
        self.dimensions = dimensions
        self.code = code # 针对ARRAY_ELEMENT / EXP / MACRO 赋值前需要执行的代码

    def __str__(self):
        if self.symbol_type == "CONST":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, value={self.value})"
        elif self.symbol_type == "VAR":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, value={self.value})"
        elif self.symbol_type == "ARRAY":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, dimensions={self.dimensions})"
        elif self.symbol_type == "ARRAY_ELEMENT":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, code={self.code})"
        elif self.symbol_type == "MACRO":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, code={self.code})"
        elif self.symbol_type == "EXP":
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type}, code={self.code})"
        else:
            return f"Symbol(type={self.symbol_type}, element_type={self.element_type})"
    
class GlobalSymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, symbol):
        if symbol.name in self.symbols:
            error_handler(f"Symbol '{symbol.name}' already exists.")
            raise ValueError(f"Symbol '{symbol.name}' already exists.")
        self.symbols[symbol.name] = symbol

    def is_symbol_exist(self, name):
        return name in self.symbols

    def get_symbol(self, name):
        if name not in self.symbols:
            return None
        return self.symbols[name]
    
    def remove_symbol(self, name):
        if name not in self.symbols:
            error_handler(f"Symbol '{name}' does not exist.")
            raise ValueError(f"Symbol '{name}' does not exist.")
        del self.symbols[name]

    def __str__(self):
        return str(self.symbols)
    
"""
    工具函数
"""
# 判断数是INT还是DOUBLE
def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

# 将子节点的code根据先后顺序拼接到一起
def concat_code_segments(segments):
    result = []
    for segment in segments:
        if segment is not None:
            result.append(segment)
    
    # 如果所有片段都为 None或空字符串，则返回None
    if not result:
        return None
    
    # 使用 '\n' 拼接所有非 None 的片段
    concatenated_code = '\n'.join(result)

    # 检查最后一个字符是否为 '\n'，如果不是，则添加一个 '\n'
    if concatenated_code[-1] != '\n':
        concatenated_code += '\n'
    
    return concatenated_code

def process_temp_var_name(var_list):
    """
    将临时变量名进行处理，生成运行时临时变量名。

    参数:
    var_list (list): 包含原始临时变量名的列表。

    返回:
    dict: 包含原始临时变量名和对应运行时临时变量名的字典。

    示例:
    输入: ['api', 'pro1']
    输出: {'api': 'api_1a2b3c4d', 'pro1': 'pro1_5e6f7g8h'}

    实现细节:
    1. 使用 uuid.uuid4().hex 生成唯一的随机字符串。
    2. 将原始临时变量名与生成的随机字符串组合，生成新的运行时临时变量名。
    3. 返回一个字典，键为原始临时变量名，值为对应的运行时临时变量名。
    """
    import uuid
    temp_vars = {var: f'{var}_{uuid.uuid4().hex}' for var in var_list}
    return temp_vars

def is_type_match(defined_type, actual_type):
    if defined_type == "INT":
        return actual_type == "INT"
    elif defined_type == "DOUBLE":
        return actual_type in ["INT", "DOUBLE"]

def parse_symbol(symbol):
    pass
    

"""
    工具函数结束
"""

class ZPLTransformer(Transformer):
    def __init__(self, config_dir):
        self.vars = {}
        self.code = ""
        self.top_ind_tree = IndTreeNode("")

        self.config_dir = config_dir
        self.macro_list = []
        self.compiled_macro_list = []

        self.global_symbol_table = GlobalSymbolTable()


    """
    value：数字、变量名、函数调用、字符串
    """ 
    def value(self, item):
        return item[0]

    def num(self, n):
        if(is_int(n[0].value)):
            symbol = Symbol("CONST", element_type="INT", value=n[0].value)
        else:
            symbol = Symbol("CONST", element_type="DOUBLE", value=n[0].value)
        return symbol
    
    def string(self, str):
        symbol = Symbol("CONST", element_type="STRING", value=str[0][1:-1])
        print(f"String: {str[0][1:-1]}")
        return symbol
    
    def id_var(self, items):
        var_name = items[0]
        if(len(items) > 1):
            if(items[1] == '$'):
                # STRING
                symbol = Symbol("VAR", element_type="STRING", name=var_name)
            else:
                # ARRAY_ELEMENT:
                # TODO: 无法报index超出范围的错误？

                # 获取数组名
                array_name = var_name


                array_symbol = self.global_symbol_table.get_symbol(array_name)
                if not array_symbol:
                    # 检查数组未定义错误
                    error_handler(f"Array '{array_name}' is not defined.")
                    raise ValueError(f"Array '{array_name}' is not defined.")

                array_dimensions = array_symbol.dimensions
                array_type = array_symbol.element_type

                # 检查数组维数
                if(len(items) - 1 != array_dimensions):
                    error_handler(f"Array '{array_name}' has {array_dimensions} dimensions, but {len(items) - 1} indices were provided.")
                    raise ValueError(f"Array '{array_name}' has {array_dimensions} dimensions, but {len(items) - 1} indices were provided.")
                
                # 检查数组种类（无法做到）

                # 获取index列表
                array_indice = items[1:]
                # 解析index列表，生成value和code
                array_value = array_name+"["
                array_code = ""

                for index in array_indice:
                    value = index.value
                    code = index.code
                    array_value += value + ','
                    array_code += code

                if array_value:
                    array_value = array_value[:-1]
                    array_value += "]"
                
                symbol = Symbol("ARRAY_ELEMENT",element_type=array_type, dimensions=array_dimensions, value=array_value, code=array_code)

        else:
            # 此处无法确定是VAR/ARRAY, INT/DOUBLE
            symbol = Symbol(None, None, value=var_name)
        return symbol
    
    """
    表达式
    """ 
    def evaluate_expression_type(self, operator, *types):
        """
        根据运算符和操作数类型，评估表达式的结果类型以及是否出错。
        如果出错，调用error_handler函数处理错误。
        参数:
        - operator: 包括一元和二元运算符，如 '+'、'-'、'*'、'/' 等。
        - *types: 操作EXP的类型，可以是一个或两个。可以是"INT"，"DOUBLE"，"STRING"

        返回:
        - result_type: 表达式的结果类型。
        - error: 是否出错，True 表示出错，False 表示没有出错。
        """

        # 定义运算符的类型检查规则
        type_rules_uni = {
            # 一元运算符
            '!': {
                ("INT", ): "INT",
                ("DOUBLE", ): "DOUBLE"
            },
            '-': {
                ("INT", ): "INT",
                ("DOUBLE", ): "DOUBLE"
            },
        }
        type_rules_bi = {
            # 二元运算符
            '+': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "DOUBLE",
                ("INT", "DOUBLE"): "DOUBLE",
                ("DOUBLE", "INT"): "DOUBLE",
                ("STRING", "STRING"): "STRING",
            },
            '-': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "DOUBLE",
                ("INT", "DOUBLE"): "DOUBLE",
                ("DOUBLE", "INT"): "DOUBLE",
            },
            '*': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "DOUBLE",
                ("INT", "DOUBLE"): "DOUBLE",
                ("DOUBLE", "INT"): "DOUBLE",
            },
            '/': {
                ("INT", "INT"): "DOUBLE",
                ("DOUBLE", "DOUBLE"): "DOUBLE",
                ("INT", "DOUBLE"): "DOUBLE",
                ("DOUBLE", "INT"): "DOUBLE",
            },
            '&': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '|': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '^': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '<': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '>': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '==': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '!=': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '<=': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '>=': {
                ("INT", "INT"): "INT",
                ("DOUBLE", "DOUBLE"): "INT",
                ("INT", "DOUBLE"): "INT",
                ("DOUBLE", "INT"): "INT",
            },
            '$<': {
                ("STRING", "STRING"): "INT",
            },
            '$>': {
                ("STRING", "STRING"): "INT",
            },
            '$==': {
                ("STRING", "STRING"): "INT",
            },
            '$!=': {
                ("STRING", "STRING"): "INT",
            },
            '$<=': {
                ("STRING", "STRING"): "INT",
            },
            '$>=': {
                ("STRING", "STRING"): "INT",
            },
        }

        # 获取运算符的类型检查规则
        if(len(types) == 1):
            rules = type_rules_uni.get(operator, {})
        elif(len(types) == 2):
            rules = type_rules_bi.get(operator, {})

        
        # 检查是否存在对应的类型规则
        if types in rules:
            result_type = rules[types]
        else:
            error_handler("Type mismatch in expression")

        return result_type

    def sub_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 3):
            # 括号的情况
            symbol.element_type = items[1].element_type
            symbol.value = f"({items[1].value})"
            symbol.code = concat_code_segments([items[1].code])
        else:
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        return symbol
    
    def negate_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 2):
            symbol.element_type = self.evaluate_expression_type(items[0], items[1].element_type)
            symbol.value = f"-{items[1].value}"
            symbol.code = concat_code_segments([items[1].code])
        else:
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        return symbol
            
    
    def mult_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 1):
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        else:
            symbol.element_type = self.evaluate_expression_type(items[1], items[0].element_type, items[2].element_type)
            symbol.value = f"{items[0].value} {items[1]} {items[2].value}"
            symbol.code = concat_code_segments([items[0].code, items[2].code])
            # if(items[1] == "*"):
            #     symbol.value = f"{items[0].value} * {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
            # elif(items[1] == "/"):
            #     symbol.value = f"{items[0].value} / {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
        return symbol

    
    def add_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 1):
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        else:
            symbol.element_type = self.evaluate_expression_type(items[1], items[0].element_type, items[2].element_type)
            symbol.value = f"{items[0].value} {items[1]} {items[2].value}"
            symbol.code = concat_code_segments([items[0].code, items[2].code])
            # if(items[1] == "+"):
            #     symbol.value = f"{items[0].value} + {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
            # elif(items[1] == "-"):
            #     symbol.value = f"{items[0].value} - {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
        return symbol
    
    def comp_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 1):
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        else:
            symbol.element_type = self.evaluate_expression_type(items[1], items[0].element_type, items[2].element_type)
            symbol.value = f"{items[0].value} {items[1]} {items[2].value}"
            symbol.code = concat_code_segments([items[0].code, items[2].code])
            # if(items[1] == "=="):
            #     symbol.value = f"{items[0].value} == {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
            # elif(items[1] == "<="):
            #     symbol.value = f"{items[0].value} <= {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
            # elif(items[1] == ">="):
            #     symbol.value = f"{items[0].value} >= {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
            # elif(items[1] == "!="):
            #     symbol.value = f"{items[0].value} != {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
            # elif(items[1] == "<"):
            #     symbol.value = f"{items[0].value} < {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
            # elif(items[1] == ">"):
            #     symbol.value = f"{items[0].value} > {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
                
        return symbol
            
    
    def not_exp(self, items):
        symbol = Symbol("EXP")
        if(len(items) == 1):
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        else:
            symbol.element_type = self.evaluate_expression_type("!", items[1].element_type)
            symbol.value = f"!{items[1]}"
            symbol.code = items[1].code
        
        return symbol
    
    def expression(self, items):
        # TODO: 处理短路计算
        symbol = Symbol("EXP")
        if len(items) == 1:
            symbol.element_type = items[0].element_type
            symbol.value = items[0].value
            symbol.code = items[0].code
        else:
            symbol.element_type = self.evaluate_expression_type(items[1], items[0].element_type, items[2].element_type)
            symbol.value = f"{items[0].value} {items[1]} {items[2].value}"
            symbol.code = concat_code_segments([items[0].code, items[2].code])
            # if(items[1] == "&"):
            #     symbol.value = f"{items[0].value} and {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
            # elif(items[1] == "|"):
            #     symbol.value = f"{items[0].value} or {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])
            # elif(items[1] == "^"):
            #     symbol.value = f"{items[0].value} xor {items[2].value}"
            #     symbol.code = concat_code_segments([items[0].code, items[2].code])

        return symbol
    
    def expression_list(self, items):
        # 返回列表中EXP的symbol
        symbol_list = []
        if len(items) == 0:
            return None
        
        symbol_list.append(items[0])

        if(len(items) == 1):
            pass
        else:
            for exp in items[1]:
                symbol_list.append(exp)
        return symbol_list



    """
    语句
    """
    ## 赋值语句
    def assign_stmt(self, items):
        # TODO: 如果是一般变量，则直接赋值，没有重复定义以及数据类型检查
        # TODO: 如果是数组名称，不允许直接赋值，一律报错
        # TODO: 如果是数组元素，则检查数组是否存在，类型是否正确，以及索引是否合法


        left_sym = items[0]
        left_sym_type = items[0].symbol_type
        # 在符号表查询左侧元素，是否已被声明？
        # 若已被声明：
        # 若为VAR INT/DOUBLE变量，根据右侧元素类型进行类型转换
        # 若为ARRAY变量，报错
        # 若为STRING变量，根据右侧元素类型进行判断

        # 若未被声明：
        # 若为NONE
        if left_sym_type == "NONE":
            # 将其type改为VAR
            # 将symbol放入全局符号表中
            left_sym_type = "VAR"
            left_sym.symbol_type = left_sym_type
            self.global_symbol_table.add_symbol(left_sym)
            

        # 若为ARRAY_ELEMENT
        # 若为STRING


        right_sym = items[2]
        right_sym_type = items[2].symbol_type
        # 在符号表查询右侧元素，是否已被声明？
        # 若已被声明：



        # 若未被声明：
        # 若为EXP
        if right_sym_type == "EXP":
            # 将左侧元素的elem_type与EXP的elem_type判断是否match？
            pass
        

        # 取出左侧代码
        # 取出右侧代码
        # 生成assign_code
        assign_code = f"{left_sym.value} = {right_sym.value}\n"

        # 取出左侧待执行的代码
        # 取出右侧待执行的代码
        pre_run_code = concat_code_segments([left_sym.code, right_sym.code])

        node1 = IndTreeNode(pre_run_code)
        node2 = IndTreeNode(assign_code)

        return [node1, node2]
    
    ## PRINT语句
    def print_stmt(self, items):
        sym_list = items[0]
        print_code = ""
        pre_run_code = ""
        if all([sym is None for sym in sym_list]):
            print_code += f"print()\n"
        else:
            print_list = ', '.join([sym.value for sym in sym_list])
            pre_run_list = [sym.code for sym in sym_list]
            print_code += f"print({print_list})\n"
            pre_run_code = concat_code_segments(pre_run_list)
            
        pre_run_node = IndTreeNode(pre_run_code)
        print_node = IndTreeNode(print_code)
        return [pre_run_node, print_node]

    def print_list(self, items):
        sym_list = []
        # 处理当前的expression
        if len(items) == 0:
            return None
        sym_list.append(items[0])

        if(len(items) == 1):
            pass
        else:
            sym_list.extend(items[1])
        return sym_list

    ## IF语句
    def if_stmt(self, items):
        if_node = IndTreeNode("")
        else_node = IndTreeNode("")
        if_code = ""
        else_code = ""

        if items[-1] != "ENDIF":
        # "IF" expression "THEN" stmt
        # if expression:
        # 
        #     command()
        # else:
        #    
        #     pass
            if_code = f"if ({items[1]}):\n"
            if_node.set_value(if_code)
            if_node.set_children(items[3])
            else_code = f"else:\n"
            pass_node = IndTreeNode("pass\n")
            else_node.set_value(else_code)
            else_node.set_children(pass_node)

        else:
        # "IF" expression stmts "ELSE" stmts "ENDIF"
        #  if expression:
        #       if_stmts
        #  else:
        #       else_stmts
            if_code = f"if {items[1]}:\n"
            else_code = f"else:\n"

            if_stmts = []
            else_stmts = []
            found_else = False
            for stmt in items[2:-1]:
                if stmt == "ELSE":
                    found_else = True
                elif not found_else:
                    if_stmts.append(stmt)
                else:
                    else_stmts.append(stmt)

            if_node.set_value(if_code)
            for node in if_stmts:
                if_node.set_children(node)

            else_node.set_value(else_code)
            for node in else_stmts:
                else_node.set_children(node)

        return [if_node, else_node]
            
    ## FOR语句
    def for_stmt(self, items):
    # for id in range(exp, exp, exp):
    #     stmts
        for_code = f"for {items[0]} in range({items[1]}, {items[2]}, {items[3]}):\n"
        for_node = IndTreeNode(for_code)
        for node in items[4:]:
            for_node.set_children(node)

        return for_node
    
    def declare_stmt(self, items):
        array_name = items[0]['value']
        array_type = items[1]
        array_dimensions = [int(token.value) for token in items[2:]]

        # 重复声明/使用
        if self.global_symbol_table.is_symbol_exist(array_name):
            error_handler("Array already declared")

        # 超过四维
        if(len(array_dimensions) > 4):
            error_handler("Array dimensions cannot exceed 4")

        symbol = Symbol('ARRAY', element_type=array_type, dimensions=array_dimensions, value=array_name)
        self.global_symbol_table.add_symbol(symbol)
    
        # 是否需要翻译Python代码？

    def type(self, items):
        return(items[0].value)

    def release_stmt(self, items):
        array_name = items[0]['content']
        self.global_symbol_table.remove_symbol(array_name)

    def stmt(self, items):
        return items[0]


    """
    宏处理
    """
    def macro_call(self, items):
        macro_name = items[0]
        exp_list = items[1]
        param_list = exp_list
        code_list = [exp.code for exp in exp_list]
        macro_symbol = Symbol('MACRO')


        # TODO: 让加载macro_dict更加自动化
        with open(config.macro_path, 'r', encoding='utf-8') as file:
            macro_dict = json.load(file)

        macro_def = macro_dict.get(macro_name)

        if macro_def:
            temp_vars = process_temp_var_name(macro_def['temp_vars'])
            code = macro_def['code']

            # 完成param的个数判断
            if len(param_list) != len(macro_def['input']):
                error_handler("Parameter number mismatch")
            # 完成param的类型判断
            # 将param_list注入到macros.json中macro_name对应条目的code中
            for i, param in enumerate(param_list):
                if not is_type_match(macro_def['input'][i]['type'], param.element_type):
                    error_handler("Parameter type mismatch")
                code = code.replace(f'{{{{{macro_def["input"][i]['name']}}}}}', str(param.value))

            # 将temp_vars注入到macros.json中macro_name对应条目的code中
            for temp_var in temp_vars:
                code = code.replace(f'{{{{{temp_var}}}}}', temp_vars[temp_var])
            
            # 将返回值赋值给macro_symbol.value
            # TODO: 是否考虑多返回值的情况？
            output_vars = temp_vars[macro_def['output'][0]['name']]
            macro_symbol.value = output_vars
            macro_symbol.element_type = macro_def['output'][0]['type']

            # 向code_list中末尾添加先前修改后的code
            code_list.append(code)
            macro_code = concat_code_segments(code_list)

            # output的类型记录
            macro_symbol.element_type = macro_def['ret_type']

            # 将code_list作为macro_symbol.code
            macro_symbol.code = macro_code

        return macro_symbol
            
    
    def macro_id(self, items):
        return (items[0].value)

    """
    构建缩进树
    """
        
    def top_node(self, items):
        self.top_ind_tree.set_children(items)
        return 0
    
    def get_ind_tree(self):
        return self.top_ind_tree
    




    