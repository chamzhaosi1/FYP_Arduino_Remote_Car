### Step 7 : Install NodeJS
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo bash -
sudo apt -y install gcc g++ make build-essential
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
sudo apt -y update
sudo apt -y dist-upgrade
sudo apt -y install nodejs yarn
node --version
npm --version