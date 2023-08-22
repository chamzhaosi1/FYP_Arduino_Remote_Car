### Step 1: Install dlib
apt -y install cmake
cd /home/engineer
git clone https://github.com/davisking/dlib.git
cd dlib
mkdir build
cd build
cmake ..
cmake --build .
cd ..
python3 setup.py install