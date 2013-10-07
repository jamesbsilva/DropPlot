DropPlot
==========

Plots data which is dragged and dropped into window. Uses wx,numpy, and matplotlib.

Setup 
------
You can make sure some dependencies by using the installDependencies.sh script as sudo

sudo sh installDependencies.sh

Choose a directory to place files in then run

sh setupAlias.sh

to setup dropplot command in terminal

and

sh makeDesktopFile.sh

to create a desktop file which should be draggable into your launcher or placed in ~/.config/autostart if looking for autostart 

sh make

Directory plot parameter files 
------
If directory contains a file plotparams.dat 

then 

plot parameters will be set based on parsed file.

plotparams.dat example contents
------
xTitle(some x axis) # x axis title

yTitle(y label here) # y axis title

Title(new plot) # plot title

xCol(1) # x axis data is second column

yCol(0) # y axis data is first column

xLog() # plot x-axis using log scale

yLog() # plot y-axis using log scale


Data labels in file name
------

if drag dropped filename has "-label()" in the filename the parentheses will label the data.

-label(my data)

will label the data as "my data".
