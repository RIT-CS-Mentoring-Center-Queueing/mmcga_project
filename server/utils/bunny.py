##
## File:    bunny.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that provides infrastructure for sending messages
## over RabbitMQ to client devices/users
##

from utils.macros import *
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
        '''
        uid = User.get_uid(uid)
        dev_id = self.uid_dev[uid]
        # connect to the targeted device
        # convert variable table into a JSON string to send over
        pass

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
    tut0_ip = "2.2.2.2"
    bunny = Bunny()
    print("Added: " + bunny.register(stu0, stu0_ip))
    print("Added: " + bunny.register(stu1.uid, stu1_ip))
    print("Added: " + bunny.register(stu2, stu2_ip))
    print("Added: " + bunny.register(tut0, tut0_ip))
    print(bunny)
    print("Deleted: " + bunny.deregister(stu1))
    print("Deleted: " + bunny.deregister(stu2.uid))
    print(bunny)
    

if __name__ == "__main__":
    # package only used for testing purposes
    from users.tutor import Tutor
    from users.student import Student
    main()
