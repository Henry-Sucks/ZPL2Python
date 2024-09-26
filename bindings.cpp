#include <pybind11/pybind11.h>
#include "/home/ZPL2Python/mylib/include/mylib.h"
namespace py = pybind11;
PYBIND11_MODULE(mylib, m){
	m.def("a", &A, "A(x, y), 计算x*y");
	m.def("b", &B, "B(x, y), 计算x+y");
	m.def("c", &C, "C(x, y), 计算x/y");
}
