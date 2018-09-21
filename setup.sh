
git clone https://github.com/maxlklaxl/python-tsl2591
cd python-tsl2591

sudo python setup.py install

cd ..

git clone https://github.com/Azure/azure-iot-sdk-python.git --recursive
cd azure-iot-sdk-python/build_all/linux
./setup.sh --python-version 2.7
./build.sh --build-python 2.7
cd ../../device/samples
cp iothub_client.so ../../../iothub_client.so

cd ../..
