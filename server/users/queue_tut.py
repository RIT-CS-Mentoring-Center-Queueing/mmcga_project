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

from users.tutor import Tutor

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
        self.busy_queue = {}
        self.free_queue = {}
        self.name = "Tutor Queue"

    def __str__(self):
        '''
        Converts queue to a string equivalent
        '''
        result = "===== " + self.name + " =====\nBusy:\n"
        for key in self.busy_queue:
            result += str(self.busy_queue[key]) + "\n"
        result += "Available:\n"
        for key in self.free_queue:
            result += str(self.free_queue[key]) + "\n"
        return result

    def len(self):
        '''
        Returns the length of the queue/number of tutors currently available
        The busy queue remains relatively hidden because most users don't need
        to know how many tutors are unavailable
        :return: Current length/size of the queue
        '''
        return len(self.free_queue)

    def is_empty(self):
        '''
        Checks if the free queue is empty
        :return: True if the the queue is empty, otherwise False
        '''
        return self.len() == 0

    def next(self):
        '''
        Returns the next available tutor
        :return: Next available tutor or None if no such tutor is available
        '''
        if not(self.is_empty()):
            # this should be practically random, which is fine
            key = next(iter(self.free_queue))
            return self.free_queue[key]
        else:
            return None

    def add(self, tut, title=""):
        '''
        Add a tutor to the queue; presumably they just went on duty
        :param: tut Tutor or the name of a new Tutor to add to the Tutor queue
        :param: title Optional argument gives a Tutor a title
        '''
        # if it's a name, build out a new Tutor object, then add it in
        if (type(tut) is str):
            tut = Tutor(tut, title)
        if (type(tut) is Tutor):
            if (tut.busy_status()):
                self.busy_queue[tut.uid] = tut
            else:
                self.free_queue[tut.uid] = tut

    def remove(self, tut):
        '''
        Remove a tutor from the queue; presumably they are now off duty
        :param: tut Tutor or UID of Tutor to be removed
        :return: Tutor removed or None if there's an error
        '''
        # convert tut to a key/UID
        if (type(tut) is Tutor):
            tut = tut.uid
        if (type(tut) is str):
            val = None
            if (tut in self.busy_queue):
                val = self.busy_queue[tut]
                del self.busy_queue[tut]
            elif (tut in self.free_queue):
                val = self.free_queue[tut]
                del self.free_queue[tut]
            return val
        return None

    def get(self, tut):
        '''
        Get a tutor object from the queue
        :param: tut Tutor or UID of Tutor to retrieve
        :return: Tutor object from the queue structure or None if not found
        '''
        key = ""
        if (type(tut) is Tutor):
            key = tut.uid
        elif (type(tut) is str):
            key = tut
        if (key != ""):
            if (key in self.busy_queue):
                return self.busy_queue[key]
            elif (key in self.free_queue):
                return self.free_queue[key]
        return None

    def update(self, tut):
        '''
        Update the status of the tutor, based on the current status of the
        tutor instance
        :param: tut Tutor or UID of Tutor to update
        :return: tut.busy_status() or None if update failed
        '''
        if ((type(tut) is Tutor) or (type(tut) is str)):
            # remove the tutor from either queue
            self.remove(tut)
            # re-assign the tutor
            self.add(tut)
            # return the current status of the Tutor
            return self.get(tut).busy_status()
        else:
            return None

    def purge_all(self):
        '''
        Purges all tutors from the queue
        '''
        self.busy_queue.clear()
        self.free_queue.clear()

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    tut0 = Tutor("Alice", "SLI")
    tut1 = Tutor("Bob", "TA")
    tut2 = Tutor("Oscar", "Tutor")
    stu0 = Student("Student A")
    stu1 = Student("Student B")
    queue = QueueTut();
    print("===== Add commands =====")
    print(queue.len() == 0)
    print(queue.is_empty() == True)
    queue.add(tut0)
    queue.add(tut1)
    queue.add(tut2)
    queue.add(stu0)    # This should not be pushed
    print(queue.len() == 3)
    print(queue.is_empty() == False)
    print(str(queue))
    print("===== Next/Update commands =====")
    print("next() call:" + str(queue.next()))
    print("next() call:" + str(queue.next()))
    print(tut0.help(stu0) == stu0)
    print(queue.update(tut0) == True)
    print(tut1.help(stu1) == stu1)
    print(queue.update(tut1) == True)
    print("next() call:" + str(queue.next()))
    print(str(queue))
    # tutors finish helping students
    print(tut1.done() == stu1)
    print(queue.update(tut1) == False)
    print(tut0.done() == stu0)
    print(queue.update(tut0) == False)
    print(str(queue))
    print("===== Purge commands =====")
    print(queue.remove(stu0) == None)
    print(queue.remove(tut2) == tut2)
    print(str(queue))
    print(queue.purge_all() == None)
    print(str(queue))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.student import Student
    main()
