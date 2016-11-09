##
## File:    user_stats.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a datagram for storing statistics
##              on users
##

from datagrams.datagram import Datagram

class UserStats(Datagram):
    '''
    Class for storing statistics on a user
    '''

    def __init__(self, uid="", init_map=None):
        '''
        UserStat constructor, uses optional named parameters
        :param: uid UID of user that these stats belong to
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        super().__init__(uid, init_map)
        # number of questions a student has asked or a tutor has answered
        self.q_count = 0
        # number of times logged into the system
        self.login_count = 0

        # override attributes in the map
        if (init_map != None):
            if ("q_count" in init_map):
                self.q_count  = init_map["q_count"]
            if ("login_count" in init_map):
                self.login_count  = init_map["login_count"]

    def __str__(self):
        '''
        Converts to a string equivalent
        '''
        title = "User Stats for " + self.uid + "\n"
        return title + super().__str__()

    def stat_count(self, var_name):
        '''
        Returns the stats measure of a specific variable
        :param: var_name Variable to fetch
        :return: Current variable count
        '''
        return self.__dict__[var_name]

    def stat_increment(self, var_name, value=1):
        '''
        Increments the stats measure of a specific variable
        :param: var_name Variable to increment
        :param: value Optional parameter, how much to increment by
        :return: Current variable count
        '''
        self.__dict__[var_name] += value
        return self.stat_count(var_name)
