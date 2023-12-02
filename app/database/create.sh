#!/bin/bash

# Variables
DB_NAME="convolens"
DB_USER="postgresql"
DB_PASS="psql1234"

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create a database
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"

# Create a user with a password
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"

# Grant privileges to the user on the database
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"
sudo -u postgres psql -c "GRANT ALL ON SCHEMA public TO $DB_USER;"
sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"

# Add vector support
sudo -u postgres psql -d $DB_NAME -c "CREATE EXTENSION vector;"

# Create schema
PGPASSWORD=$DB_PASS psql -U $DB_USER -d convolens -h localhost -p 5432 -f ./sql/DDL.sql

