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
from utils.bunny import Bunny.parse_msg

#### GLOBALS    ####

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
    msg_map = Bunny.parse_msg(body)
    method = msg_map[MSG_PARAM_METHOD]

    ## "registration" commands ##
    # first-time student registration
    if (method == MSG_STU_ENTER):
        name   = msg_map[MSG_PARAM_USER_NAME]
        passwd = msg_map[MSG_PARAM_USER_PASSWD]
        f_name = msg_map[MSG_PARAM_USER_F_NAME]
        l_name = msg_map[MSG_PARAM_USER_L_NAME]
        queue_manager.register_stu(name, passwd, f_name, l_name)
    # first-time tutor registration
    elif (method == MSG_TUT_ENTER):
        name   = msg_map[MSG_PARAM_USER_NAME]
        passwd = msg_map[MSG_PARAM_USER_PASSWD]
        f_name = msg_map[MSG_PARAM_USER_F_NAME]
        l_name = msg_map[MSG_PARAM_USER_L_NAME]
        title  = msg_map[MSG_PARAM_USER_TITLE]
        queue_manager.register_tut(name, passwd, f_name, l_name, title)
    # returning user login
    elif (method == MSG_USER_ENTER): 
        name   = msg_map[MSG_PARAM_USER_NAME]
        passwd = msg_map[MSG_PARAM_USER_PASSWD]
        queue_manager.login_user(name, passwd)
    # user logs out
    elif (method == MSG_USER_LEAVE):
        uid = msg_map[MSG_PARAM_UID]
        queue_manager.deregister_user(uid)
    ## Student actions ##
    # student asks a question
    elif (method == MSG_STU_QUEST):
        uid = msg_map[MSG_PARAM_UID]
        queue_manager.stu_ask_q(uid)
    ## Tutor actions ##
    # tutor gets done answering a question
    elif (method == MSG_TUT_DONE):
        uid = msg_map[MSG_PARAM_UID]
        queue_manager.tut_ans_q(uid)
    ## Error - Command not found ##
    else:
        printd("Unknown message: " + str(body))

#### MAIN       ####

def main():
    '''
    Main execution point of the program
    '''

    # establish connection to server
    print("+ Starting MMCGA Server...")
    queue_manager = QueueManager()
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
