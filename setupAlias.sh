#!/bin/bash
# This script will setup an alias for drop plot.
# -jbsilva.

if grep -q dropplot= ~/.bashrc; then
    echo "Already registered in bashrc"
    exit 1
fi
echo " " >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "#     Drop Plot" >> ~/.bashrc
echo "#" >> ~/.bashrc
echo "alias dropplot='python $(pwd)/DropPlot.py'" >> ~/.bashrc


