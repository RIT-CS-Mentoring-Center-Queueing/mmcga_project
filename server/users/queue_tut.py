##
## File:    queue_tut.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a Tutor Queue data structure for
## the server. It makes sense to only ever have one queue of tutors and queue
## probably isn't the best term for Tutor management; Tutors can become
## available at any one point and may come and go as their shifts end
##

class QueueTut:
    '''
    Tutor Queue class
    Manages which tutors are on duty and are available to answer questions
    '''

    def __init__(self):
        '''
        Queue constructor
        '''
        # queue implementation is actually two Python sets
        self.busy_queue = set()
        self.free_queue = set()

    def __str__(self):
        '''
        Converts queue to a string equivalent
        '''
        result = "Busy:\n"
        for key in self.busy_queue:
            result += str(self.busy_queue[key]) + "\n"
        result += "Available:\n"
        for key in self.free_queue:
            result += str(self.free_queue[key]) + "\n"
        return result

    def len(self):
        '''
        Returns the length of the queue/number of tutors currently working
        :return: Current length/size of the queue
        '''
        return len(self.busy_queue) + len(self.free_queue)

    def is_empty(self):
        '''
        Checks if the queue is empty
        :return: True if the the queue is empty, otherwise False
        '''
        return self.len() == 0

    def next(self):
        '''
        Returns the next available tutor
        :return: Next available tutor or None if no such tutor is available
        '''
        if (len(self.busy_queue()) != 0):
            # this should be practically random, which is fine
            return next(iter(self.free_queue))
        else
            return None

    def update(self, tut):
        '''
        Update the status of the tutor, based on the current status of the
        tutor instance
        :param: tut Tutor to update
        '''
        if (type(tut) is Tutor):
            # discard is a safe operation and will not crash if the tutor is
            # not in one of these sets
            self.busy_queue.discard(tut)
            self.free_queue.discard(tut)
            # re-assign the tutor
            if (tut.busy_status()):
                self.busy_queue.add(tut)
            else:
                self.free_queue.add(tut)
        else
            return None

    def add(self, tut):
        '''
        Add a tutor to the queue; presumably they just went on duty
        :param: tut Tutor to add the the Tutor queue
        '''
        if (type(tut) is Tutor):
            if (tut.busy_status()):
                self.busy_queue.add(tut)
            else:
                self.free_queue.add(tut)
        else
            return None

    def remove(self, tut):
        '''
        Remove a tutor from the queue; presumably they are now off duty
        '''
        if (tut.busy_status()):
            self.busy_queue.discard(tut)
        else:
            self.free_queue.discard(tut)

    def purge_all(self):
        '''
        Purges all tutors from the queue
        '''
        self.busy_queue = set()
        self.free_queue = set()
