import logging
from logManager import log

log.info('Program Begin\n')


log.info('Importing Packages')
import os
log.debug('\tImported OS')
import numpy as np
log.debug('\tImported Numpy')
log.info('\tImporting Done\n')


def _format_array(file):    # A big clusterfuck of I don't know what
    # log.info('DataFormatter._format called for file {}'.format(file))
    output = []
    rawData = open(file, 'r').read()

    rawData.replace("[", "")
    rawData.replace("]", "")
    rawData.replace(",", "")

    length = len(rawData)

    char = rawData[0]

    for i in range(0, length):
        # log.info('Char: {}'.format(i))
        strNum = ""
        close = False
        char = rawData[i]
        if char == '0' or char == '1' or char == '2' or char == '.':
            strNum += char
            print(strNum)
            close = False

        if char == ' ' or char == ']':
            close = True

        # if close:
            # output.append(float(strNum))
            # print(strNum)

        # print(char)

    return output


def _format_array_v2(file):    # This one actually works :)
    output = []
    rawData = open(file, 'r').read()    # reads the data from specified file as string

    rawData = rawData.replace("[", "")
    rawData = rawData.replace("]", "")    # reduces string to essential characters
    rawData = rawData.replace(",", "")

    length = len(rawData)

    char = rawData[0]

    strNum = ""    # Buffer to hold characters for single value

    for i in range(length):
        char = rawData[i]
        if not char == " ":    # If char is .|0|1|2
            strNum += char

        if char == " " or i == length:    # If reached end of number
            Num = float(strNum)
            output.append(Num)
            strNum = ""    # Resets buffer

    return output
