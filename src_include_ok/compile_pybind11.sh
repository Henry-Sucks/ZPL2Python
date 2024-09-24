echo "rm *.so and build"
rm ./*.so
rm build -r
echo "-------------------------------building---------------------"
mkdir build
cd build
cmake ..
make
cp *.so ../