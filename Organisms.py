# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 21:52:08 2019

@author: Thijs Weenink

Organisme objecten, met naam, sequentie en de header van de data.
"""
import re

class Organism():
    __sequence = ""
    __header = ""
    __name = ""

    # Constructor
    def __init__(self, sequence, header, name):
        self.__sequence = sequence
        self.__header = header
        self.__name = name

    # De string die het object geeft.
    def __str__(self):
        return "Organism name: {}\nFasta data:\n {}\n{}\n".format(self.__name, self.__header, self.__sequence)


    # Getters
    def getName(self):
        return self.__name


    def getSimpleName(self):
        fullName = self.__name
        return fullName.split(" (")[0]


    def getSequence(self):
        return self.__sequence


    def getHeader(self):
        return self.__header

    # Methode om de data uit de header en sequentie te halen,
    # en er een Organism object van te maken.
    @classmethod
    def getFromUneditedData(cls, headerWithName, uneditedSequence):
        headerSearch = re.search("^>\S*", headerWithName)
        header = headerSearch.group()

        # Zoeken naar de naam in []
        nameSearch = re.search("\.\s*\[.+\]", headerWithName)
        if nameSearch == None:
            print(headerWithName)
            name = "Unknown"
        else:
            name = nameSearch.group().strip(".").strip().strip("[").strip("]")

        # Zoeken naar alleen de sequentie, zonder de extra text erachter.
        seqSearch = re.search("^\w+", uneditedSequence)
        sequence = seqSearch.group()

        return cls(sequence, header, name)
