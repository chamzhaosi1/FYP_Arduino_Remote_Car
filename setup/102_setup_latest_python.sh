### Step 7 : Install Python
apt -y install build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev wget libbz2-dev python3-pip 
cd ~ 
wget https://www.python.org/ftp/python/3.11.3/Python-3.11.3.tgz
tar -xf Python-3.11.3.tgz 
cd Python-3.11.3
./configure --enable-optimizations && make -j$(nproc) && make altinstall
cd /usr/bin
rm python
ln -s /usr/local/bin/python3.11 python
python --version
cd ~
rm -rf Python-3.11.3
rm -rf Python-3.11.3.tgz

# pip cache purge
pip install --upgrade pip
pip install virtualenv

cd /usr/local/bin/
virtualenv -p /usr/local/bin/python3.11 venv
chmod 777 -R /usr/local/bin/venv/

### Activate
cd ~
source /usr/local/bin/venv/bin/activate

# sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.11 1
# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 2
# sudo update-alternatives --config python
# sudo update-alternatives --config python3

### Requirement library 
# Noted, please run the file 002_faceRecognize_setup.sh first before run below library
pip install opencv-contrib-python-headless face-recognition flask pyserial, scipy, numpy, Flask-SQLAlchemy bcrypt #matplotlib

# run this line if want to run flask app
# export FLASK_APP=app.py
# flask run
