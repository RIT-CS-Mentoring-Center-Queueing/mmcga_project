##
## File:    question_ticket.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a datagram for storing meta-data
##              about a student question
##

from datagrams.datagram import Datagram

class QuestionTicket(Datagram):
    '''
    Class for storing metadata about a student question
    '''

    def __init__(self, uid="", q_text="", course_id="", assignment="",
            init_map=None):
        '''
        QuestionTicket constructor, uses optional named parameters
        :param: uid UID of user that these stats belong to
        :param: q_text Text of the question
        :param: course_id Course associated with the question
        :param: assignment Assignment name/identifier
        :param: init_map Dictionary that maps class attributes to values
                This map, if it is passed in, will replace all attributes that
                are seen in the dictionary. This is how we load an object from
                JSON in the DB
        '''
        super().__init__(uid, init_map)
        # class attributes
        self.q_text = q_text
        self.course_id = course_id
        self.assignment = assignment

        # override attributes in the map
        if (init_map != None):
            if ("q_text" in init_map):
                self.q_text  = init_map["q_text"]
            if ("course_id" in init_map):
                self.course_id  = init_map["course_id"]
            if ("assignment" in init_map):
                self.assignment  = init_map["assignment"]

    def __str__(self):
        '''
        Converts to a string equivalent
        '''
        title = "QuestionTicket from " + self.uid + "\n"
        return title + super().__str__()

