##
## File:    user.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a generic user for the system
##

import uuid

class User:
    '''
    Generic user class
    '''

    def __init__(self, name):
        '''
        User contstructor
        :param: name Name of the user
        '''
        self.name = name
        # for now, unique IDs are generated at random
        self.uid = str(uuid.uuid4())
        # the number of questions a user has asked/answered
        self.q_count = 0

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return self.name + ", UID: " + self.uid

    def __eq__(self, user):
        '''
        Checks if two users are the same
        :param: user The other user
        '''
        if not(isinstance(user, User)):
            return False
        return self.uid == user.uid

    def __hash__(self):
        '''
        Returns the hash code of a user
        '''
        return self.uid
