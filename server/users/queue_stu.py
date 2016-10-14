##
## File:    queue_stu.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a Student Queue data structure for
## the server. For now there will only be one Queue of students, but there
## could be one per Tutor later on
##

class QueueStu:
    '''
    Student Queue class
    Manages who's next based on who currently has unanswered questions
    '''

    def __init__(self, name):
        '''
        Queue constructor
        :param: name Name of the queue
        '''
        self.name = name
        # queue implementation is a Python list
        self.queue = []
        # total "life time" count of students who have entered the queue
        self.lt_count = 0

    def __str__(self):
        '''
        Converts queue to a string equivalent
        '''
        result = self.name + ":\n"
        for stu in self.queue:
            result += str(stu) + "\n"
        return result

    def len(self):
        '''
        Returns the length of the queue
        :return: Current length/size of the queue
        '''
        return len(self.queue)

    def is_empty(self):
        '''
        Checks if the queue is empty
        :return: True if the the queue is empty, otherwise False
        '''
        return self.len() == 0

    def top(self):
        '''
        Returns a student from the front of the queue
        :return: Student at the top of the queue or None if empty
        '''
        if not(self.is_empty()):
            return self.queue[0]
        else
            return None

    def pop(self):
        '''
        Removes a student from the front of the queue
        :return: Student at the top of the queue or None if empty
        '''
        if not(self.is_empty()):
            return self.queue.pop(0)
        else
            return None

    def push(self, stu):
        '''
        Adds a student to the back of the queue
        :param: stu Student to add
        '''
        # some type checking protections have been added to keep tutors or
        # others from being added to the queue
        if (type(stu) is Student):
            self.queue.append(stu)
            self.lt_count += 1

    def purge_all(self):
        '''
        Purges all students from the queue
        '''
        self.queue = []

    def purge(self, stu):
        '''
        Purges a student from the queue (at any position in the queue)
        :param: stu Student to purge
        :return: UID of the student or None if there's an error
        '''
        uid = None
        if (type(stu) is Student):
            for i in range(0, self.len()):
                if (self.queue[i] == stu):
                    uid = stu.uid
                    break
            if (uid != None)
                self.queue.pop(stu)
        return uid
