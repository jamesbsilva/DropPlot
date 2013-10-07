#!/usr/bin/env python
##########################################################
#
#            DropPlot
#
#       Drag and drop plotting is done using matplotlib and wx.
#   Numpy is required as well as brewer2mpl.
#
#   @author : jbsilva
#
##########################################################

import wx
import numpy as np
import os.path
import brewer2mpl
import matplotlib as mpl
import matplotlib.pyplot as plt

class PlottingManager():
    def __init__(self):
        # Change the default colors
        bmap = brewer2mpl.get_map('Set2', 'qualitative', 7)
        colors = bmap.mpl_colors
        mpl.rcParams['axes.color_cycle'] = colors
        self.plotParamsFilename = "plotparams.dat"
        self.font = {'fontname':'Lucid','fontsize':30, 'fontweight':'bold'}
        self.fontax = {'fontname':'Lucid','fontsize':24, 'fontweight':'bold'}

    def plotData(self,filename, xcol, ycol, xaxis, yaxis, titleIn, labelIn, plotLogX = False,plotLogY = False,histMode = False):
        print "Plotting : ", str(filename)
        data = np.genfromtxt(filename, unpack=True)
        if plotLogX:
            tx = np.log(data[xcol]);
        else:
            tx = data[xcol]; ty = data[ycol]
        if plotLogY:
            ty = np.log(data[ycol])
        else:
            ty = data[ycol]
        plt.xlabel(xaxis, **self.fontax); plt.ylabel(yaxis, **self.fontax);
        plt.title(titleIn,**self.font)
        if histMode:
            if labelIn is None:
                plt.hist(tx)
            else:
                plt.hist(tx,label=labelIn)
        else:
            if labelIn is None:
                plt.plot(tx, ty, marker='o')
            else:
                plt.plot(tx, ty, marker='o',label=labelIn)
        print "Done Plotting"

    def checkForPlotParams(self,filename,xcol,ycol,xaxis,yaxis, titleIn, plotLgX, plotLgY):
        paramFile = self.parseDir(filename)+self.plotParamsFilename
        if os.path.exists(paramFile):
            strFile = open(paramFile,"r")
            paramRaw = strFile.read()
            inL = paramRaw.find("xCol(")
            if inL is not -1:
                inL += 5
                inR = paramRaw.find(")",inL,len(paramRaw))
                xcol = int(paramRaw[inL:inR])
            inL = paramRaw.find("yCol(")
            if inL is not (-1):
                inL += 5
                inR = paramRaw.find(")",inL,len(paramRaw))
                ycol = int(paramRaw[inL:inR])
            inL = paramRaw.find("xTitle(")
            if inL is not (-1):
                inL += 7
                inR = paramRaw.find(")",inL,len(paramRaw))
                xaxis = paramRaw[inL:inR]
            inL = paramRaw.find("yTitle(")
            if inL is not (-1):
                inL += 7
                inR = paramRaw.find(")",inL,len(paramRaw))
                yaxis = paramRaw[inL:inR]
            inL = paramRaw.find("Title(")
            if inL is not (-1):
                inL += 6
                inR = paramRaw.find(")",inL,len(paramRaw))
                titleIn = paramRaw[inL:inR]
            inL = paramRaw.find("xLog()")
            if inL is not (-1):
                plotLgX = True
            else:
                plotLgX = False
            inL = paramRaw.find("yLog()")
            if inL is not (-1):
                plotLgY = True
            else:
                plotLgY = False
        return [xcol,ycol,xaxis,yaxis, titleIn, plotLgX, plotLgY,self.parseLabel(filename)]

    def parseDir(self,file):
        name= file.split("/")
        dirOut = file[:-len(name[len(name)-1])]
        return dirOut

    def parseLabel(self,filename):
        inL = filename.find("-label(")
        if inL is (-1):
            return None
        inL += 7
        inR = filename.find(")",inL,len(filename))
        return filename[inL:inR]

    def showPlot(self):
        plt.grid(True);
        plt.legend();
        plt.show()

MENU_FILE_EXIT = wx.NewId()
DRAG_SOURCE    = wx.NewId()

class PlotFileDropTarget(wx.TextDropTarget):
    def __init__(self, PlottingManager, obj):
        wx.TextDropTarget.__init__(self)
        self.obj = obj
        self.xCol = 0; self.yCol = 1
        self.xTitle = "x"; self.yTitle = "y";
        self.plotTitle = "plot";
        self.plotLogX = False; self.plotLogY = False;
        self.plotManager = PlottingManager
        self.plotNow = True
        self.HistNow = False


    def OnDropText(self, x, y, data):
        self.obj.WriteText("Will plot | "+data[7:-2] + '\n\n')
        [self.xCol,self.yCol,self.xTitle,self.yTitle,self.plotTitle, self.plotLogX, self.plotLogY,labelOut] = self.plotManager.checkForPlotParams(data[7:-2],self.xCol,self.yCol,self.xTitle,self.yTitle,self.plotTitle, self.plotLogX, self.plotLogY)
        self.plotManager.plotData(data[7:-2],self.xCol,self.yCol,self.xTitle,self.yTitle,self.plotTitle, labelOut , self.plotLogX,self.plotLogY,self.HistNow)
        if self.plotNow:
            self.plotManager.showPlot()

