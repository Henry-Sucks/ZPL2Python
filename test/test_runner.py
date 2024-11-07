from ..src.translator import translate

import os
import subprocess
import tempfile

ZPL_CODE_DIR = "./zpl_code"
PY_CODE_DIR = "./py_code"

def run_python_code(code):
    # 创建临时文件
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.py') as temp_file:
        temp_file.write(code)
        temp_file_path = temp_file.name
    
    # 运行临时文件中的Python代码，捕获输出
    result = subprocess.run(["python", temp_file_path], capture_output=True, text=True)
    
    # 删除临时文件
    os.remove(temp_file_path)
    
    return result.stdout

def run_test(zpl_file, py_file):
    # 读取ZPL代码
    with open(zpl_file, 'r') as f:
        zpl_code = f.read()
    
    # 调用translate方法进行翻译
    translated_code = translate(zpl_code)
    
    # 运行翻译后的Python代码
    translated_output = run_python_code(translated_code)
    
    # 读取预期结果
    with open(py_file, 'r') as f:
        expected_code = f.read()
    
    # 运行预期逻辑的Python代码
    expected_output = run_python_code(expected_code)
    
    # 比较实际输出和预期结果
    if translated_output == expected_output:
        print(f"Test passed: {zpl_file}")
    else:
        print(f"Test failed: {zpl_file}")
        print("Expected output:")
        print(expected_output)
        print("Actual output:")
        print(translated_output)

def run_test_all():
    # 遍历所有测试用例
    for zpl_file in os.listdir(ZPL_CODE_DIR):
        if zpl_file.endswith(".zpl"):
            zpl_path = os.path.join(ZPL_CODE_DIR, zpl_file)
            expected_result_file = os.path.join(PY_CODE_DIR, f"{os.path.splitext(zpl_file)[0]}_expected.py")
            
            # 运行测试
            run_test(zpl_path, expected_result_file)

if __name__ == "__main__":
    run_test_all()