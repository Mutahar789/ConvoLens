#!/bin/bash

# Install PostgreSQL
sudo apt-get -y install bash-completion wget
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" |sudo tee  /etc/apt/sources.list.d/pgdg.list

sudo apt-get update
sudo apt-get install -y postgresql postgresql-contrib

# Enable pgvector extension
cd /tmp
git clone --branch v0.5.0 https://github.com/pgvector/pgvector.git
cd pgvector
sudo apt install postgresql-server-dev-15
make
sudo make install
