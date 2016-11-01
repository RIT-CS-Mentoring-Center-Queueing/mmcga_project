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

    def __dispatch_tut(self):
        '''
        Checks if a tutor is currently available and someone is waiting for a
        quetion to be answered. If both are true, a Tutor is dispatched to help
        :return: Tutor dispatched or None if there isn't one
        '''
        # check if there is a tutor available to dispatch
        if not(self.tut_queue.is_empty() and self.stu_queue.is_empty()):
            # get the UID of the next available tutor and user
            tut_uid = self.tut_queue.next()
            stu_uid = self.stu_queue.pop()
            # update the tutor
            tut = self.bunny.fetch_user(tut_uid)
            stu = self.bunny.fetch_user(stu_uid)
            tut.help(stu_uid)
            # TODO alert users of the change
            tbl = {}
            tbl[MSG_PARAM_METHOD]  = MSG_USER_HELPED
            tbl[MSG_PARAM_STU_UID] = stu_uid
            tbl[MSG_PARAM_TUT_UID] = tut_uid
            self.bunny.send_msg(stu_uid, tbl)
            slef.bunny.send_msg(tut_uid, tbl)
        return None

    def register_stu(self, rit_name, passwd, f_name, l_name)
        '''
        Registers a student with the system
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :return: New user object
        '''
        user = Student(rit_name, passwd, f_name, l_name)
        self.bunny.register(user)
        self.stu_queue.push(user)
        return user

    def register_tut(self, rit_name, passwd, f_name, l_name, title="")
        '''
        Registers a tutor with the system
        :param: rit_name Username of the user (RIT email, sans @rit.edu)
        :param: passwd Password, encrypted by client
        :param: f_name First name of the user
        :param: l_name Last name of the user
        :param: title Optional title of the tutor
        :return: New user object
        '''
        user = Tutor(rit_name, passwd, f_name, l_name, title)
        self.bunny.register(user)
        self.tut_queue.add(user)
        # newly registered tutors should check the queue Student queue
        self.__dispatch_tut():
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

    def stu_ask_q(self, stu_uid):
        '''
        Function that gets called when a student has a question to be answered
        :param: stu_uid Student object/UID asking the question
        '''
        self.stu_queue.push(stu_uid)
        # stats: track questions asked
        stu = self.bunny.fetch_user(stu_uid)
        stu.q_increment()
        # student should cause a check to dispatch a tutor
        self.__dispatch_tut():

    def tut_ans_q(self, tut_uid):
        '''
        Function that gets called when a tutor has just answered a question
        :param: tut_uid Tutor object/UID answering a question
        '''
        # stats: track questions asked
        tut = self.bunny.fetch_user(tut_uid)
        tut.q_increment()
        # update tutor state
        tut.done()
        # tutor should see if there is somebody else to help
        self.__dispatch_tut():

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    pass

if __name__ == "__main__":
    main()
