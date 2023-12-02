#!/bin/bash

# Variables
DB_NAME="convolens"
DB_USER="postgresql"
DB_PASS="psql1234"

# Drop
PGPASSWORD=$DB_PASS psql -U $DB_USER -d convolens -h localhost -p 5432 -f ./sql/DROP.sql

# Drop the database
sudo -u postgres psql -c "DROP DATABASE IF EXISTS $DB_NAME;"

# Drop the role (user)
sudo -u postgres psql -c "REVOKE ALL ON SCHEMA public FROM $DB_USER;"
sudo -u postgres psql -c "DROP ROLE IF EXISTS $DB_USER;"

# Stop PostgreSQL service
sudo systemctl stop postgresql
sudo systemctl disable postgresql
