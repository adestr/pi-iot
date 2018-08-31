
git clone https://github.com/Azure/azure-iot-sdk-python.git --recursive
cd azure-iot-sdk-python/build_all/linux
./setup.sh --python-version $PYTHON_VERSION
./build.sh --build-python $PYTHON_VERSION
cd ../../device/samples
cp iothub_client.so ../../../iothub_client.so

# TODO: Aren't we in a folder now?

git clone https://github.com/maxlklaxl/python-tsl2591
cd python-tsl2591

if [[ $PYTHON_VERSION == 2.7 ]]; then
    sudo python setup.py install
else 
    sudo python3 setup.py install
fi

cd ..
