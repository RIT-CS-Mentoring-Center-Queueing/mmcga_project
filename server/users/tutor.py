##
## File:    tutor.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a tutor user for the system
## This is someone who can answer questions
##

class Tutor(User):
    '''
    Tutor user class
    '''

    def __init__(self, name, title):
        '''
        Tutor contstructor
        :param: name Name of the user
        :param: title Job title of the Tutor (TA, SLI, etc)
        '''
        super().__init__(name)
        self.title = title

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Tutor " + super().__str__()self.name
