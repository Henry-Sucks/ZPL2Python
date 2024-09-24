#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "example.h"
#include "calculator.h"
// pybind11 绑定代码
namespace py = pybind11;

PYBIND11_MODULE(example, m) {
    // 注册基类
    py::class_<Base>(m, "Base")
        .def(py::init<>()) // 默认构造函数
        .def("print", &Base::print)        // 函数绑定
        .def("setValue", &Base::setValue)
        .def("getValue", &Base::getValue);

    // 注册派生类
    py::class_<Derived, Base>(m, "Derived")
        .def(py::init<std::string, double>()) // 构造函数定义
        .def("print", &Derived::print)        // 函数绑定
        .def("addDouble", &Derived::addDouble)
        .def("getPointerValue", &Derived::getPointerValue)
        .def("setPointerValue", &Derived::setPointerValue);

    // 注册C++模板函数
    m.def("sum", [](const std::vector<int>& v) { return sum(v); }, py::arg("numbers")); // 针对 int
    m.def("sum", [](const std::vector<double>& v) { return sum(v); }, py::arg("numbers")); // 针对 double

    py::class_<Calculator>(m, "Calculator")
        .def(py::init<>())
        .def("add", &Calculator::add)
        .def("subtract", &Calculator::subtract)
        .def("multiply", &Calculator::multiply)
        .def("divide", &Calculator::divide);
}