from lark import Transformer, Token

class TestTransformer(Transformer):
    def __init__(self):
        self.vars = {}
        self.code = ""

    def num(self, n):
        # print("NUM: ", float(n[0]))
        return float(n[0])
    
    def string(self, str):
        str = str[0][1:-1]
        # print("STRING:", str)
        return str
    
    def id_def(self, id):
        # 两种情况：首次声明/赋值以及已经存在
        # 首次声明，先赋0的初始值
        if id[0] not in self.vars:
            self.vars[id[0]] = 0

        # 返回变量的名称
        # print("ID: ", id[0])
        return id[0]
    
    def id_val(self, id):
        return self.vars[id[0]]
    
    def value(self, item):
        # print("VALUE: ", item[0])
        return item[0]
    
    def sub_exp(self, items):
        if(len(items) == 3):
            # 括号的情况
            pass
        else:
            return items[0]
    
    def negate_exp(self, items):
        if(len(items) == 2):
            return(-items[0])
        else:
            return(items[0])
            
    
    def mult_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "*"):
                return(items[0] * items[2])
            elif(items[1] == "/"):
                return(items[0] / items[2])

    
    def add_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "+"):
                return(items[0] + items[2])
            elif(items[1] == "-"):
                return(items[0] - items[2])
    
    def comp_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            if(items[1] == "=="):
                return(items[0] == items[2])
            elif(items[1] == "<="):
                return(items[0] <= items[2])
            elif(items[1] == ">="):
                return(items[0] >= items[2])
            elif(items[1] == "!="):
                return(items[0] != items[2])
            elif(items[1] == "<"):
                return(items[0] < items[2])
            elif(items[1] == ">"):
                return(items[0] > items[2])
            
    
    def not_exp(self, items):
        if(len(items) == 1):
            return(items[0])
        else:
            return(not items[1])
    
    def expression(self, items):
        if len(items) == 1:
            return items[0]
        else:
            if(items[1] == "&"):
                return (items[0] and items[2])
            elif(items[1] == "|"):
                return (items[0] or items[2])
            elif(items[1] == "^"):
                return (items[0] != items[2]) # Python中的异或运算需要注意一下！
    
    # 赋值语句
    def assign_stmt(self, items):
        var, _, val = items
        self.vars[var] = val

        print(f"{var} {val}")
        return 0  # 应该返回什么值？
    
    # PRINT语句
    def print_stmt(self, items):
        if len(items) == 0:
            print('\n')
        else:
            print(items[0])
        return 0

    def print_list(self, items):
        # 处理当前的expression
        if len(items) == 0:
            return None
        cur = items[0]
        if(isinstance(cur, Token) and cur.type == "IDENTIFIER"):
            cur = self.vars[cur]
        else:
            pass

        # 如果不是最末字符串，将当前字符串加到先前字符串的左侧再返回
        if(len(items) == 1):
            cur = str(cur)
        else:
            cur = str(cur) + items[1]
        return cur

    # IF语句
    def if_stmt(self, items):
        pass

    def then_clause(self, items):
        pass


    def func_ret(self, items):
        for item in items:
            print(item)

