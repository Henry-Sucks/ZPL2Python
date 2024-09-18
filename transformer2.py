from lark import Transformer, Token

class TestTransformer(Transformer):
    def __init__(self):
        self.vars = {}
        self.code = ""
        # 控制当前代码缩进个数
        self.cur_indentation_num = 0
        self.cur_indentation = ""

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
    



    # 语句
    # 赋值语句
    def assign_stmt(self, items):
        cur_code = ""
        var, _, val = items
        cur_code = f"{var} = {val}"

        cur_code += '\n'
        return cur_code  # 应该返回什么值？
    
    # PRINT语句
    def print_stmt(self, items):
        cur_code = ""
        if all([elem is None for elem in items]):
            cur_code += f"print()"
        else:
            cur_code += f"print({items[0]})"

        cur_code += '\n'
        return cur_code

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

    # IF语句
    def if_stmt(self, items):
        cur_code = ""
        if items[-1] != "ENDIF":
        # "IF" expression "THEN" stmt
        # if expression:
        # 
        #     command()
        # else:
        #    
        #     pass
            cur_code += f"if ({items[1]}):\n"
            
            cur_code += f"{items[3]}\n"
            
            cur_code += f"else:\n"
            
            cur_code += f"pass\n"

        else:
        # "IF" expression stmts "ELSE" stmts "ENDIF"
        #  if expression:
        #       if_stmts
        #  else:
        #       else_stmts
            cur_code += f"if {items[1]}:\n"
            
            if_stmts = ""
            else_stmts = ""
            found_else = False
            for stmt in items[2:-1]:
                if stmt == "ELSE":
                    found_else = True
                elif not found_else:
                    if_stmts += stmt
                else:
                    else_stmts += stmt

            
            cur_code += f"{if_stmts}\n"
            
            cur_code += f"else:\n"
            
            cur_code += f"{else_stmts}\n"

            # print(cur_code)
            return cur_code


        return cur_code
            

    def stmt(self, items):
        return items[0]
        
    def top_node(self, items):
        # 遍历列表，将语句放入code中
        for stmt in items:
            self.code += stmt


    def func_ret(self, items):
        for item in items:
            print(item)


    def get_code(self):
        return self.code
    

    def get_indentation(self):
        self.cur_indentation = ""
        for i in range(self.cur_indentation_num):
            self.cur_indentation += "\t"

        return self.cur_indentation