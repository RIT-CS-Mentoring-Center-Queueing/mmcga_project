##
## File:    bunny.py
##
## Author:  Schuyler Martin <sam8050@rit.edu>
##
## Description: Python class that provides infrastructure for sending messages
##              over RabbitMQ to client devices/users
##

# Python libraries
import json
import pika
import sqlite3

# project libraries
from datagrams.json_db_encoder import JSON_DB_Encoder
from utils.macros import *
from utils.utils import printd
from users.user import User

#### GLOBALS    ####

#### CLASS      ####

class Bunny:
    '''
    Bunny object, an interface/wrapper for the RabbitMQ messaging system
    This class keeps track of who we are messaging
    '''

    def __init__(self):
        '''
        Constructs a Bunny object, an interface/wrapper for RabbitMQ messaging
        '''
        # table that tracks connected/registered Users
        # originally I thought we would need to track User IPs but that's
        # handled by the RabbitMQ server. This server and user clients just
        # need to be pointed to look at the correct message queue
        self.uid_tbl = {}
        # default RabbitMQ exchange to use for out-going messages
        self.exchange = ""
        # init the database, if need be
        self.__db_init()

    def __str__(self):
        '''
        Converts Bunny object to a string equivalent
        '''
        result = "===== Bunny Interface =====\n"
        for key in self.uid_tbl:
            result += str(key) + "\n -> " + str(self.uid_tbl[key]) + "\n"
        return result

    def __contains__(self, uid):
        '''
        Checks if user is registered
        :param: uid User/UID that identifies who we are looking up
        :return: True if the UID is found, False otherwise
        '''
        uid = User.get_uid(uid)
        return uid in self.uid_tbl

    #### BEGIN: Internal Functions ####
    def __send_msg(self, msg_queue, var_tbl):
        '''
        Sends a message to a specific message queue
        :param: msg_queue Message queue to write to 
        :param: var_tbl Dictionary hash table that stores values to send over
                the network in a packaged way.
        :return: JSON string sent to device or None if there is a failure
        '''
        # convert variable table into a JSON string to send over
        json_str = json.dumps(var_tbl)

        # connect to the targeted device by establishing connection to server
        socket = pika.BlockingConnection(
            pika.ConnectionParameters(SERVER_HOST)
        )
        channel = socket.channel()
        # send information to a specific RabbitMQ queue
        channel.queue_declare(queue=msg_queue)
        # actually submit the message
        channel.basic_publish(exchange=self.exchange,
            routing_key=msg_queue,
            body=json_str);
        printd("Sent to queue " + msg_queue + ":")
        printd(json_str)
        # close the connection
        socket.close()
        return json_str

    ## BEGIN: DB Functions ##

    def __db_connect(self):
        '''
        Connects to the database
        :return: Database connection object
        '''
        # connect to the database
        if (DEBUG_MACRO):
            db_connect = sqlite3.connect(SQL_DB_DEBUG)
        else:
            db_connect = sqlite3.connect(SQL_DB)
        return db_connect

    def __db_disconnect(self, db_connect):
        '''
        Disconnects to the database and commit changes
        :param: db_connect Connection to the database
        '''
        db_connect.commit()
        db_connect.close()

    def __db_get_tables(self):
        '''
        Fetches a list of all tables
        :return: List of all tables in the database
        '''
        db_connect = self.__db_connect()
        cur = db_connect.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name;
            """)
        lst = cur.fetchall()
        self.__db_disconnect(db_connect)
        return lst

    def __db_tbl_exists(self, tbl_name):
        '''
        Checks if a table exists
        :param: tbl_name Name of the table of interest
        :return: True if the table exists, false otherwise
        '''
        db_connect = self.__db_connect()
        cur = db_connect.execute(
            """
            SELECT COUNT(*)
            FROM sqlite_master
            WHERE type='table' AND name='{tbl}';
            """.format(tbl=tbl_name))
        if (cur.fetchone()[0] == 1):
            self.__db_disconnect(db_connect)
            return True

        self.__db_disconnect(db_connect)
        return False

    def __db_init(self):
        '''
        Initializes the database for the first time
        '''
        db_connect = self.__db_connect()
        # check for tables; build if missing
        if not(self.__db_tbl_exists(DB_USER_TBL)):
            # make the user table that stores:
            # - UIDs as the Primary Key
            # - User names as an index
            # - JSON serialization of Python object state
            db_connect.execute(
                """
                CREATE TABLE {tbl_name} (
                    {f0} {t0} PRIMARY KEY,
                    {f1} {t1},
                    {f2} {t2}
                );
                """.format(
                    tbl_name=DB_USER_TBL,
                    f0=DB_FIELD_UID,   t0=DB_F_TYPE_TXT,
                    f1=DB_FIELD_UNAME, t1=DB_F_TYPE_TXT,
                    f2=DB_FIELD_JSON,  t2=DB_F_TYPE_TXT,
                )
            )
            db_connect.execute(
                """
                CREATE UNIQUE INDEX {tbl_idx} ON {tbl_name}({f1});
                """.format(
                    tbl_idx=DB_UNAME_IDX,
                    tbl_name=DB_USER_TBL,
                    f1=DB_FIELD_UNAME,
                )
            )
        self.__db_disconnect(db_connect)

    def __db_lookup(self, key):
        '''
        Checks if key is in the database
        :param: key Key to lookup
        :return: True if the key is there, False otherwise
        '''
        pass

    def __db_load(self, key):
        '''
        Loads a JSON map from the a JSON string in the database
        :param: key Key to the data to load
        :return: JSON dictionary mappings from the database
        '''
        pass

    def __db_store(self, obj, tbl):
        '''
        Takes an object, serializes it into JSON, and stores it in the database
        :param: obj Python object to store
        :param: tbl Table to store data into
        :return: JSON string stored in the database
        '''
        json_str = JSON_DB_Encoder.dumps(obj)
        db_connect = self.__db_connect()
        # TODO store object in the database
        self.__db_disconnect(db_connect)
        
    ## END: DB Functions ##
    #### END: Internal Functions ####

    def register(self, user):
        '''
        Adds a user; user connects to the system
        :param: user User object being created
        :return: User object added or None if failure
        '''
        if not(isinstance(user, User)):
            return None
        uid = User.get_uid(user)
        # hash on the uid
        self.uid_tbl[uid] = user
        # send a message so that the client can pick up their UID
        var_tbl = {}
        var_tbl[MSG_PARAM_METHOD] = MSG_USER_ENTER
        var_tbl[MSG_PARAM_USER_UID] = uid
        var_tbl[MSG_PARAM_USER_NAME] = user.name
        self.__send_msg(UID_BOOTSTRAP_QUEUE, var_tbl)
        return user

    def deregister(self, uid):
        '''
        Removes a user; user disconnects to the system
        :param: uid User/UID that identifies who we are removing
        :return: UID removed or None if failure
        '''
        uid = User.get_uid(uid)
        # remove look up in both directions
        if ((type(uid) is str) and (uid in self.uid_tbl)):
            del self.uid_tbl[uid]
            return uid
        # failure; UID is not a string or in the table
        return None

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
        if not(uid in self.uid_tbl):
            return None
        return self.__send_msg(uid, var_tbl)

    def fetch_user(self, uid):
        '''
        Fetches a User object that is registered to the system
        :param: uid User/UID that identifies who we are retrieving
        :return: UID removed or None if failure
        '''
        if (uid in self):
            return self.uid_tbl[uid]
        return None

    @staticmethod
    def parse_msg(msg_body):
        '''
        Takes a message from a device/RabbitMQ and parses it into a hash table
        :param: msg_body RabbitMQ body message received from a device/user
        :return: Dictionary hash table that stores values to received over
                the network in a packaged way.
        '''
        json_str = str(msg_body)
        # strip RabbitMQ's weird body tag information: b'<JSON>'
        json_str = json_str[2:-1]
        # return dictionary map
        return json.loads(json_str)

#### MAIN       ####

def main():
    '''
    Test program for this class
    '''
    bunny = Bunny()
    stu0 = Student("aic4242", "pass", "Alice", "in Chains")
    stu1 = Student("bob8888", "pass", "Bob", "Man")
    stu2 = Student("exo6666", "xkcd", "Evil", "Oscar")
    tut0 = Tutor("tut1234", "pass", "Tutor", "A", "SLI")

    print("Added: " + str(bunny.register(stu0)))
    print("Added: " + str(bunny.register(stu1)))
    print("Added: " + str(bunny.register(stu2)))
    print("Added: " + str(bunny.register(tut0)))
    print(bunny)
    print("Deleted: " + str(bunny.deregister(stu1)))
    print("Deleted: " + str(bunny.deregister(stu2.uid)))
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
    print("Parse JSON to Python dictionary:")
    print(str(Bunny.parse_msg("b'" + test_vars_json + "'")))

if __name__ == "__main__":
    # package only used for testing purposes
    from users.tutor import Tutor
    from users.student import Student
    main()
