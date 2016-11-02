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

    def __init__(self, uid, q_text, course_id, assignment=""):
        '''
        QuestionTicket constructor
        :param: uid UID of user that these stats belong to
        :param: q_text Text of the question
        :param: course_id Course associated with the question
        :param: assignment Assignment name/identifier
        '''
        super().__init__(uid)
        self.q_text = q_text
        self.course_id = course_id
        self.assignment = assignment

    def __str__(self):
        '''
        Converts to a string equivalent
        '''
        title = "QuestionTicket from " + self.uid + "\n"
        return title + super().__str__()

