"""
Name: DataFormatter.py
Version: 0.01
Purpose: Format array in file to usable format
Author: Graham Mark Broadbent
Date: 25/03/19
"""

import logging
from logManager import log

log.info('DataFormatter')
log.info('\tProgram Begin\n')


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

    try:
        raw_data = open(file, 'r').read()    # reads the data from specified file as string
    except:
        log.error('File {} could not be read'.format(file))
        return False

    raw_data = raw_data.replace("[", "")
    raw_data = raw_data.replace(" ", "")
    # raw_data = raw_data.replace("]", "")    # reduces string to essential characters
    # raw_data = raw_data.replace(",", "")

    length = len(raw_data)

    str_num = ""    # Buffer to hold characters for single value

    for i in range(length):
        char = raw_data[i]
        # if not char == " ":    # If char is .|0|1|2
        if not char == "," and not char == "]":    # If char is .|0|1|2
            str_num += char

        # if char == " " or i == length:    # If reached end of number
        if char == "," or char == "]":    # If reached end of number
            num = float(str_num)
            output.append(num)
            str_num = ""    # Resets buffer

    return output
