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

    def __init__(self, uid, title, bio="", course_ids=[]):
        '''
        TutorExperience constructor
        :param: uid UID of user that these stats belong to
        :param: q_text Text of the question
        :param: bio Short text biography about the tutor that describes what
                the tutor knows
        :param: course_ids List of courses a tutor can answer questions about
        '''
        super().__init__(uid)
        self.title = title
        self.bio = bio
        self.course_ids = course_ids

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
