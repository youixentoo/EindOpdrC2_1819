# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:50:54 2019

@author: gebruiker
"""
import tkinter as tk
import traceback
from PIL import Image, ImageTk

# Self-made scripts
import CreatePlot


class PLoopGUI():
    
    __data = None
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("P-Loop finder")
        
        self.filler1 = tk.Label(self.root, text="")
        self.filler1.grid(row=0, column=0, columnspan=3, padx=10)
        
        
        self.fileLabel = tk.Label(self.root, text="Enter the filelocation:")
        self.fileLabel.grid(row=1, column=0, sticky="w")
        
        filename = tk.StringVar(self.root, value="Oefentoets\ploop.fa")
        self.fileEntry = tk.Entry(self.root, width=40, borderwidth=2, textvariable=filename)
        self.fileEntry.grid(row=1, column=1, padx=2, sticky="w")
        
        self.fileButton = tk.Button(self.root, text="Open...", command=self._openFile)
        self.fileButton.grid(row=1, column=2, sticky="we")
        
        
        self.patternLabel = tk.Label(self.root, text="Pattern to search:")
        self.patternLabel.grid(row=2, column=0, sticky="w")
        
        
        pattern = tk.StringVar(self.root, value="G.{2}GAGK[ST]")
        self.patternEntry = tk.Entry(self.root, width=20, borderwidth=2, textvariable=pattern)
        self.patternEntry.grid(row=2, column=1, padx=2, sticky="w")
        
        self.fileLoadedLabel = tk.Label(self.root, text="")
        self.fileLoadedLabel.grid(row=2, column=2, sticky="w")
        
        
        self.fileMessageLabel = tk.Label(self.root, text="")
        self.fileMessageLabel.grid(row=3, column=0, columnspan=3, padx=10)
        
        
        self.cutOffLabel = tk.Label(self.root, text="Minimum amount of hits:")
        self.cutOffLabel.grid(row=4, column=0, sticky="w")
        
        cutoff = tk.StringVar(self.root, value="2")
        self.cutOffEntry = tk.Entry(self.root, width=20, borderwidth=2, textvariable=cutoff)
        self.cutOffEntry.grid(row=4, column=1, padx=2, sticky="w")
        
        self.plotVar = tk.BooleanVar()
        self.showPlotCheckBox = tk.Checkbutton(self.root, text="Show plot", variable=self.plotVar)
        self.showPlotCheckBox.grid(row=4, column=2, sticky="w")
        
        
        self.plotWidthLabel = tk.Label(self.root, text="Plot Width multiplier:")
        self.plotWidthLabel.grid(row=5, column=0, sticky="w")
        
        width = tk.StringVar(self.root, value='1')
        self.plotWidthEntry = tk.Entry(self.root, width=20, borderwidth=2, textvariable=width)
        self.plotWidthEntry.grid(row=5, column=1, padx=2, sticky="w")
        
        self.showDataButton = tk.Button(self.root, text="Show Data", command=self._showData)
        self.showDataButton.grid(row=5, column=2, sticky="we")
        
        
        self.plotHeightLabel = tk.Label(self.root, text="Plot Height multiplier:")
        self.plotHeightLabel.grid(row=6, column=0, sticky="w")
        
        height = tk.StringVar(self.root, value="1")
        self.plotHeightEntry = tk.Entry(self.root, width=20, borderwidth=2, textvariable=height)
        self.plotHeightEntry.grid(row=6, column=1, padx=2, sticky="w")
        
        
        self.filler2 = tk.Label(self.root, text="")
        self.filler2.grid(row=7, column=0, columnspan=3, padx=10)
        
        
        self.resultsLabel = tk.Label(self.root, text="", anchor="w")
        self.resultsLabel.grid(row=8, column=0, columnspan=3)
        
        
        
        self.root.mainloop()
        
        
    def _openFile(self):
        self._setFileMessage("")
        filename = self.fileEntry.get()
        pattern = str(self.patternEntry.get())
            
        data = CreatePlot.getData(filename, pattern)
        
        if type(data) != type(list()):
            errorMessage = "An error ({}) has occurred when trying to open the file.".format(data.__class__.__name__)
            traceback.print_tb(data.__traceback__)
            self._setFileLoadedMessage(False)
            self._setFileMessage(errorMessage, "RED")
        else:
            self._setFileLoadedMessage(True)
            self.__data = data
            
    
    def _showData(self):
        try:
            cutOff = int(self.cutOffEntry.get())
        except ValueError as err:
            self._setCutOffEntry(2)
            cutOff = 2
        
        try:
            width = float(self.plotWidthEntry.get())
        except ValueError as err:
            self._setWidthEntry(1)
            width = 1
            
        try:
            height = float(self.plotHeightEntry.get())
        except ValueError as err:
            self._setHeightEntry(1)
            height = 1
            
        if self.plotVar.get():
            self._setResultsLabel("")
             
            CreatePlot.createPlot(self.__data, cutOff, width, height)
            self._showPlot()
        else:
            rawData = CreatePlot.getProcessedData(self.__data, cutOff)
            results = "\n".join(["{}: {}".format(key, rawData[key]) for key in rawData.keys()])
            self._setResultsLabel("Amount of motifs in organism:\n"+results)

        
    def _setFileMessage(self, message, color="BLACK"):
        self.fileMessageLabel['text'] = str(message)
        self.fileMessageLabel.config(fg=color)
        
        
    def _setResultsLabel(self, results):
        self.resultsLabel['text'] = str(results)
#        self.resultsLabel.config(anchor="w")
        
    def _setFileLoadedMessage(self, isLoaded):
        if isLoaded:
            self.fileLoadedLabel["text"] = "Data loaded"
        else:
            self.fileLoadedLabel["text"] = ""
        
        
    def _setCutOffEntry(self, value):
        self.cutOffEntry.delete(0, last="end")
        self.cutOffEntry.insert(0, str(value))
        
        
    def _setWidthEntry(self, value):
        self.plotWidthEntry.delete(0, last="end")
        self.plotWidthEntry.insert(0, str(value))
        
        
    def _setHeightEntry(self, value):
        self.plotHeightEntry.delete(0, last="end")
        self.plotHeightEntry.insert(0, str(value))
        
        
    def _showPlot(self):
        # Easy way to show plot in TK, just load it as a picture.
        loadImage = Image.open('plot.png')                                   
        renderImage = ImageTk.PhotoImage(loadImage)
        
        plotWindow = tk.Toplevel()                                                           
        plotWindow.wm_title("Amounts of motifs in organism")                                          
        img = tk.Label(plotWindow, image=renderImage)                                                 
        img.image = renderImage
        img.pack()
       
    
       
    

PLoopGUI()
    
