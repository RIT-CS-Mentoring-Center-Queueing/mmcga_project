##
## File:    tutor.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a tutor user for the system
##              This is someone who can answer questions
##

from datagrams.tutor_experience import TutorExperience
from users.user import User
from users.student import Student
from utils.macros import UID_PREFIX_TUT

class Tutor(User):
    '''
    Tutor user class
    '''

    def __init__(self, rit_name="", passwd="", f_name="", l_name="",
            title="", init_map=None):
        '''
        Tutor constructor, uses optional named parameters
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :param: title Job title of the Tutor (TA, SLI, etc)
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        # identify the type of user in the UID string 
        super().__init__(rit_name, passwd, f_name, l_name, UID_PREFIX_TUT,
            init_map)
        # class attributes
        # tutor experience information
        self.exp = TutorExperience(self.uid, title)
        # indicates if the tutor is available to answer questions
        self.busy = False
        # list of student IDs of students this tutor has helped
        self.helped = []

        # override attributes in the map
        if (init_map != None):
            if ("exp" in init_map):
                self.exp = TutorExperience(init_map=init_map["exp"])
            if ("busy" in init_map):
                self.busy  = init_map["busy"]
            if ("helped" in init_map):
                self.helped  = init_map["helped"]

    def __str__(self):
        '''
        Converts user to a string equivalent
        '''
        return "Tutor(" + self.exp.get_title() + ") " + super().__str__()

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
