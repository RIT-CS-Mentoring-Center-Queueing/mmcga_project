##
## File:    student.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a student user for the system
##              This is a user who asks questions.
##

from users.user import User
from utils.macros import UID_PREFIX_STU

class Student(User):
    '''
    Student user class
    '''

    def __init__(self, rit_name="", passwd="", f_name="", l_name="",
            init_map=None):
        '''
        Student constructor, uses optional named parameters
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        # identify the type of user in the UID string 
        super().__init__(rit_name, passwd, f_name, l_name, UID_PREFIX_STU,
            init_map)

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Student " + super().__str__()

    @staticmethod
    def is_stu(uid):
        '''
        Checks if a UID or User is a student UID
        :param: uid UID string or User to extract a UID out of
        :return: True if the UID is a Student, False otherwise
        '''
        uid = User.get_uid(uid)
        if (type(uid) is str):
            return UID_PREFIX_STU == uid[:len(UID_PREFIX_STU)]
        return False
