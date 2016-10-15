#!/usr/bin/python3
##
## File:    mmcga_server.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Main server program for the MMCGA Project
##

# Python libraries
import pika
import sys

# project libraries
from utils.macros import *
from utils.utils import printd
from user.student import Student
from user.tutor import Tutor
from user.queue_stu import QueueStu
from user.queue_tut import QueueTut

#### GLOBALS    ####

# Student and Tutor queues that manage the mentoring center
stu_queue = None
tut_queue = None

#### FUNCTIONS  ####

def msg_callback(ch, method, properties, body):
    '''
    Basic callback function registered with the RMQ connection, passed as a
    function pointer to the server channel listener
    :param: ch RMQ channel
    :param: method RMQ method
    :param: properties RMQ properties
    :param: body RMQ body of the message
    '''
    # perform actions based on message received
    printd("Msg: " + str(body))
    # "registration" commands
    if (method == MSG_TUT_ENTER):
        name = "TODO"
        title = "TODO"
        tut_queue.add(name, title)
        # TODO send return message to client with UID
    elif (method == MSG_TUT_LEAVE):
        # TODO get uid from message
        uid = "TODO"
        tut_queue.remove(uid)
    else:
        printd("Unknown message: " + str(body))

def init():
    '''
    Initializes our run-time variables
    '''
    # I believe that these need to be globalvariables in order for themessage
    # handlers/callback functions to manipulate the queues
    global stu_queue, tut_queue
    stu_queue = QueueStu(SERVER_QUEUE)
    tut_queue = QueueTut();

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
