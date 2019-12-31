# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:50:54 2019

@author: gebruiker
"""
import re
import matplotlib.pyplot as plt
import numpy as np
import traceback
from collections import Counter

# Self-made scripts
import fix_linebreaks
from Organisms import Organism


def getProcessedData(relevantOrgs, cutOff):
    return __processDataForPlotting(relevantOrgs, cutOff)


def createPlot(relevantOrgs, cutOff = 2, widthMult = 1, heightMult = 1):
    processedData = __processDataForPlotting(relevantOrgs, cutOff)
    __makePlot(processedData, widthMult, heightMult)
    

def getData(filename, pattern):
    # Opening of file and extracting the data
    fileContents = __fileOpening(filename)
    
    # Only if the data is a zip(), the script continues
    if type(fileContents) == type(zip()):
        organismsList = __getOrganisms(fileContents)
        relevantOrgs = __getRelevantOrganisms(organismsList, pattern)
        return relevantOrgs  
    else:
        return fileContents

#########################################################################################################
# Main method is only here for running from the current script, for all other uses, use the methods above
def __main(filename, pattern):
#    Motif based on the logo made in MEME from the fasta file with human p-loops
#    patternPLoop = "[AG].{4}GK[ST]" # Old one
    
    # Opening of file and extracting the data
    fileContents = __fileOpening(filename)
    
    # Only if the data is a zip(), the script continues
    if type(fileContents) == type(zip()):
        organismsList = __getOrganisms(fileContents)
        relevantOrgs = __getRelevantOrganisms(organismsList, pattern)
        processedData = __processDataForPlotting(relevantOrgs, cutOff = 2)
        __makePlot(processedData, 2.5, 2.5)
        
    else:
        print("An error ({}) has occurred when trying to open the file.".format(fileContents.__class__.__name__))
        traceback.print_tb(fileContents.__traceback__)
 
    
def __processDataForPlotting(organisms, cutOff):
    processedData = Counter([organism.getSimpleName() for organism in organisms])
    if cutOff > 1:
        return {key : processedData[key] for key in processedData if processedData[key] >= cutOff}
    else:
        return processedData


def __makePlot(data, widthMult = 1, heightMult = 1):
    # Base values are the defaults in pyplot
    plotWidth = 6.4*widthMult
    plotHeight = 4.8*heightMult
    
    titleSize = 12*(widthMult)
    xLabelSize = 12*(widthMult/2)
    yLabelSize = 12*(heightMult/2)
    
    # Configuring and making of the bar plot
    plt.figure(figsize=[plotWidth, plotHeight])
    fig = plt.bar(range(len(data)), data.values(), align="center")
    
    # Vertical axis labels and relative text size
    plt.xticks(range(len(data)), data.keys(), rotation=-90, size=xLabelSize)
    
    # Coloring of bars, in a nice rainbow ofcourse
    amountOfData = len(data)
    colors = iter(plt.cm.rainbow(np.linspace(0,1,amountOfData)))
    for i in range(amountOfData):
        c = next(colors)
        fig[i].set_color(c)
    
    # Legend and names
    plt.legend(fig,data.keys())
    plt.title("Amount of motifs in organism", size=titleSize)
    plt.ylabel("Counts", size=xLabelSize)
    plt.xlabel("Organism", size=yLabelSize)
    
    
    # Saving the plot as an image, bbox_inches makes sure the plot doesn't get cut-off.
    plt.savefig("plot.png", bbox_inches="tight", dpi=100)
    
    plt.show()
    
    
def __getRelevantOrganisms(organisms, pattern):
    relevantOrgs = []    
    
    for organism in organisms:
        seq = organism.getSequence()
        if re.search(pattern, seq) != None:
            relevantOrgs.append(organism)
    
    return relevantOrgs


def __getOrganisms(data):
    organismsList = []
    
    for header, sequence in data:
        organismsList.append(Organism.getFromUneditedData(header, sequence))
        
    return organismsList


def __fileOpening(filename):
    try:
        with open(filename) as file:
            data = fix_linebreaks.getData(file)
        return data
    except FileNotFoundError as err:
        return err
    except OSError as err:
        return err
    except Exception as err:
        return err






if __name__ == "__main__":
    __main(filename = "Oefentoets\ploop.fa", pattern =  "G.{2}GAGK[ST]")
    
    
"""
1st Site
GPNGAGKT
GHSGTGKS
GHSGAGKS
GHSGAGKT
GHNGAGKS

2nd Site
GVNGAGKT
GPNGAGKS
GPNGAGKS
GHNGAGKS
GHNGAGKS

"G.{2}GAGK[ST]"

"""