# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 13:26:06 2019

@author: Thijs Weenink

Methodes om line breaks te verwerken.
"""
import re

# Zorgt ervoor dat het bestand, met de line breaks, goed wordt verwerkt.
# Returneerd een zip() van de headers en sequenties
def getData(openedFile, fastaStart = ">"):
    headers = []
    sequences = []
    header = ""
    sequence = []

    atHeader = False

    for index, line in enumerate(openedFile):
        if line != "\n" and index > 4:
            if re.search(fastaStart, line) == None:
                if atHeader and re.search("^\[*", line) != None:
                    headers.append("".join([header, line]))
                    atHeader = False
                else:
                    sequence.append(line.strip("\n").strip("\t"))
            else:
                atHeader = True
                sequences.append("".join(sequence))
                sequence = []
                header = line

    sequences.append("".join(sequence))

    # De eerste index van sequences is leeg, in plaats van fixen,
    # is het negeren van de eerste index makkelijker. Data gaat niet verloren.
    return zip(headers, sequences[1::])


# Oude versie.
def get_headers_and_sequences(file, starting_symbol):
    line = file.readline()
    headers = [line]
    sequences = []
    sequence = ""

    while line:
        line = file.readline()
        result = re.match(starting_symbol, line)
        if result == None:
            sequence += line.strip("\n")
        else:
            sequences.append(sequence)
            sequence = ""
            headers.append(line)

    sequences.append(sequence)

    return headers, sequences
