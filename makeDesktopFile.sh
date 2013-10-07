#!/bin/bash
# This creates a desktop file based on current directory.
# -jbsilva.

# remove old version
rm DropPlot.desktop

# create desktop file
echo "[Desktop Entry]" >> DropPlot.desktop
echo "Encoding=UTF-8 " >> DropPlot.desktop
echo "Version=1.0" >> DropPlot.desktop
echo "Name=Drop Plot" >> DropPlot.desktop
echo "Comment=Drag and drop plotting" >> DropPlot.desktop
echo "Exec=python $(pwd)/DropPlot.py" >> DropPlot.desktop
echo "Icon=$(pwd)/dpicon.png" >> DropPlot.desktop
echo "Categories=GNOME;Application;" >> DropPlot.desktop
echo "Type=Application" >> DropPlot.desktop
echo "Terminal=false" >> DropPlot.desktop
echo "X-Ayatana-Desktop-Shortcuts=Regular;" >> DropPlot.desktop
echo "Name[en_US]=Drop Plot" >> DropPlot.desktop
