#!/bin/bash

echo "Doctest README.txt"
echo "=================="
python3 -m doctest -v README.txt
echo 

echo "Unit tests"
echo "=========="
python3 -m unittest -v
