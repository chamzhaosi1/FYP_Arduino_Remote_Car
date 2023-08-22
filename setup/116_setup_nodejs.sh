#!/bin/bash

# NodeJS

################################################################################
### NODEJS ### NODEJS ### NODEJS ### NODEJS ### NODEJS ### NODEJS ### NODEJS ###
################################################################################

# As ROOT, remove previous wrong NodeJS 16
# apt -y purge nodejs yarn
# apt -y autoremove
# rm -rf /etc/apt/sources.list.d/yarn.list 
# rm -rf /etc/apt/sources.list.d/nodesource.list

### As ROOT : Install Server-side Scripting - NodeJS.
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

### As ROOT : need development tools to build native addons:
apt -y install gcc g++ make build-essential

### As ROOT : install the Yarn package manager, run:
curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | tee /etc/apt/sources.list.d/yarn.list
apt -y update
apt -y dist-upgrade

### As ROOT : Install
apt -y install nodejs yarn
node --version
# Latest LTS Version: 16.13.0
npm --version
# npm 8.1.0
npm install -g npm@latest
npm --version
# npm 8.1.3

################################################################################
### ANGULAR  ### ANGULAR  ### ANGULAR  ### ANGULAR  ### ANGULAR  ### ANGULAR  ##
################################################################################

npm install -g json-server
npm install -g @angular/cli@latest
npm list -g
su - engineer