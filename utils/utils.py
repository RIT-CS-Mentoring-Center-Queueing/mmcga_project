#!/usr/bin/python3
##
## File:    utils.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python file that contains basic utility functions
##

import sys

#### GLOBALS    ####

#### FUNCTIONS  ####

def read_file(fd):
    '''
    Reads in the file, line by line
    :param: fd Name of the file
    :return: Contents of the file, as an array of line strings
    '''
    data = []
    for line in open(fd):
        data += [line]
    return data

def write_file(data, fd):
    '''
    Writes to a file, line by line
    :param: data Lines of the file to write
    :param: fd Name of the file to write
    '''
    fptr = open(fd, 'w')
    for line in data:
        fptr.write(line)
    fptr.close()
        
