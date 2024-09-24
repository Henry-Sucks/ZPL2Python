#include "example.h"
#include <iostream>

// Base 类实现
Base::Base() : value(0) {}

Base::~Base() {}

void Base::print() const {
    std::cout << "Base value: " << value << std::endl;
}

void Base::setValue(int v) {
    value = v;
}

int Base::getValue() const {
    return value;
}

// Derived 类
Derived::Derived(const std::string& str, double d) : Base(), myString(str), myDouble(d), myDoublePtr(new double(d)) {}

Derived::~Derived() {
    delete myDoublePtr;  
}

void Derived::print() const {
    Base::print(); // 调用基类的 print 方法
    std::cout << "Derived String: " << myString << " Double: " << myDouble << " Pointer Value: " << *myDoublePtr << std::endl;
}

void Derived::addDouble(double d) {
    myDouble += d;
    *myDoublePtr += d; // 也修改指针所指向的值
}

double Derived::getPointerValue() const {
    return *myDoublePtr;
}

void Derived::setPointerValue(double d) {
    *myDoublePtr = d;
}

// C++模板函数实现
template<typename T>
T sum(const std::vector<T>& v) {
    T sum = T(); // 初始化模板类型为零
    for (const auto& val : v) sum += val;
    return sum;
}

// 显式实例化模板函数
template int sum<int>(const std::vector<int>&);
template double sum<double>(const std::vector<double>&);