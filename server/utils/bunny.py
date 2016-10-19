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
        # table that connects Users (UIDs) to devices (IPs) bidirectionally
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

    def register(self, uid, dev_id):
        '''
        Adds a user; user connects to the system
        :param: uid User/UID that identifies who we are trying to talk to
        :param: dev_id ID of the device (IP)
        :return: UID of user registered
        '''
        uid = User.get_uid(uid)
        # add the connection both ways, in case we need to look up in both
        # directions quickly
        self.uid_dev[uid] = dev_id
        self.uid_dev[dev_id] = uid
        return uid

    def deregister(self, uid):
        '''
        Removes a user; user disconnects to the system
        :param: uid User/UID that identifies who we are trying to talk to
        '''
        uid = User.get_uid(uid)
        dev_id = self.uid_dev[uid]
        # remove look up in both directions
        del self.uid_dev[uid]
        del self.uid_dev[dev_id]
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
        dev_id = self.uid_dev[uid]
        

        # convert variable table into a JSON string to send over
        json_str = json.dumps(var_tbl)

        # connect to the targeted device by establishing connection to server
        socket = pika.BlockingConnection(
            pika.ConnectionParameters(SERVER_HOST)
        )
        channel = socket.channel()
        # send information to a specific RabbitMQ queue
        channel.queue_declare(queue=dev_id)
        # actually submit the message
        channel.basic_publish(exchange=self.exchange,
            routing_key=dev_id,
            body=json_str);
        printd("Sent msg to: " + uid)
        # close the connection
        socket.close()
        return json_str

    def parse_msg(self, msg):
        '''
        Takes a message from a device/RabbitMQ and parses it into a hash table
        :param: msg RabbitMQ message received from a device/user
        :return: Dictionary hash table that stores values to received over
                the network in a packaged way.
        '''
        pass

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    stu0 = Student("Alice")
    stu0_ip = "1.1.1.1"
    stu1 = Student("Bob")
    stu1_ip = "1.1.1.42"
    stu2 = Student("Oscar")
    stu2_ip = "1.6.6.6"
    tut0 = Tutor("Tutor", "SLI")
    tut0_ip = "127.0.0.1"
    bunny = Bunny()
    print("Added: " + bunny.register(stu0, stu0_ip))
    print("Added: " + bunny.register(stu1.uid, stu1_ip))
    print("Added: " + bunny.register(stu2, stu2_ip))
    print("Added: " + bunny.register(tut0, tut0_ip))
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
