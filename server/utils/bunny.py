##
## File:    bunny.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that provides infrastructure for sending messages
## over RabbitMQ to client devices/users
##

# Python libraries
import json
import pika

# project libraries
from utils.macros import *
from utils.utils import printd
from users.user import User

#### GLOBALS    ####

#### FUNCTIONS  ####

class Bunny:
    '''
    Bunny object, an interface/wrapper for the RabbitMQ messaging system
    This class keeps track of who we are messaging
    '''

    def __init__(self):
        '''
        Constructs a Bunny object, an interface/wrapper for RabbitMQ messaging
        '''
        # table that tracks connected Users
        # originally I thought we would need to track User IPs but that's
        # handled by the RabbitMQ server. This server and user clients just
        # need to be pointed to look at the correct message queue
        self.uid_dev = {}
        # default RabbitMQ exchange to use for out-going messages
        self.exchange = ""

    def __str__(self):
        '''
        Converts Bunny object to a string equivalent
        '''
        result = "===== Bunny Interface =====\n"
        for key in self.uid_dev:
            result += str(key) + " -> " + str(self.uid_dev[key]) + "\n"
        return result

    def register(self, uid):
        '''
        Adds a user; user connects to the system
        :param: uid User/UID that identifies who we are trying to talk to
        :return: UID of user registered
        '''
        uid = User.get_uid(uid)
        # add the connection; I don't like using the Python set so I'm going
        # to leave this as an empty look-up
        self.uid_dev[uid] = ""
        return uid

    def deregister(self, uid):
        '''
        Removes a user; user disconnects to the system
        :param: uid User/UID that identifies who we are trying to talk to
        '''
        uid = User.get_uid(uid)
        # remove look up in both directions
        del self.uid_dev[uid]
        return uid

    def send_msg(self, uid, var_tbl):
        '''
        Sends a message to a target user's device
        :param: uid User/UID that identifies who we are trying to talk to 
        :param: var_tbl Dictionary hash table that stores values to send over
                the network in a packaged way.
        :return: JSON string sent to device or None if there is a failure
        '''
        # perform some type checking and data validation
        uid = User.get_uid(uid)
        if not(uid in self.uid_dev):
            return None

        # convert variable table into a JSON string to send over
        json_str = json.dumps(var_tbl)

        # connect to the targeted device by establishing connection to server
        socket = pika.BlockingConnection(
            pika.ConnectionParameters(SERVER_HOST)
        )
        channel = socket.channel()
        # send information to a specific RabbitMQ queue
        channel.queue_declare(queue=uid)
        # actually submit the message
        channel.basic_publish(exchange=self.exchange,
            routing_key=uid,
            body=json_str);
        printd("Sent msg to " + uid + ":")
        printd(json_str)
        # close the connection
        socket.close()
        return json_str

    def parse_msg(self, msg_body):
        '''
        Takes a message from a device/RabbitMQ and parses it into a hash table
        :param: msg_body RabbitMQ body message received from a device/user
        :return: Dictionary hash table that stores values to received over
                the network in a packaged way.
        '''
        out_map = {}
        return out_map

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    stu0 = Student("Alice")
    stu1 = Student("Bob")
    stu2 = Student("Oscar")
    tut0 = Tutor("Tutor", "SLI")
    bunny = Bunny()
    print("Added: " + bunny.register(stu0))
    print("Added: " + bunny.register(stu1.uid))
    print("Added: " + bunny.register(stu2))
    print("Added: " + bunny.register(tut0))
    print(bunny)
    print("Deleted: " + bunny.deregister(stu1))
    print("Deleted: " + bunny.deregister(stu2.uid))
    print(bunny)

    # send some stuff to RabbitMQ
    print("Sending to RabbitMQ...")
    test_vars = {}
    test_vars['name'] = stu0.name
    test_vars['uid'] = stu0.uid
    test_vars['lst'] = [1, 2, 3, 4, 5]
    test_vars_json = json.dumps(test_vars)
    print(bunny.send_msg(stu0, test_vars) == test_vars_json)
    print(bunny.send_msg(stu1, test_vars) == None)

if __name__ == "__main__":
    # package only used for testing purposes
    from users.tutor import Tutor
    from users.student import Student
    main()
