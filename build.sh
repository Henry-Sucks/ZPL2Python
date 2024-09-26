mkdir -p build
cd build
export CMAKE_PREFIX_PATH=/usr/local/lib/python3.8/dist-packages:$CMAKE_PREFIX_PATH
cmake ..
cmake --build
cd build
make
