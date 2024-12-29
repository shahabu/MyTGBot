#!/bin/bash

echo "Start bot process..."
python3 main.py & 


sleep 3

echo "Start scanner process..."
python3 scanner_channels.py &

wait  
