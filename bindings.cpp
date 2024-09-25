#include <pybind11/pybind11.h>
#include "/home/ZPL2Python/mylib/include/mylib.h"
namespace py = pybind11;
PYBIND11_MODULE(mylib, m){
	m.def("A", &A, "A(x, y), 计算x*y");
	m.def("A", &A, "B(x, y), 计算x+y");
}
