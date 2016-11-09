##
## File:    tutor_experience.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a datagram for storing data about a
##              Tutor's experience
##

from datagrams.datagram import Datagram

class TutorExperience(Datagram):
    '''
    Class for storing information about a Tutor's experience
    '''

    def __init__(self, uid="", title="", bio="", course_ids=[], init_map=None):
        '''
        TutorExperience constructor, uses optional named parameters
        :param: uid UID of user that these stats belong to
        :param: q_text Text of the question
        :param: bio Short text biography about the tutor that describes what
                the tutor knows
        :param: course_ids List of courses a tutor can answer questions about
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        super().__init__(uid, init_map)
        # class attributes
        self.title = title
        self.bio = bio
        self.course_ids = course_ids

        # override attributes in the map
        if (init_map != None):
            if ("title" in init_map):
                self.title  = init_map["title"]
            if ("bio" in init_map):
                self.bio  = init_map["bio"]
            if ("course_ids" in init_map):
                self.course_ids  = init_map["course_ids"]

    def __str__(self):
        '''
        Converts to a string equivalent
        '''
        title = "Tutor experience for " + self.uid + "\n"
        return title + super().__str__()

    def get_title(self):
        '''
        Returns the title of a Tutor
        :return: Job title of the tutor
        '''
        return self.title
