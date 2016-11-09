##
## File:    user.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a generic user for the system
##

import uuid
from datagrams.user_stats import UserStats
from utils.macros import RIT_EMAIL_EXT

class User:
    '''
    Generic user class
    '''

    def __init__(self, rit_name="", passwd="", f_name="", l_name="",
            uid_prefix="", init_map=None):
        '''
        User constructor, uses optional named parameters
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :param: uid_prefix Prefix for UIDs to identify user types
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        # basic user information
        self.name   = rit_name
        self.email  = self.name + RIT_EMAIL_EXT
        self.passwd = passwd
        self.f_name = f_name
        self.l_name = l_name
        # for now, unique IDs are generated at random
        self.uid = uid_prefix + str(uuid.uuid4())
        # datagram for storing user statistics
        self.stats = UserStats(self.uid)

        # override attributes in the map
        if (init_map != None):
            if ("name" in init_map):
                self.name = init_map["name"]
            if ("email" in init_map):
                self.email  = init_map["email"]
            if ("passwd" in init_map):
                self.passwd  = init_map["passwd"]
            if ("f_name" in init_map):
                self.f_name  = init_map["f_name"]
            if ("l_name" in init_map):
                self.l_name  = init_map["l_name"]
            if ("uid" in init_map):
                self.uid  = init_map["uid"]
            # user-defined objects will need to call the map constructor
            if ("stats" in init_map):
                self.stats = UserStats(init_map=init_map["stats"])

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

    def get_stats(self):
        '''
        Returns the UserStats datagram associated with this user
        :return: UserStats object belonging to this user
        '''
        return self.stats

    def str_stats(self):
        '''
        Dumps the statistics of a user as a string
        :return: Stats as a string
        '''
        return str(self.get_stats())

    def q_increment(self):
        '''
        Increments the number of questions a user has asked/answered
        :return: Current question count
        '''
        return self.stats.q_increment("q_count")

    def login_increment(self):
        '''
        Increments the number of logins a user has had
        :return: Current login count
        '''
        return self.stats.stat_increment("login_count")

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
