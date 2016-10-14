##
## File:    tutor.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a tutor user for the system
## This is someone who can answer questions
##

from user import User
from student import Student

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
        # indicates if the tutor is available to answer questions
        self.busy = False
        # list of student IDs of students this tutor has helped
        self.helped = []

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Tutor (" + self.title + ")" + super().__str__()

    def busy_status(self):
        '''
        Indicates if a tutor is busy or able to help someone
        :return: True if they are busy, False otherwise
        '''
        return self.busy

    def help(self, stu):
        '''
        A tutor helps a student
        :param: stu Student to help
        :return: UID of student that was just helped or None
        '''
        if (type(stu) is Student):
            self.helped.append(stu.uid)
            self.busy = True
            return stu.uid
        return None

    def done(self):
        '''
        A tutor is done helping a student
        :return: UID of student that was just helped or None
        '''
        self.busy = False
        if (len(self.helped) != 0):
            return self.helped[-1]
        else:
            return None
