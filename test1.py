class TestTransformer():
    def __init__(self):
        pass

    # ... 其他方法 ...

    # 通用的工厂方法来生成函数处理方法
    def create_func_method(self, func_name):
        def func_method(items):
            cur_code = func_name
            cur_code += f"({', '.join(items)})"
            return cur_code
        return func_method

    # 方法来动态添加函数处理方法
    def add_func_methods(self, func_names):
        for name in func_names:
            method_name = f"{name}_func"
            setattr(self, method_name, self.create_func_method(name))

# 函数名列表
func_names = ['acos', 'asin', 'pow']

# 创建 TestTransformer 实例
transformer = TestTransformer()

# 添加方法
transformer.add_func_methods(func_names)

# 测试自动创建的方法
print(transformer.acos_func(["x"]))  # 输出: acos(x)
print(transformer.asin_func(["y"]))  # 输出: asin(y)
print(transformer.pow_func(["a", "b", "c"]))  # 输出: pow(a, b, c)