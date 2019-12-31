# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 21:52:08 2019

@author: gebruiker
"""
import re

class Organism():
    __sequence = ""
    __header = ""
    __name = ""
    
    def __init__(self, sequence, header, name):
        self.__sequence = sequence
        self.__header = header
        self.__name = name
        
    
    def __str__(self):
        return "Organism name: {}\nFasta data:\n {}\n{}\n".format(self.__name, self.__header, self.__sequence)
      
     
    def getName(self):
        return self.__name
    
    
    def getSimpleName(self):
        fullName = self.__name
        return fullName.split(" (")[0]
    
    
    def getSequence(self):
        return self.__sequence
    
    
    def getHeader(self):
        return self.__header
    
        
    @classmethod
    def getFromUneditedData(cls, headerWithName, uneditedSequence):
        headerSearch = re.search("^>\S*", headerWithName)
        header = headerSearch.group()
        
        # Name search was hard as sometimes there a more than 1 set of []
        nameSearch = re.search("\.\s*\[.+\]", headerWithName)
        if nameSearch == None:
            print(headerWithName)
            name = "Unknown"
        else:
            name = nameSearch.group().strip(".").strip().strip("[").strip("]")
            
        seqSearch = re.search("^\w+", uneditedSequence)
        sequence = seqSearch.group()
        
        return cls(sequence, header, name)
            
            
    
    
    
    