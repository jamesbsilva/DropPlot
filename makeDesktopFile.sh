#!/bin/bash
# This creates a desktop file based on current directory.
# -jbsilva.

# remove old version
rm dropplot.desktop

# create desktop file
cp dropbase.desktop dropplot.desktop
echo "Exec=\"$(pwd)/DropPlot.py\"" >> dropplot.desktop
echo "Icon=$(pwd)/dpicon.png" >> dropplot.desktop
echo "Categories=Graphics;Plots;" >> dropplot.desktop
echo "Type=Application" >> dropplot.desktop
echo "Terminal=false" >> dropplot.desktop
echo "X-Ayatana-Desktop-Shortcuts=Regular;" >> dropplot.desktop
echo "Name[en_US]=DropPlot" >> dropplot.desktop
echo " " >> dropplot.desktop

# make DropPlot executable
echo "Making dropplot executable to allow desktop file to run properly"
chmod +x DropPlot.py

