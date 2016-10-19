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
        else:
            return None

    def pop(self):
        '''
        Removes a student from the front of the queue
        :return: Student at the top of the queue or None if empty
        '''
        if not(self.is_empty()):
            return self.queue.pop(0)
        else:
            return None

    def push(self, stu):
        '''
        Adds a student to the back of the queue
        :param: stu Student object or the name of a Student to add
        '''
        if (type(stu) is str):
            stu = Student(stu)
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
        :param: stu Student object or Student UID to purge
        :return: Student purged or None if there's an error
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
    stu0 = Student("Alice")
    stu1 = Student("Bob")
    stu2 = Student("Oscar")
    tut0 = Tutor("Tutor", "SLI")
    queue = QueueStu("Primary Queue");
    print("===== Push commands =====")
    print(queue.len() == 0)
    print(queue.is_empty() == True)
    queue.push(stu0)
    queue.push(stu1)
    queue.push(stu2)
    queue.push(tut0)    # This should not be pushed
    print(queue.len() == 3)
    print(queue.is_empty() == False)
    print(str(queue))
    print("===== Pop/Top commands =====")
    print(queue.top())
    print(queue.top() == stu0)
    print(queue.pop() == stu0)
    print(str(queue))
    print("===== Purge commands =====")
    print(queue.purge(tut0) == None)
    print(queue.purge(stu2) == stu2)
    print(queue.purge_all() == None)
    print(str(queue))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.tutor import Tutor
    main()
