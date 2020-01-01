# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:50:54 2019

@author: Thijs Weenink

Hierin staat de methodes die nodig zijn om de data te maken en te verwerken.
"""
import re
import matplotlib.pyplot as plt
import numpy as np
import traceback
from collections import Counter

# Zelf gemaakte scripts
import fix_linebreaks
from Organisms import Organism


# Methodes die de andere functies aanroepen in het script.
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
# De main methode is hier alleen voor het uitvoeren van het script op zichzelf.
def __main(filename, pattern):
#    patternPLoop = "[AG].{4}GK[ST]" # Test motief

    # Openen van het bestand en verkrijgen van de data.
    fileContents = __fileOpening(filename)

    # Als alles goed gaat, dan geeft fileContents een zip() terug en worden de rest van de methodes aangeroepen.
    # Als dit niet het geval is, dan is het een error en wordt deze geprint.
    if type(fileContents) == type(zip()):
        organismsList = __getOrganisms(fileContents)
        relevantOrgs = __getRelevantOrganisms(organismsList, pattern)
        processedData = __processDataForPlotting(relevantOrgs, cutOff = 2)
        __makePlot(processedData, 2.5, 2.5)

    else:
        print("An error ({}) has occurred when trying to open the file.".format(fileContents.__class__.__name__))
        traceback.print_tb(fileContents.__traceback__)


# Openen van het bestand en het verkrijgen van de data
# Hierbij wordt gebruik gemaakt van een methode in fix_linebreaks
# Bij een error wordt de error gereturneerd.
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


# Loopt over de lijst met Organismen en checkt of het motief in de sequentie voorkomt.
def __getRelevantOrganisms(organisms, pattern):
    relevantOrgs = []

    for organism in organisms:
        seq = organism.getSequence()
        if re.search(pattern, seq) != None:
            relevantOrgs.append(organism)

    return relevantOrgs


# Telt hoe vaak elke naam van de organismen waarin het motief voorkomen, voorkomt in de lijst.
# cutOff bepaalt hoe vaak ze minimaal in de lijst moeten voorkomen.
def __processDataForPlotting(organisms, cutOff):
    processedData = Counter([organism.getSimpleName() for organism in organisms])
    if cutOff > 1:
        return {key : processedData[key] for key in processedData if processedData[key] >= cutOff}
    else:
        return processedData


# Vult een lijst met Organism objecten van de data
def __getOrganisms(data):
    organismsList = []

    for header, sequence in data:
        organismsList.append(Organism.getFromUneditedData(header, sequence))

    return organismsList


# Maakt een pyplot van de data
def __makePlot(data, widthMult = 1, heightMult = 1):
    # Default waarden van de variabelen in pyplot zelf * eigen waarde.
    plotWidth = 6.4*widthMult
    plotHeight = 4.8*heightMult

    titleSize = 12*(widthMult)
    xLabelSize = 12*(widthMult/2)
    yLabelSize = 12*(heightMult/2)

    # Configuratie en het maken van de staafdiagram
    plt.figure(figsize=[plotWidth, plotHeight])
    fig = plt.bar(range(len(data)), data.values(), align="center")

    # Namen op de verticale as, met een text grootte die schaalt met de grafiek grootte.
    plt.xticks(range(len(data)), data.keys(), rotation=-90, size=xLabelSize)

    # Regenboog kleuring van de grafiek.
    amountOfData = len(data)
    colors = iter(plt.cm.rainbow(np.linspace(0,1,amountOfData)))
    for i in range(amountOfData):
        c = next(colors)
        fig[i].set_color(c)

    # Legenda en namen
    plt.legend(fig,data.keys())
    plt.title("Amount of motifs in organism", size=titleSize)
    plt.ylabel("Counts", size=xLabelSize)
    plt.xlabel("Organism", size=yLabelSize)


    # Opslaan van de grafiek als .png, bbox_inches zorgt ervoor dat het plaatje volledig is.
    plt.savefig("plot.png", bbox_inches="tight", dpi=100)

    plt.show()



# Aanroepen van de main als dit script op zichzelf wordt uitgevoerd.
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
