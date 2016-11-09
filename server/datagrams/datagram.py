##
## File:    datagram.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a base Datagram object for others to
##              inherit from
##

class Datagram():
    '''
    Base class for Datagrams that provide some basic features
    '''

    def __init__(self, uid="", init_map=None):
        '''
        Base Datagram constructor, uses optional named parameters
        :param: uid UID of user that these stats belong to
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        # class attributes
        self.uid = uid

        # override attributes in the map
        if (init_map != None):
            if ("uid" in init_map):
                self.uid  = init_map["uid"]

    def __str__(self):
        '''
        Converts datagrams to a string equivalent
        '''
        # this is done in a generic way so you don't have to modify the print
        # everytime new datagram properties are added
        result = ""
        for key in self.__dict__:
            result += "  " + str(key) + " -> " + str(self.__dict__[key]) + "\n"
        return result

    def get_params(self):
        '''
        Returns the parameters/attributes of the datagram as a dictionary
        :return: Dictionary mapping of datagram attributes
        '''
        return self.__dict__

