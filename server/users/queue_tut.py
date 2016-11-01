##
## File:    queue_tut.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a Tutor Queue data structure for
##              the server. It makes sense to only ever have one queue of
##              tutors and queue probably isn't the best term for Tutor
##              management; Tutors can become available at any one point and
##              may come and go as their shifts end
##

from users.tutor import Tutor
from users.user import User

class QueueTut:
    '''
    Tutor Queue class
    Manages which tutors are on duty and are available to answer questions
    '''

    def __init__(self):
        '''
        Queue constructor
        '''
        # queue implementation is actually two Python dictionaries
        # these could be sets but I'd prefer to use dictionaries because they
        # have more functionality. This does mean that the keys are the
        # also the values (UID -> UID)
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

    def __contains__(self, uid):
        '''
        Checks if user is in the queue
        :param: uid User/UID that identifies who we are looking up
        :return: True if the UID is found, False otherwise
        '''
        uid = User.get_uid(uid)
        return (uid in self.busy_queue) or (uid in self.free_queue)

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
        Returns the next available tutor by UID
        :return: Next available tutor or None if no such tutor is available
        '''
        if not(self.is_empty()):
            # this should be practically random, which is fine
            key = next(iter(self.free_queue))
            return key
        else:
            return None

    def add(self, tut_uid, busy_state=False):
        '''
        Add a tutor to the queue; presumably they just went on duty
        :param: tut_uid UID/Tutor object to add
        :param: busy_state Optional parameter specifies if the tutor is busy
        :return: Tutor UID added or None if there's an error
        '''
        # override busy state if tutor object is provided
        if (type(tut_uid) is Tutor):
            busy_state = tut_uid.busy_status()
        tut_uid = User.get_uid(tut_uid)
        if (Tutor.is_tut(tut_uid)):
            if (busy_state):
                self.busy_queue[tut_uid] = tut_uid
            else:
                self.free_queue[tut_uid] = tut_uid
            return tut_uid
        return None

    def remove(self, tut_uid):
        '''
        Remove a tutor from the queue; presumably they are now off duty
        :param: tut_uid Tutor object/UID of Tutor to be removed
        :return: UID of Tutor removed or None if there's an error
        '''
        tut_uid = User.get_uid(tut_uid)
        if (Tutor.is_tut(tut_uid)):
            val = None
            if (tut_uid in self.busy_queue):
                val = self.busy_queue[tut_uid]
                del self.busy_queue[tut_uid]
            elif (tut_uid in self.free_queue):
                val = self.free_queue[tut_uid]
                del self.free_queue[tut_uid]
            return val
        return None

    def update(self, tut_uid, busy_state=False):
        '''
        Update the status of the tutor, based on the current status of the
        tutor instance
        :param: tut_uid UID/Tutor object to update
        :param: busy_state Optional parameter specifies if the tutor is busy
        :return: tut.busy_status() or None if update failed
        '''
        # override busy state if tutor object is provided
        if (type(tut_uid) is Tutor):
            busy_state = tut_uid.busy_status()
        tut_uid = User.get_uid(tut_uid)
        if (Tutor.is_tut(tut_uid)):
            # remove the tutor from either queue
            self.remove(tut_uid)
            # re-assign the tutor
            self.add(tut_uid, busy_state)
            # return the current status of the Tutor
            return busy_state
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
    tut0 = Tutor("aic4242", "pass", "Alice", "in Chains", "SLI")
    tut1 = Tutor("bob8888", "pass", "Bob", "Man", "TA")
    tut2 = Tutor("exo6666", "xkcd", "Evil", "Oscar", "Tutor")
    stu0 = Student("stu1234", "pass", "Student", "A")
    stu1 = Student("stu2345", "word", "Student", "B")
    queue = QueueTut();
    print("##### Add commands #####")
    print(queue.len() == 0)
    print(queue.is_empty() == True)
    queue.add(tut0)
    queue.add(tut1)
    queue.add(tut2)
    queue.add(stu0)    # This should not be pushed
    print(queue.len() == 3)
    print(queue.is_empty() == False)
    print(str(queue))
    print("##### Next/Update commands #####")
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
    print("##### Purge commands #####")
    print(queue.remove(stu0) == None)
    print(queue.remove(tut2) == tut2)
    print(not(tut2 in queue))
    print(tut1 in queue)
    print(tut0 in queue)
    print(str(queue))
    print(queue.purge_all() == None)
    print(str(queue))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.student import Student
    main()
