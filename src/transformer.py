from lark import Transformer
class IndTreeNode:
        def  __init__(self, value):
            self.code = ""
            self.value = value
            self.children = []

            # 为什么是-1？因为top_node是一个空节点，需要耗费一次层数
            self.level = -1
            

        def add_child(self, child_node):
            self.children.append(child_node)

        def set_children(self, items):
            if isinstance(items, list):
                for item in items:
                    self.set_children(item)
            elif isinstance(items, IndTreeNode):
                    self.add_child(items)


        def set_value(self, value):
            self.value = value

        def get_children(self):
            return self.children
        
        def get_indentation(self):
            cur_indentation = ""
            for i in range(self.level):
                cur_indentation += "\t"

            return cur_indentation
        
        
        def dfs(self, cur_level):
            # 访问当前节点
            ## 将缩进+value中代码放入value中
            ## 增加缩进层数
            self.level = cur_level
            self.value = f"{self.get_indentation()}{self.value}"
            self.level += 1


            ## 遍历子节点，加上子节点返回的代码
            for child in self.children:
                
                self.value += child.dfs(self.level)

            return self.value
        
        def build_code(self):
            self.code = self.dfs(self.level)
            return
        
        def get_code(self):
            return self.code
            
            
        def __repr__(self):
            children_repr = ', '.join(repr(child) for child in self.children)
            return f"IndTreeNode(\"{self.value}\", [{children_repr}])"
        

class TestTransformer(Transformer):
    def __init__(self):
        self.vars = {}
        self.code = ""
        self.top_ind_tree = IndTreeNode("")
        self.called_not_built_in_list = []
        self.called_has_not_built_in = False


    """
    value：数字、变量名、函数调用、字符串
    """ 
    def num(self, n):
        return n[0]
    
    def string(self, str):
        str = str[0][1:-1]
        return f"\"{str}\""
    
    def id_def(self, id):
        return id[0]
    
    def id_val(self, id):
        return id[0]
    
    def value(self, item):
        return item[0]
    
    def func_ret(self, items):
        return items[0]
    
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
            return(f"-{items[0]}")
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
    函数处理
    """
    # def abso_func(self, items):
    #     cur_code = "abs"
    #     cur_code += f"({items[0]})"
    #     return cur_code

    # def powr_func(self, items):
    #     cur_code = "pow"
    #     cur_code += f"({items[0]})"
    #     return cur_code
    
    def create_built_in_func_method(self, zpl_name, py_name):
        def func_method(items):
            cur_code = py_name
            cur_code += f"({items[0]})"
            return cur_code
        
        method_name = f"{zpl_name}_func"
        setattr(self, method_name, func_method)

    def create_not_built_in_func_method(self, zpl_name, py_name):
        def func_method(items):
            cur_code = py_name
            cur_code += f"({items[0]})"
            if py_name not in self.called_not_built_in_list:
                self.called_not_built_in_list.append(py_name)
            self.called_has_not_built_in = True
            return cur_code
        
        method_name = f"{zpl_name}_func"
        setattr(self, method_name, func_method)

    
    def get_called_not_built_in_list(self):
        called_not_built_in_list = ''
        for index, func in enumerate(self.called_not_built_in_list):
            called_not_built_in_list += func
            if index < len(self.called_not_built_in_list) - 1:
                called_not_built_in_list += ', '

        return called_not_built_in_list
    

    """
    构建缩进树
    """
        
    def top_node(self, items):
        self.top_ind_tree.set_children(items)
        return 0
    
    def get_ind_tree(self):
        return self.top_ind_tree
    




    