#!/bin/bash

if [ $# -lt 1 ]; then
    echo "Usage: $0 <task>"
    exit 1
fi

cd ./app/database

if [ "$1" = "reinit" ]; then
    bash ./delete.sh
    bash ./create.sh
    python3 populate.py
    rm ../audio_files/*
    cp ./build_data/*.wav ../audio_files/

elif [ "$1" = "create" ]; then
    bash ./create.sh
    python3 populate.py
    cp ./build_data/*.wav ../audio_files/

elif  [ "$1" = "delete" ]; then
    bash ./delete.sh
    rm ../audio_files/*

fi

cd ../../
