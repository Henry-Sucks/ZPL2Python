class TempVarManager:
    def __init__(self):
        self.counter = 0
        self.available_vars = []  # 可用变量列表
        self.used_vars = []       # 已使用变量列表

    def generate_var(self):
        # 如果有可用变量，重用它
        if self.available_vars:
            new_var = self.available_vars.pop()  # 从可用列表中取出一个
        else:
            self.counter += 1
            new_var = f"res{self.counter}"  # 生成新的变量名
        self.used_vars.append(new_var)  # 记录使用过的变量
        return new_var

    def remove_var(self, var_name):
        if var_name in self.used_vars:
            self.used_vars.remove(var_name)  # 从已使用列表中移除
            self.available_vars.append(var_name)  # 将变量加入可用列表
        else:
            raise ValueError(f"Variable {var_name} does not exist!")

class CodeGenerator:
    def __init__(self):
        self.temp_var_manager = TempVarManager()  # 创建 TempVarManager 实例

    def generate_code(self, macro_info, input_args):
        """
        根据macro数据和输入参数生成对应的Python代码。
        macro_info 是包含 'usage_call', 'args', 'res' 等的字典。
        input_args 是一个列表，包含实际传入的参数值。
        """
        code = macro_info["usage"]
        args = macro_info["args"]
        res = macro_info["res"]

        # 生成并替换返回值变量
        if res:
            for return_var in res:
                temp_var = self.temp_var_manager.generate_var()  # 使用 TempVarManager 生成临时变量
                code = code.replace(f"<{return_var}>", temp_var)
        
        # 替换参数变量
        for i, arg in enumerate(args):
            if i < len(input_args):
                code = code.replace(f"<{arg}>", str(input_args[i]))

        return code, temp_var
    


# 示例使用
macro_info = {
    "usage": "print('Hello world')\n<return_var1> = abs(<x>)\n",
    "args": ["x"],
    "res": ["return_var1"]
}