###############################################################################
### Step 1 : Disable Nouveau Driver
###############################################################################
lsmod | grep nouveau
cat > /etc/modprobe.d/blacklist.conf << EOF
blacklist nouveau
EOF
reboot
lsmod | grep nouveau

#######################################################################
### Step 3 : Install CUDA with CUDA self-tested Nvidia Driver  
#######################################################################

# https://developer.nvidia.com/rdp/cudnn-download

lspci | grep NVIDIA
# 01:00.0 VGA compatible controller: NVIDIA Corporation GM204 [GeForce GTX 970] (rev a1)
# 01:00.1 Audio device: NVIDIA Corporation GM204 High Definition Audio Controller (rev a1)
apt -y install software-properties-common gnupg

### Add Repo
# add-apt-repository "deb https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/ /"
add-apt-repository contrib

### Add Keys
# apt-key del 7fa2af80
apt -y install wget
# apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/7fa2af80.pub
apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/3bf863cc.pub
wget https://developer.download.nvidia.com/compute/cuda/repos/debian11/x86_64/cuda-keyring_1.0-1_all.deb
dpkg -i cuda-keyring_1.0-1_all.deb
rm -rf ./cuda-keyring_1.0-1_all.deb

### Install
apt update
apt-cache search cuda
apt-cache search cuda | grep cuda

apt-cache policy cuda
apt -y install cuda
# apt -y install cuda-11-1
# apt -y install cuda-12-0
# apt -y install nvidia-cuda-toolkit
watch -n 1 nvidia-smi
nvidia-smi -L
apt -y autoremove

### GeForce GTX 970 CUDA
# | NVIDIA-SMI 525.85.12    Driver Version: 525.85.12    CUDA Version: 12.0     |

### GeForce 1050 & 1060 Driver Only
# | NVIDIA-SMI 510.54       Driver Version: 510.54       CUDA Version: 11.6     |

### GeForce 1050 & 1060 CUDA
# | NVIDIA-SMI 510.47.03    Driver Version: 510.47.03    CUDA Version: 11.6     |

### Quadro K2000  Driver Only
# | NVIDIA-SMI 470.103.01   Driver Version: 470.103.01   CUDA Version: 11.4     |

#######################################################################
### Step 4 : Monitoring GPU 
#######################################################################
nvidia-smi -q -g 0 -d UTILIZATION -l | grep Gpu
nvidia-smi pmon

###############################################################################
### Step 5 : CUDA Deep Neural Network library (cuDNN)
###############################################################################
# as ROOT

# Download
cd ~
# wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-ubuntu2004-8.3.3.40_1.0-1_amd64.deb
# wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-ubuntu2004-8.4.1.50_1.0-1_amd64.deb
# wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-ubuntu2004-8.4.1.50_1.0-1_amd64.deb
# wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-debian11-8.6.0.163_1.0-1_amd64.deb
# wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-debian11-8.8.0.121_1.0-1_amd64.deb
wget --no-check-certificate https://engineer:anakperantau@file.iisb.my/nvidia/cudnn-local-repo-debian11-8.9.1.23_1.0-1_amd64.deb


# Enable the local repository.
dpkg -i cudnn-local-repo-debian11-8.9.1.23_1.0-1_amd64.deb
rm -rf cudnn-local-repo-debian11-8.9.1.23_1.0-1_amd64.deb

### Import cuDNN GPG key
find /var/ -name *.pub
apt-key add /var/cudnn-local-repo-debian11-8.9.1.23/C25D6890.pub
find /var/ -name *-keyring.gpg
cp /var/cudnn-local-repo-debian11-8.9.1.23/cudnn-local-C25D6890-keyring.gpg /usr/share/keyrings/cudnn-local-C25D6890-keyring.gpg
cd /var/cudnn-local-repo-debian11-8.9.1.23/ && dpkg -i *.deb

# Refresh the repository metadata.
apt -y update

# Install the runtime library.
apt -y install libcudnn8

# Install the developer library.
apt -y install libcudnn8-dev

# Install the code samples and the cuDNN library documentation.
apt -y install libcudnn8-samples

###############################################################################
### Step 6 : install requirement library
###############################################################################
apt -y install tensorrt

pip install numpy
pip install cupy
pip install numba
pip install dlib
pip install dlib_cuda
pip install --upgrade nvitop
# Run nvitop
nvitop

pip install tensorflow-gpu
pip install deepface
# Read more at: https://viso.ai/computer-vision/deepface/


# Install dlib
apt-get -y install cmake
apt -y install pkg-config

cd ~
wget http://dlib.net/files/dlib-19.24.tar.bz2
tar xvf dlib-19.24.tar.bz2
cd dlib-19.24/
mkdir build
cd build
cmake ..
cmake --build . --config Release
sudo make install
sudo ldconfig
cd ..
pkg-config --libs --cflags dlib-1


