##
## File:    student.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a student user for the system
## This is a user who asks questions.
##

from users.user import User

class Student(User):
    '''
    Student user class
    '''

    def __init__(self, name):
        '''
        Student contstructor
        :param: name Name of the user
        '''
        super().__init__(name)

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Student " + super().__str__()
