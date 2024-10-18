from lark import Transformer
import json
import os
from .ind_tree_node import IndTreeNode

        

class ZPLTransformer(Transformer):
    def __init__(self, config_dir):
        self.vars = {}
        self.code = ""
        self.top_ind_tree = IndTreeNode("")

        self.config_dir = config_dir
        self.macro_list = []
        self.compiled_macro_list = []


    """
    value：数字、变量名、函数调用、字符串
    """ 
    def value(self, item):
        return item[0]

    def num(self, n):
        return {"type": "num","content": n[0]}
    
    def string(self, str):
        str = str[0][1:-1]
        return {"type": "string","content": f"\"{str}\""}
    
    def id_def(self, id):
        return {"type": "id_def","content": id[0]}
    
    def id_val(self, id):
        return {"type": "id_val","content": id[0]}
    
    def macro_ret(self, items):
        return {"type": "macro_ret","content": items}
    
    """
    表达式
    """ 
    def sub_exp(self, items):
        if(len(items) == 3):
            # 括号的情况
            return f"( {items[1]} )"
        else:
            return items[0]
    
    def negate_exp(self, items):
        if(len(items) == 2):
            return(f"-{items[1]}")
        else:
            return(items[0])
            
    
    def mult_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "*"):
                return(f"{items[0]} * {items[2]}")
            elif(items[1] == "/"):
                return(f"{items[0]} / {items[2]}")

    
    def add_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "+"):
                return(f"{items[0]} + {items[2]}")
            elif(items[1] == "-"):
                return(f"{items[0]} - {items[2]}")
    
    def comp_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "=="):
                return(f"{items[0]} == {items[2]}")
            elif(items[1] == "<="):
                return(f"{items[0]} <= {items[2]}")
            elif(items[1] == ">="):
                return(f"{items[0]} >= {items[2]}")
            elif(items[1] == "!="):
                return(f"{items[0]} != {items[2]}")
            elif(items[1] == "<"):
                return(f"{items[0]} < {items[2]}")
            elif(items[1] == ">"):
                return(f"{items[0]} > {items[2]}")
            
    
    def not_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            return(f"!{items[1]}")
    
    def expression(self, items):
        cur_code = ""
        if len(items) == 1:
            cur_code = items[0]
        else:
            if(items[1] == "&"):
                cur_code = (f"{items[0]} and {items[2]}")
            elif(items[1] == "|"):
                cur_code = (f"{items[0]} or {items[2]}")
            elif(items[1] == "^"):
                cur_code = (f"({items[0]} or {items[2]}) and not ({items[0]} and {items[2]})")

        return cur_code
    
    def expression_list(self, items):
        list_code = ""
        if len(items) == 0:
            return None
        list_code = items[0]

        if(len(items) == 1):
            pass
        else:
            list_code = f"{list_code}, {items[1]}"
        return list_code



    """
    语句
    """
    ## 赋值语句
    def assign_stmt(self, items):
        cur_code = ""
        var, _, val = items
        cur_code = f"{var} = {val}"


        cur_code += '\n'
        node = IndTreeNode(cur_code)
        return node
    
    ## PRINT语句
    def print_stmt(self, items):
        cur_code = ""
        if all([elem is None for elem in items]):
            cur_code += f"print()"
        else:
            cur_code += f"print({items[0]})"

        cur_code += '\n'
        node = IndTreeNode(cur_code)
        return node

    def print_list(self, items):
        list_code = ""
        # 处理当前的expression
        if len(items) == 0:
            return None
        list_code = items[0]

        # 如果不是最末字符串，将当前字符串加到先前字符串的左侧再返回
        if(len(items) == 1):
            pass
        else:
            list_code = f"{list_code}, {items[1]}"
        return list_code

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

    def stmt(self, items):
        return items[0]
    
    """
    宏处理
    """

    def record_macro(self, macro):
        if macro not in self.compiled_macro_list:
            self.compiled_macro_list.append(macro)

    # def create_macro_method(self, macro):


        # if macro['type'] == 'built_in':
        #     # Python内部实现调用
        #     def macro_method(items):
        #         self.record_macro(macro)
        #         cur_code = f"{macro['python_call']}{items}"
        #         return cur_code
            
        # else:
        #     if macro['type'] == 'function':
        #         # 普通函数调用
        #         def macro_method(items):
        #             self.record_macro(macro)
        #             cur_code = f"{macro['python_module']}.{macro['python_call']}({items[0]})"
        #             return cur_code
            
        #     elif macro['type'] == 'static_method':
        #         # 静态方法调用
        #         def macro_method(items):
        #             self.record_macro(macro)
        #             cur_code = f"{macro['python_module']}.{macro['python_class']}.{macro['python_call']}({items[0]})"
        #             return cur_code
        #     elif macro['type'] == 'member_method':
        #         # 成员方法调用（有构造函数）
        #         def macro_method(items):
        #             self.record_macro(macro)
        #             instance_name = f"{macro['python_class'].lower()}_instance"  # 动态生成类的实例名
        #             cur_code = f"{instance_name} = {macro['python_module']}.{macro['python_class']}({items[0]})\n"
        #             cur_code += f"{instance_name}.{macro['python_call']}()"
        #             return cur_code
        #     elif macro['type'] == 'constructor_method':
        #         # 成员方法调用（构造函数在外）
        #         def macro_method(items):
        #             self.record_macro(macro)
        #             instance_name = f"{macro['python_class'].lower()}_instance"
        #             cur_code = f"{instance_name} = {macro['python_module']}.{macro['python_class']}()\n"
        #             cur_code += f"{instance_name}.{macro['python_call']}({items[0]})"
        #             return cur_code
                
        # method_name = f"{macro['zpl_macro'].lower()}_macro"
        # setattr(self, method_name, macro_method)

    # 向transformer注入函数处理
    # 将config中定义的函数载入到字典中
    def load_config(self):
        for filename in os.listdir(self.config_dir):
            if filename.endswith('.json'):
                file_path = os.path.join(self.config_dir, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    config_data = json.load(file)
                    for macro in config_data.get('macros', []):
                        self.macro_list.append(macro)

    # def build_transformer(self):
    #     self.load_config()
    #     for macro in self.macro_list:
    #         self.create_macro_method(macro)


    def get_import_code(self):
        # 遍历self.compiled_macro_list获取macro调用的module，并生成Python的import代码
        # 存储在macro['python_module']中
        import_statements = set()
        for macro in self.compiled_macro_list:
            python_module = macro.get('python_module')
            if python_module:
                import_statements.add(f"import {python_module}")

        return "\n".join(import_statements)
    

    """
    构建缩进树
    """
        
    def top_node(self, items):
        self.top_ind_tree.set_children(items)
        return 0
    
    def get_ind_tree(self):
        return self.top_ind_tree
    




    