## Refer: https://linuxhint.com/install-sqlite-on-debian-11/
apt -y update & dist-upgrade
apt -y install sqlite3

sqlite3 --version

sqlite3 testing.db

# Create table test(name String);
# .table