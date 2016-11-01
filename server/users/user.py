##
## File:    user.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a generic user for the system
##

import uuid
from utils.macros import RIT_EMAIL_EXT

class User:
    '''
    Generic user class
    '''

    def __init__(self, rit_name, passwd, f_name, l_name):
        '''
        User contstructor
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        '''
        # basic user information
        self.name   = rit_name
        self.email  = self.name + RIT_EMAIL_EXT
        self.passwd = passwd
        self.f_name = f_name
        self.l_name = l_name
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
        # can check against UIDs directly
        if (isinstance(user, str)):
            return self.uid == user
        # other types are not allowed
        if (isinstance(user, User)):
            return self.uid == user.uid
        return False

    def __hash__(self):
        '''
        Returns the hash code of a user
        '''
        return hash(self.uid)

    def q_count(self):
        '''
        Returns the number of questions a user has asked/answered
        :return: Current question count
        '''
        return self.q_count

    def q_increment(self):
        '''
        Increments the number of questions a user has asked/answered
        :return: Current question count
        '''
        self.q_count += 1
        return self.q_count()

    @staticmethod
    def get_uid(uid):
        '''
        Extracts a UID out of a User object or UID string; handles implicit
        typing issues
        :param: uid UID string or User to extract a UID out of
        :return: UID string or None
        '''
        if (isinstance(uid, str)):
            return uid
        elif (isinstance(uid, User)):
            return uid.uid
        return None
