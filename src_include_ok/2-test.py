import example

# 创建基类实例
base = example.Base()
base.setValue(42)
base.print()  # 输出 "Base value: 42"

# 创建派生类实例
derived = example.Derived('Hello, World!', 3.14)
derived.addDouble(2.72)
derived.print()  # 输出 "Base value: 0 Derived String: Hello, World! Double: 5.86 Pointer Value: 5.86"

# 获取和设置指针的值
print(derived.getPointerValue())  # 输出 5.86
derived.setPointerValue(10.0)
print(derived.getPointerValue())  # 输出 10.0

# 使用模板函数
int_sum = example.sum([1, 2, 3, 4, 5])  # 输出 15
double_sum = example.sum([1.1, 2.2, 3.3, 4.4, 5.5])  # 输出 16.5


# 创建 Calculator 对象
calc = example.Calculator()

# 进行运算
print('++++++++++++++++',calc.add(5, 3))        # 输出 8
print(calc.subtract(5, 3))   # 输出 2
print(calc.multiply(5, 3))   # 输出 15
print(calc.divide(5, 3))     # 输出 1.6666666666666667

# 测试除零
try:
    print(calc.divide(5, 0))
except Exception as e:
    print(e)  # 输出 Division by zero