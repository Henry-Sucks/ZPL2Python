#ifndef EXAMPLE_H
#define EXAMPLE_H

#include <string>
#include <vector>


class Base {
public:
    Base();
    virtual ~Base();
    
    virtual void print() const;
    void setValue(int v);
    int getValue() const;

private:
    int value;
};

// 派生类
class Derived : public Base {
public:
    Derived(const std::string& str, double d);
    ~Derived();
    
    void print() const override;
    void addDouble(double d);
    double getPointerValue() const;
    void setPointerValue(double d);

private:
    std::string myString;
    double myDouble;
    double* myDoublePtr; // 指针成员变量
};

// C++模板函数
template<typename T>
T sum(const std::vector<T>& v);

#endif // EXAMPLE_H