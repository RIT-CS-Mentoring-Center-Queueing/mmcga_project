#!/usr/bin/python3
##
## File:    queue_manager.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: This file defines the QueueManager class that provides high-
## level functionality for managing users in the Mentoring Center.
##

# Python libraries
import pika
import sys

# project libraries
from utils.macros import *
from utils.utils import printd
from utils.bunny import Bunny
from users.student import Student
from users.tutor import Tutor
from users.queue_stu import QueueStu
from users.queue_tut import QueueTut

#### GLOBALS    ####

#### CLASS      ####

class QueueManager:
    '''
    QueueManager object, provides the infrastructure to complete high-level
    queue tasks such as adding/removing users to/from the appropriate queue
    '''

    def __init__(self):
        '''
        Constructs a QueueManager object
        '''
        self.stu_queue = QueueStu(SERVER_QUEUE)
        self.tut_queue = QueueTut()
        self.bunny = Bunny()

    def register_stu(self, name)
        '''
        Registers a student with the system
        :param: name Name of the user
        :return: New user object
        '''
        user = Student(name)
        self.bunny.register(user)
        self.stu_queue.push(user)
        return user

    def register_tut(self, name, title="")
        '''
        Registers a tutor with the system
        :param: name Name of the user
        :param: title Optional title of the tutor
        :return: New user object
        '''
        user = Tutor(name, title)
        self.bunny.register(user)
        self.tut_queue.add(user)
        return user

    def deregister_user(self, uid)
        '''
        Removes a user from the system
        :param: uid UID of user to remove
        :return: Removed UID or None if failed
        '''
        uid = self.bunny.deregister(uid)
        if (uid in self.stu_queue):
            self.stu_queue.purge(uid)
        elif (uid in self.tut_queue):
            self.tut_queue.purge(uid)
        return uid

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    pass

if __name__ == "__main__":
    main()
