##
## File:    queue_stu.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that defines a Student Queue data structure for
## the server. For now there will only be one Queue of students, but there
## could be one per Tutor later on
##

from users.student import Student
from users.user import User

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
        result = "===== " + self.name + " =====\n"
        for stu in self.queue:
            result += str(stu) + "\n"
        return result

    def __contains__(self, uid):
        '''
        Checks if user is in the queue
        :param: uid User/UID that identifies who we are looking up
        :return: True if the UID is found, False otherwise
        '''
        uid = User.get_uid(uid)
        return uid in self.queue

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
        :return: Student UID at the top of the queue or None if empty
        '''
        if not(self.is_empty()):
            return self.queue[0]
        else:
            return None

    def pop(self):
        '''
        Removes a student from the front of the queue
        :return: Student UID at the top of the queue or None if empty
        '''
        if not(self.is_empty()):
            return self.queue.pop(0)
        else:
            return None

    def push(self, stu_uid):
        '''
        Adds a student to the back of the queue
        :param: stu_uid UID/Student object to add
        :return: Student UID added or None if there's an error
        '''
        stu_uid = User.get_uid(stu_uid)
        if (Student.is_stu(stu_uid)):
            self.queue.append(stu_uid)
            self.lt_count += 1
            return stu_uid
        return None

    def purge_all(self):
        '''
        Purges all students from the queue
        '''
        self.queue = []

    def purge(self, stu):
        '''
        Purges a student from the queue (at any position in the queue)
        :param: stu Student object or Student UID to purge
        :return: Student UID purged or None if there's an error
        '''
        ret = None
        if ((type(stu) is Student) or (type(stu) is str)):
            for i in range(0, self.len()):
                # equals overloaded to check against UID strings
                if (self.queue[i] == stu):
                    ret = self.queue[i]
                    break
            if (ret != None):
                self.queue.pop(i)
        return ret

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    stu0 = Student("aic4242", "pass", "Alice", "in Chains")
    stu1 = Student("bob8888", "pass", "Bob", "Man")
    stu2 = Student("exo6666", "xkcd", "Evil", "Oscar")
    tut0 = Tutor("tut1234", "pass", "Tutor", "A", "SLI")
    queue = QueueStu("Primary Queue");
    print("##### Push commands #####")
    print(queue.len() == 0)
    print(queue.is_empty() == True)
    queue.push(stu0)
    queue.push(stu1)
    queue.push(stu2)
    queue.push(tut0)    # This should not be pushed
    print(queue.len() == 3)
    print(queue.is_empty() == False)
    print(str(queue))
    print("##### Pop/Top commands #####")
    print(queue.top())
    print(queue.top() == stu0)
    print(queue.pop() == stu0)
    print(str(queue))
    print("##### Purge commands #####")
    print(queue.purge(tut0) == None)
    print(queue.purge(stu2) == stu2)
    print(not(stu2 in queue))
    print(stu1 in queue)
    print(queue.purge_all() == None)
    print(str(queue))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.tutor import Tutor
    main()