class MainWindow(wx.Frame):
    def __init__(self,parent,id,title):
        wx.Frame.__init__(self,parent, wx.ID_ANY, title, size = (750,600), style=wx.DEFAULT_FRAME_STYLE|wx.NO_FULL_REPAINT_ON_RESIZE)

        self.SetBackgroundColour(wx.WHITE)
        # Setup plotting manager
        self.plotManager = PlottingManager()

        # setup menu bar
        menuBar = wx.MenuBar()
        menu1 = wx.Menu()
        menu1.Append(MENU_FILE_EXIT, "Exit", "Quit DropPlot")
        menuBar.Append(menu1, "&File")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, MENU_FILE_EXIT, self.CloseWindow)

        # setup dragdrop box
        self.text = wx.TextCtrl(self, DRAG_SOURCE, "", pos=(0,0), size=(750,200), style = wx.TE_MULTILINE|wx.HSCROLL)
        self.dt1 = PlotFileDropTarget(self.plotManager,self.text)
        self.text.SetDropTarget(self.dt1)

        wx.EVT_RIGHT_DOWN(self.text, self.OnDragInit)

        # add buttons
        self.dt1.xCol = 0; self.dt1.yCol = 1;
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL); self.buttons = []
        self.sizer3 = wx.BoxSizer(wx.HORIZONTAL);

        # first row of buttons
        self.buttons.append(wx.Button(self, -1, "X Column &"))
        self.sizer2.Add(self.buttons[0], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeXaxis,self.buttons[0])

        self.buttons.append(wx.Button(self, -1, "Y Column &"))
        self.sizer2.Add(self.buttons[1], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeYaxis,self.buttons[1])

        self.buttons.append(wx.Button(self, -1, "X Title &"))
        self.sizer2.Add(self.buttons[2], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeXtitle,self.buttons[2])

        self.buttons.append(wx.Button(self, -1, "Y Title  &"))
        self.sizer2.Add(self.buttons[3], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeYtitle,self.buttons[3])

        self.buttons.append(wx.Button(self, -1, "Plot Title  &"))
        self.sizer2.Add(self.buttons[4], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ChangeTitle,self.buttons[4])

        # second row of buttons
        self.buttons.append(wx.Button(self, -1, "Hold For Multi Plots  &"))
        self.sizer3.Add(self.buttons[5], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.ShowPlots,self.buttons[5])

        self.buttons.append(wx.Button(self, -1, "Start Histogram &"))
        self.sizer3.Add(self.buttons[6], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.SetHist,self.buttons[6])

        self.buttons.append(wx.Button(self, -1, "Log Scale X &"))
        self.sizer3.Add(self.buttons[7], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.SetLogX,self.buttons[7])

        self.buttons.append(wx.Button(self, -1, "Log Scale Y &"))
        self.sizer3.Add(self.buttons[8], 1, wx.EXPAND)
        self.Bind(wx.EVT_BUTTON, self.SetLogY,self.buttons[8])

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.text, 1, wx.EXPAND)
        self.sizer.Add(self.sizer2, 0, wx.EXPAND)
        self.sizer.Add(self.sizer3, 0, wx.EXPAND)

        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        self.Show()

    def ChangeXtitle(self,event):
        self.boxCol1 = wx.TextEntryDialog(None,"X- Axis Title? ","X-axis","x")
        if self.boxCol1.ShowModal() == wx.ID_OK :
            self.dt1.xTitle = self.boxCol1.GetValue()

    def ChangeYtitle(self,event):
        self.boxCol1 = wx.TextEntryDialog(None,"Y- Axis Title? ","Y-axis","y")
        if self.boxCol1.ShowModal() == wx.ID_OK :
            self.dt1.yTitle = self.boxCol1.GetValue()

    def SetLogX(self,event):
        if self.dt1.plotLogX:
            self.dt1.plotLogX = False
            self.buttons[7].SetLabel('Log Scale X On')
        else:
            self.dt1.plotLogX = True
            self.buttons[7].SetLabel('Log Scale X Off')

    def SetLogY(self,event):
        if self.dt1.plotLogY:
            self.dt1.plotLogY = False
            self.buttons[8].SetLabel('Log Scale Y On')
        else:
            self.dt1.plotLogY = True
            self.buttons[8].SetLabel('Log Scale Y Off')

    def ShowPlots(self,event):
        if self.dt1.plotNow:
            self.dt1.plotNow = False
            self.buttons[5].SetLabel('Show Multi Plots')
        else:
            self.dt1.plotNow = True
            self.plotManager.showPlot()
            self.buttons[5].SetLabel('Hold For Multi Plots')

    def SetHist(self,event):
        if self.dt1.HistNow:
            self.dt1.HistNow = False
            self.buttons[6].SetLabel('Start Histograms')
        else:
            self.dt1.HistNow = True
            self.buttons[6].SetLabel('Start Plots')

    def ChangeTitle(self,event):
        self.boxCol1 = wx.TextEntryDialog(None,"Plot Title? ","X-axis","0")
        if self.boxCol1.ShowModal() == wx.ID_OK :
            self.dt1.plotTitle = self.boxCol1.GetValue()

    def ChangeXaxis(self,event):
        self.boxCol1 = wx.TextEntryDialog(None,"X- Axis Column? ","X-axis","0")
        if self.boxCol1.ShowModal() == wx.ID_OK :
            self.dt1.xCol = int(self.boxCol1.GetValue())

    def ChangeYaxis(self,event):
        self.boxCol1 = wx.TextEntryDialog(None,"Y- Axis Column? ","Y-axis","1")
        if self.boxCol1.ShowModal() == wx.ID_OK :
            self.dt1.yCol = int(self.boxCol1.GetValue())

    def CloseWindow(self, event):
        self.Close()

    def OnDragInit(self, event):
        tdo = wx.PyTextDataObject(self.text.GetStringSelection())
        tds = wx.DropSource(self.text)
        tds.SetData(tdo)
        tds.DoDragDrop(True)

class DropPlot(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, "DropPlot - Drag data to plot")
        self.SetTopWindow(frame)
        return True

# main loop
app = DropPlot(0)
app.MainLoop()
