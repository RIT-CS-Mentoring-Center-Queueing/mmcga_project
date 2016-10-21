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
        user = self.stu_queue.push(name)
        self.bunny.register(user)
        return user

    def register_tut(self, name, title="")
        '''
        Registers a tutor with the system
        :param: name Name of the user
        :param: title Optional title of the tutor
        :return: New user object
        '''
        user = self.tut_queue.add(name, title)
        self.bunny.register(user)
        return user

    def deregister_user(self, uid)
        '''
        Removes a user from the system
        :param: uid UID of user to remove
        :return: Removed user or None if failed
        '''
        if (uid in self.stu_queue):
            user = self.stu_queue.purge(uid)
            self.bunny.deregister(user)
            return user
        elif (uid in self.tut_queue):
            user = self.tut_queue.purge(uid)
            self.bunny.deregister(user)
            return user
        return None

#### MAIN       ####

def main():
    '''
    Main execution point of the program
    '''
    # initialize our run-time variables
    init()

    # establish connection to server
    print("+ Starting MMCGA Server...")
    socket = pika.BlockingConnection(pika.ConnectionParameters(SERVER_HOST))
    channel = socket.channel()
    # send information to a specific RabbitMQ queue; building this queue for
    # the first time
    channel.queue_declare(queue=SERVER_QUEUE)
    # listen to messages on the primary queue and handle them as need be
    channel.basic_consume(msg_callback,
        queue=SERVER_QUEUE,
        no_ack=True);

    # busy loop that waits for messages to come in; clean-up on ckill
    print("Waiting for messages. CTRL-C to exit")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n- Stopping MMCGA Server...")
        channel.stop_consuming()
    socket.close()

if __name__ == "__main__":
    main()
