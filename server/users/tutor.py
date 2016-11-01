##
## File:    tutor.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a tutor user for the system
##              This is someone who can answer questions
##

from users.user import User
from users.student import Student
from utils.macros import UID_PREFIX_TUT

class Tutor(User):
    '''
    Tutor user class
    '''

    def __init__(self, rit_name, passwd, f_name, l_name, title):
        '''
        Tutor contstructor
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :param: title Job title of the Tutor (TA, SLI, etc)
        '''
        super().__init__(rit_name, passwd, f_name, l_name)
        # identify the type of user in the UID string 
        self.uid = UID_PREFIX_TUT + self.uid
        # Give the user a title
        self.title = title
        # indicates if the tutor is available to answer questions
        self.busy = False
        # list of student IDs of students this tutor has helped
        self.helped = []

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Tutor(" + self.title + ") " + super().__str__()

    def busy_status(self):
        '''
        Indicates if a tutor is busy or able to help someone
        :return: True if they are busy, False otherwise
        '''
        return self.busy

    def help(self, stu_uid):
        '''
        A tutor helps a student
        :param: stu_uid UID/Student object to help
        :return: UID of student that was just helped or None
        '''
        stu_uid = User.get_uid(stu_uid)
        if (stu_uid != None):
            self.helped.append(stu_uid)
            self.busy = True
            return stu_uid
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

    @staticmethod
    def is_tut(uid):
        '''
        Checks if a UID or User is a tutor UID
        :param: uid UID string or User to extract a UID out of
        :return: True if the UID is a Tutor, False otherwise
        '''
        uid = User.get_uid(uid)
        if (uid != None):
            return UID_PREFIX_TUT == uid[:len(UID_PREFIX_TUT)]
        return False
